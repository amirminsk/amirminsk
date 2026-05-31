import cv2
import numpy as np

img = cv2.imread('Figure_P2.jpg', cv2.IMREAD_GRAYSCALE)
h, w = img.shape

# step 1: find threshold using otsu's method
# loop through all possible thresholds and find the one with max between-class variance

hist = [0] * 256
for i in range(h):
    for j in range(w):
        hist[img[i, j]] += 1

total = h * w
total_mean = sum(t * hist[t] for t in range(256)) / total

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
    between = w0 * w1 * (sum0/w0 - mean1)**2
    if between > best_var:
        best_var = between
        best_t = t

print(f'threshold: {best_t}')

# step 2: binarize the image
binary = np.zeros((h, w), dtype=np.uint8)
for i in range(h):
    for j in range(w):
        if img[i, j] > best_t:
            binary[i, j] = 1

cv2.imwrite('binary_P2.jpg', binary * 255)


# step 3: erosion - a pixel is 1 only if all 9 pixels around it are also 1
def erode(b):
    bh, bw = b.shape
    padded = np.zeros((bh+2, bw+2), dtype=np.uint8)
    padded[1:bh+1, 1:bw+1] = b
    res = np.ones((bh, bw), dtype=np.uint8)
    for di in range(3):
        for dj in range(3):
            res = res & padded[di:di+bh, dj:dj+bw]
    return res


# boundary = original - eroded
# do it for white regions and black regions separately then combine
eroded = erode(binary)
boundary1 = binary - eroded

inv = 1 - binary
eroded_inv = erode(inv)
boundary2 = inv - eroded_inv

boundary = boundary1 | boundary2

cv2.imwrite('Output_P2.jpg', boundary * 255)
print(f'done, boundary pixels: {int(boundary.sum())}')
