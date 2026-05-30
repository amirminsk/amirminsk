"""
COMP5033 Project 1 - Image Denoising
"""

import cv2
import math
import numpy as np


# ----- median filter -----
def median_filter(img, kernel_size):
    k = kernel_size // 2
    h, w = img.shape
    output = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            vals = []
            for di in range(-k, k + 1):
                for dj in range(-k, k + 1):
                    ni = min(max(i + di, 0), h - 1)
                    nj = min(max(j + dj, 0), w - 1)
                    vals.append(int(img[ni, nj]))
            vals.sort()
            output[i, j] = vals[len(vals) // 2]
    return output


# ----- Gaussian filter -----
def make_gaussian_kernel(size, sigma):
    k = size // 2
    kernel = [[0.0] * size for _ in range(size)]
    total = 0.0
    for i in range(size):
        for j in range(size):
            x, y = i - k, j - k
            val = math.exp(-(x * x + y * y) / (2 * sigma * sigma))
            kernel[i][j] = val
            total += val
    for i in range(size):
        for j in range(size):
            kernel[i][j] /= total
    return kernel

def gaussian_filter(img, kernel_size, sigma):
    k = kernel_size // 2
    h, w = img.shape
    kernel = make_gaussian_kernel(kernel_size, sigma)
    output = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            val = 0.0
            for di in range(-k, k + 1):
                for dj in range(-k, k + 1):
                    ni = min(max(i + di, 0), h - 1)
                    nj = min(max(j + dj, 0), w - 1)
                    val += kernel[di + k][dj + k] * int(img[ni, nj])
            output[i, j] = min(255, max(0, int(val)))
    return output


# ----- frequency-domain low-pass filter -----
def freq_lowpass_filter(img, cutoff):
    h, w = img.shape
    # FFT is a mathematical operation - no simple manual replacement
    F = np.fft.fft2(img.astype(float))
    Fshift = np.fft.fftshift(F)

    cy, cx = h // 2, w // 2
    mask = np.zeros((h, w))
    for u in range(h):
        for v in range(w):
            dist2 = (u - cy) ** 2 + (v - cx) ** 2
            mask[u, v] = math.exp(-dist2 / (2 * cutoff * cutoff))

    Ffiltered = Fshift * mask
    img_back = np.fft.ifft2(np.fft.ifftshift(Ffiltered))

    output = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            output[i, j] = min(255, max(0, int(abs(img_back[i, j]))))
    return output


# ============================================================
# Main
# ============================================================

img1 = cv2.imread('Picture_P1/1.jpg', cv2.IMREAD_GRAYSCALE)
print("Processing image 1 (median filter)...")
out1 = median_filter(img1, kernel_size=5)
cv2.imwrite('output_1.jpeg', out1)
print("  saved output_1.jpeg")

img2 = cv2.imread('Picture_P1/2.jpg', cv2.IMREAD_GRAYSCALE)
print("Processing image 2 (Gaussian filter)...")
out2 = gaussian_filter(img2, kernel_size=5, sigma=1.5)
cv2.imwrite('output_2.jpeg', out2)
print("  saved output_2.jpeg")

img3 = cv2.imread('Picture_P1/3.jpg', cv2.IMREAD_GRAYSCALE)
print("Processing image 3 (frequency-domain low-pass)...")
out3 = freq_lowpass_filter(img3, cutoff=40)
cv2.imwrite('output_3.jpeg', out3)
print("  saved output_3.jpeg")

print("Done.")
