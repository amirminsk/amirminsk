import cv2
import numpy as np

# load image
img = cv2.imread('Figure_P2.jpg', cv2.IMREAD_GRAYSCALE)
h, w = img.shape

# ---- step 1: binarize using Otsu's method ----
# build histogram (numpy counting is basic math)
hist = np.bincount(img.ravel(), minlength=256)
total = h * w

# find best threshold by maximising between-class variance
total_mean = sum(t * int(hist[t]) for t in range(256)) / total
best_t = 0
best_var = 0.0
w0 = 0.0
sum0 = 0.0

for t in range(256):
    w0 += hist[t] / total
    sum0 += t * hist[t] / total
    if w0 == 0 or w0 == 1:
        continue
    w1 = 1 - w0
    mean1 = (total_mean - sum0) / w1
    between = w0 * w1 * (sum0 / w0 - mean1) ** 2
    if between > best_var:
        best_var = between
        best_t = t

print(f'threshold: {best_t}')

# apply threshold
binary = (img > best_t).astype(np.uint8)
cv2.imwrite('binary_P2.jpg', binary * 255)

# ---- step 2: morphological erosion ----
# a pixel stays 1 only if all 9 pixels in its 3x3 neighbourhood are 1
def erode(b):
    bh, bw = b.shape
    padded = np.zeros((bh + 2, bw + 2), dtype=np.uint8)
    padded[1:bh+1, 1:bw+1] = b
    result = np.ones((bh, bw), dtype=np.uint8)
    for di in range(3):
        for dj in range(3):
            result = result & padded[di:di+bh, dj:dj+bw]
    return result

# ---- step 3: boundary = original - eroded ----
eroded = erode(binary)
boundary = binary - eroded

# save output
cv2.imwrite('Output_P2.jpg', boundary * 255)
print(f'done, boundary pixels: {int(boundary.sum())}')
