"""
COMP5033 Project 2 - Morphological Boundary Detection
"""

import cv2
import numpy as np


# ----- Otsu's thresholding -----
def otsu_threshold(img):
    h, w = img.shape
    total = h * w

    # histogram using a plain Python list
    hist = [0] * 256
    for i in range(h):
        for j in range(w):
            hist[img[i, j]] += 1

    total_mean = sum(t * hist[t] for t in range(256)) / total

    best_t = 0
    best_var = 0.0
    w0 = 0.0
    mean0_sum = 0.0

    for t in range(256):
        w0 += hist[t] / total
        mean0_sum += t * hist[t] / total
        if w0 == 0 or w0 == 1:
            continue
        w1 = 1 - w0
        mean1 = (total_mean - mean0_sum) / w1
        var_between = w0 * w1 * (mean0_sum / w0 - mean1) ** 2
        if var_between > best_var:
            best_var = var_between
            best_t = t

    return best_t


# ----- morphological erosion -----
def erode(binary):
    h, w = binary.shape
    # pad with zeros so border pixels are handled
    padded = np.zeros((h + 2, w + 2), dtype=np.uint8)
    padded[1:h + 1, 1:w + 1] = binary
    # a pixel stays 1 only if the entire 3x3 neighbourhood is 1
    result = np.ones((h, w), dtype=np.uint8)
    for di in range(3):
        for dj in range(3):
            result = result & padded[di:di + h, dj:dj + w]
    return result


# ============================================================
# Main
# ============================================================

img = cv2.imread('Figure_P2.jpg', cv2.IMREAD_GRAYSCALE)
print(f"Image size: {img.shape}")

# binarize
print("Computing Otsu threshold (this may take a moment)...")
T = otsu_threshold(img)
print(f"Otsu threshold: {T}")

h, w = img.shape
binary = np.zeros((h, w), dtype=np.uint8)
for i in range(h):
    for j in range(w):
        if img[i, j] > T:
            binary[i, j] = 1

cv2.imwrite('binary_P2.jpg', binary * 255)
print("Saved binary_P2.jpg")

# boundary of white regions
eroded = erode(binary)
boundary_fg = binary - eroded

# boundary of black regions
binary_inv = np.ones((h, w), dtype=np.uint8) - binary
eroded_inv = erode(binary_inv)
boundary_bg = binary_inv - eroded_inv

# combine
boundary = boundary_fg | boundary_bg
cv2.imwrite('Output_P2.jpg', boundary * 255)
print(f"Boundary pixels: {int(boundary.sum())}")
print("Saved Output_P2.jpg")
