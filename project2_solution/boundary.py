"""
COMP5033 Project 2 – Morphological Image Processing
Find the boundary of a binary image using morphological erosion.

Steps:
  1. Load Figure_P2.jpg (1024×1024 grayscale)
  2. Binarize with Otsu's method (implemented from scratch)
  3. Apply morphological erosion (implemented from scratch)
  4. Boundary = binary image − eroded image
  5. Save Output_P2.jpg

Rules: no cv2 key processing; cv2 used only for I/O;
       numpy used for all numerical operations.
"""

import cv2
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


# ── Otsu's thresholding ───────────────────────────────────────────────────────

def otsu_threshold(img: np.ndarray) -> int:
    """
    Find the optimal binarization threshold by maximising the inter-class
    variance (Otsu, 1979).

        σ²_B(t) = w₀(t)·w₁(t)·[μ₀(t) − μ₁(t)]²

    Returns the threshold t* that maximises σ²_B.
    """
    hist, _ = np.histogram(img.ravel(), bins=256, range=(0, 256))
    total_px = img.size
    total_sum = float(np.dot(np.arange(256), hist))

    best_thresh, best_var = 0, 0.0
    w0, cumsum = 0.0, 0.0

    for t in range(256):
        w0 += hist[t]
        if w0 == 0:
            continue
        w1 = total_px - w0
        if w1 == 0:
            break
        cumsum += t * hist[t]
        mu0 = cumsum / w0
        mu1 = (total_sum - cumsum) / w1
        var_between = w0 * w1 * (mu0 - mu1) ** 2
        if var_between > best_var:
            best_var = var_between
            best_thresh = t

    return best_thresh


def binarize(img: np.ndarray, threshold: int) -> np.ndarray:
    """Return a {0, 1} binary image: 1 where pixel > threshold."""
    return (img > threshold).astype(np.uint8)


# ── Morphological operations ──────────────────────────────────────────────────

def erosion(binary: np.ndarray, se_size: int = 3) -> np.ndarray:
    """
    Morphological erosion with a square structuring element (se_size × se_size).
    A pixel p in the output is 1 iff every pixel in the se_size×se_size
    neighbourhood centred at p is 1 in the input.

    Equivalent to a min-filter on a binary image.
    """
    pad = se_size // 2
    padded = np.pad(binary, pad, mode='constant', constant_values=0)
    windows = sliding_window_view(padded, (se_size, se_size))
    # shape: (H, W, se_size, se_size)
    return np.all(windows == 1, axis=(-2, -1)).astype(np.uint8)


def dilation(binary: np.ndarray, se_size: int = 3) -> np.ndarray:
    """
    Morphological dilation with a square structuring element.
    A pixel p is 1 iff at least one pixel in its neighbourhood is 1.
    """
    pad = se_size // 2
    padded = np.pad(binary, pad, mode='constant', constant_values=0)
    windows = sliding_window_view(padded, (se_size, se_size))
    return np.any(windows == 1, axis=(-2, -1)).astype(np.uint8)


def extract_boundary(binary: np.ndarray, se_size: int = 3) -> np.ndarray:
    """
    Inner boundary of a binary region:
        β(A) = A − (A ⊖ B)
    where ⊖ denotes erosion and B is the structuring element.
    """
    return binary - erosion(binary, se_size)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("COMP5033 Project 2 – Morphological Boundary Detection")
    print("=" * 55)

    # 1. Load
    img = cv2.imread('Figure_P2.jpg', cv2.IMREAD_GRAYSCALE)
    print(f"  Loaded image: shape={img.shape}  dtype={img.dtype}")

    # 2. Binarize via Otsu
    T = otsu_threshold(img)
    print(f"  Otsu threshold T* = {T}")
    binary = binarize(img, T)
    foreground_ratio = binary.mean() * 100
    print(f"  Foreground pixels: {foreground_ratio:.1f}%")

    # Save intermediate binary image for reference / report
    cv2.imwrite('binary_P2.jpg', (binary * 255).astype(np.uint8))
    print("  Saved binary image: binary_P2.jpg")

    # 3. Compute inner boundary for bright foreground
    boundary_fg = extract_boundary(binary, se_size=3)

    # 4. Also compute boundary for dark (inverted) foreground to capture
    #    boundaries of black regions (e.g. the dark cat in the yin-yang design)
    binary_inv = (1 - binary).astype(np.uint8)
    boundary_bg = extract_boundary(binary_inv, se_size=3)

    # 5. Union of both boundaries → all edges in the image
    boundary = np.clip(boundary_fg + boundary_bg, 0, 1).astype(np.uint8)

    # 6. Save output
    output = (boundary * 255).astype(np.uint8)
    cv2.imwrite('Output_P2.jpg', output)

    boundary_px = int(boundary.sum())
    print(f"  Boundary pixels: {boundary_px}  "
          f"({boundary_px / img.size * 100:.2f}% of image)")
    print("  Saved: Output_P2.jpg")
    print("\nDone.")


if __name__ == '__main__':
    main()
