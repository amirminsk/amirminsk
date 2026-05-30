"""
COMP5033 Project 1 - Image Enhancement/Restoration
Noise analysis and denoising for three assigned images.

Rules: no cv2 key processing; cv2 used only for I/O;
       numpy used for all numerical operations.
"""

import os
import cv2
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


# ── Filter implementations ────────────────────────────────────────────────────

def median_filter(img: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Median filter for salt-and-pepper (impulse) noise.
    Each output pixel = median of the kernel_size×kernel_size neighbourhood.
    """
    assert img.ndim == 2, "Expects a single-channel (grayscale) image"
    pad = kernel_size // 2
    padded = np.pad(img, pad, mode='reflect')
    # shape: (H, W, ks, ks)
    windows = sliding_window_view(padded, (kernel_size, kernel_size))
    return np.median(windows, axis=(-2, -1)).astype(np.uint8)


def _gaussian_kernel(size: int, sigma: float) -> np.ndarray:
    k = size // 2
    y, x = np.mgrid[-k:k + 1, -k:k + 1]
    kernel = np.exp(-(x ** 2 + y ** 2) / (2.0 * sigma ** 2))
    return kernel / kernel.sum()


def gaussian_filter(img: np.ndarray, kernel_size: int = 5,
                    sigma: float = 1.4) -> np.ndarray:
    """
    Spatial Gaussian low-pass filter for additive Gaussian noise.
    Convolves the image with a Gaussian kernel computed from scratch.
    """
    assert img.ndim == 2
    kernel = _gaussian_kernel(kernel_size, sigma)
    pad = kernel_size // 2
    padded = np.pad(img.astype(np.float64), pad, mode='reflect')
    windows = sliding_window_view(padded, (kernel_size, kernel_size))
    result = (windows * kernel).sum(axis=(-2, -1))
    return np.clip(result, 0, 255).astype(np.uint8)


def freq_gaussian_lowpass(img: np.ndarray,
                           cutoff_ratio: float = 0.25) -> np.ndarray:
    """
    Frequency-domain Gaussian low-pass filter for periodic / mixed noise.
    Uses 2D DFT (numpy.fft) to attenuate high-frequency noise components
    while preserving low-frequency structure.

    cutoff_ratio: D0 = cutoff_ratio × min(H, W)  (controls bandwidth)
    """
    assert img.ndim == 2
    h, w = img.shape
    F = np.fft.fft2(img.astype(np.float64))
    Fshift = np.fft.fftshift(F)

    cy, cx = h // 2, w // 2
    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    D0 = min(h, w) * cutoff_ratio
    mask = np.exp(-dist ** 2 / (2.0 * D0 ** 2))          # Gaussian envelope

    filtered = np.fft.ifft2(np.fft.ifftshift(Fshift * mask))
    return np.clip(np.abs(filtered), 0, 255).astype(np.uint8)


# ── Noise analysis helpers ────────────────────────────────────────────────────

def estimate_snr(original: np.ndarray, denoised: np.ndarray) -> float:
    signal_power = np.mean(denoised.astype(np.float64) ** 2)
    noise = original.astype(np.float64) - denoised.astype(np.float64)
    noise_power = np.mean(noise ** 2) + 1e-10
    return 10.0 * np.log10(signal_power / noise_power)


def count_impulse_pixels(img: np.ndarray,
                          low: int = 5, high: int = 250) -> int:
    """Count pixels that are likely impulse-noise outliers."""
    return int(np.sum(img < low) + np.sum(img > high))


# ── Main processing ───────────────────────────────────────────────────────────

def process_image_1(input_dir: str) -> None:
    """
    Image 1 (van): Salt noise (isolated bright/white pixels).
    Best remedy: median filter – replaces each pixel with the neighbourhood
    median, eliminating isolated outliers while preserving edges.
    """
    img = cv2.imread(os.path.join(input_dir, '1.jpg'), cv2.IMREAD_GRAYSCALE)
    print(f"\n[Image 1] shape={img.shape}  "
          f"impulse pixels (estimated)={count_impulse_pixels(img)}")

    output = median_filter(img, kernel_size=5)
    cv2.imwrite('output_1.jpeg', output)

    print(f"  -> 5×5 Median filter applied.")
    print(f"     SNR improvement: {estimate_snr(img, output):.2f} dB")
    print(f"     Saved: output_1.jpeg")


def process_image_2(input_dir: str) -> None:
    """
    Image 2 (dog): Additive Gaussian noise (uniform fine-grained texture).
    Best remedy: Gaussian low-pass filter – averages the neighbourhood with
    Gaussian weights to suppress zero-mean random noise.
    """
    img = cv2.imread(os.path.join(input_dir, '2.jpg'), cv2.IMREAD_GRAYSCALE)
    print(f"\n[Image 2] shape={img.shape}  "
          f"std-dev (proxy for noise level)={img.std():.2f}")

    output = gaussian_filter(img, kernel_size=7, sigma=2.0)
    cv2.imwrite('output_2.jpeg', output)

    print(f"  -> 7×7 Gaussian filter (σ=2.0) applied.")
    print(f"     SNR improvement: {estimate_snr(img, output):.2f} dB")
    print(f"     Saved: output_2.jpeg")


def process_image_3(input_dir: str) -> None:
    """
    Image 3 (ABUNDANCE sign): Mixed noise – Gaussian + periodic / structured
    components visible as a regular dot pattern.
    Two-stage approach:
      Stage 1 – 3×3 median filter to suppress any remaining impulse pixels.
      Stage 2 – Frequency-domain Gaussian LPF to attenuate periodic and
                 high-frequency noise while preserving text edges.
    """
    img = cv2.imread(os.path.join(input_dir, '3.jpg'), cv2.IMREAD_GRAYSCALE)
    print(f"\n[Image 3] shape={img.shape}  "
          f"std-dev={img.std():.2f}  impulse={count_impulse_pixels(img)}")

    stage1 = median_filter(img, kernel_size=3)
    output = freq_gaussian_lowpass(stage1, cutoff_ratio=0.25)
    cv2.imwrite('output_3.jpeg', output)

    print(f"  -> 3×3 Median  +  Freq-domain Gaussian LPF (D0=0.25·min(H,W)).")
    print(f"     SNR improvement: {estimate_snr(img, output):.2f} dB")
    print(f"     Saved: output_3.jpeg")


def main() -> None:
    input_dir = 'Picture_P1'
    print("COMP5033 Project 1 – Image Denoising")
    print("=" * 45)
    process_image_1(input_dir)
    process_image_2(input_dir)
    process_image_3(input_dir)
    print("\nAll images processed successfully.")


if __name__ == '__main__':
    main()
