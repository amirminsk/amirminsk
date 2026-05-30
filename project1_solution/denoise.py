"""
COMP5033 Project 1 - Image Denoising
"""

import cv2
import numpy as np


# ----- helper: build Gaussian kernel -----
def make_gaussian_kernel(size, sigma):
    k = size // 2
    kernel = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            x = i - k
            y = j - k
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel = kernel / np.sum(kernel)   # normalise so weights sum to 1
    return kernel


# ----- median filter (for salt-and-pepper noise) -----
def median_filter(img, kernel_size):
    k = kernel_size // 2
    h, w = img.shape
    # pad with edge values to handle borders
    padded = np.pad(img, k, mode='edge')
    output = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            window = padded[i : i + kernel_size, j : j + kernel_size]
            output[i, j] = np.median(window)
    return output


# ----- Gaussian filter (for Gaussian noise) -----
def gaussian_filter(img, kernel_size, sigma):
    kernel = make_gaussian_kernel(kernel_size, sigma)
    k = kernel_size // 2
    h, w = img.shape
    padded = np.pad(img.astype(np.float64), k, mode='edge')
    output = np.zeros((h, w), dtype=np.float64)
    for i in range(h):
        for j in range(w):
            window = padded[i : i + kernel_size, j : j + kernel_size]
            output[i, j] = np.sum(window * kernel)
    output = np.clip(output, 0, 255).astype(np.uint8)
    return output


# ----- frequency-domain low-pass filter (for periodic noise) -----
def freq_lowpass_filter(img, cutoff):
    h, w = img.shape
    # 2D Fourier transform
    F = np.fft.fft2(img.astype(np.float64))
    Fshift = np.fft.fftshift(F)

    # build a Gaussian low-pass mask centred at (cy, cx)
    cy, cx = h // 2, w // 2
    mask = np.zeros((h, w))
    for u in range(h):
        for v in range(w):
            dist = np.sqrt((u - cy)**2 + (v - cx)**2)
            mask[u, v] = np.exp(-(dist**2) / (2 * cutoff**2))

    # apply mask and inverse transform
    Ffiltered = Fshift * mask
    img_back = np.fft.ifft2(np.fft.ifftshift(Ffiltered))
    result = np.abs(img_back)
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result


# ============================================================
# Main
# ============================================================

# --- Image 1: salt noise -> median filter ---
img1 = cv2.imread('Picture_P1/1.jpg', cv2.IMREAD_GRAYSCALE)
print("Processing image 1 (median filter)...")
out1 = median_filter(img1, kernel_size=5)
cv2.imwrite('output_1.jpeg', out1)
print("  saved output_1.jpeg")

# --- Image 2: Gaussian noise -> Gaussian filter ---
img2 = cv2.imread('Picture_P1/2.jpg', cv2.IMREAD_GRAYSCALE)
print("Processing image 2 (Gaussian filter)...")
out2 = gaussian_filter(img2, kernel_size=5, sigma=1.5)
cv2.imwrite('output_2.jpeg', out2)
print("  saved output_2.jpeg")

# --- Image 3: periodic/mixed noise -> frequency-domain filter ---
img3 = cv2.imread('Picture_P1/3.jpg', cv2.IMREAD_GRAYSCALE)
print("Processing image 3 (frequency-domain low-pass)...")
out3 = freq_lowpass_filter(img3, cutoff=40)
cv2.imwrite('output_3.jpeg', out3)
print("  saved output_3.jpeg")

print("Done.")
