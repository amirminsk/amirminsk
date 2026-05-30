"""
COMP5033 Project 2 - Morphological Boundary Detection
"""

import cv2
import numpy as np


# ----- Otsu's thresholding -----
def otsu_threshold(img):
    # compute histogram
    hist = np.zeros(256)
    for val in img.ravel():
        hist[val] += 1

    total = img.size
    total_mean = np.sum(np.arange(256) * hist) / total

    best_t = 0
    best_var = 0.0

    w0 = 0.0
    mean0 = 0.0

    for t in range(256):
        w0 += hist[t] / total
        if w0 == 0 or w0 == 1:
            continue
        mean0 += t * hist[t] / total
        w1 = 1 - w0
        mean1 = (total_mean - mean0) / w1
        var_between = w0 * w1 * (mean0 / w0 - mean1) ** 2
        if var_between > best_var:
            best_var = var_between
            best_t = t

    return best_t


# ----- morphological erosion with a 3x3 structuring element -----
def erode(binary):
    h, w = binary.shape
    # pad with zeros (background) so borders are handled correctly
    padded = np.pad(binary, 1, constant_values=0)
    result = np.ones((h, w), dtype=np.uint8)
    # a pixel stays 1 only if ALL neighbours in the 3x3 window are 1
    for di in range(3):
        for dj in range(3):
            result = result & padded[di : di + h, dj : dj + w]
    return result


# ============================================================
# Main
# ============================================================

# 1. load image
img = cv2.imread('Figure_P2.jpg', cv2.IMREAD_GRAYSCALE)
print(f"Image size: {img.shape}")

# 2. binarize with Otsu's threshold
T = otsu_threshold(img)
print(f"Otsu threshold: {T}")
binary = (img > T).astype(np.uint8)
cv2.imwrite('binary_P2.jpg', binary * 255)
print("Saved binary_P2.jpg")

# 3. find boundary of white (foreground) regions
eroded = erode(binary)
boundary_fg = binary - eroded

# 4. also find boundary of black (background) regions inside the circle
binary_inv = 1 - binary
eroded_inv = erode(binary_inv)
boundary_bg = binary_inv - eroded_inv

# 5. combine both boundaries
boundary = np.clip(boundary_fg + boundary_bg, 0, 1).astype(np.uint8)

# 6. save output
cv2.imwrite('Output_P2.jpg', boundary * 255)
print(f"Boundary pixels: {boundary.sum()}")
print("Saved Output_P2.jpg")
