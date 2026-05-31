import cv2
import math
import numpy as np

# ---- image 1: salt noise ----
# i can see white dots scattered around so this is salt noise
# median filter should work, i tried 3x3 first but 5x5 removed more noise

img1 = cv2.imread('Picture_P1/1.jpg', cv2.IMREAD_GRAYSCALE)
h, w = img1.shape
out1 = np.zeros((h, w), dtype=np.uint8)

k = 2  # 5x5 window, k=2 means 2 pixels each side

for i in range(h):
    for j in range(w):
        vals = []
        for di in range(-k, k+1):
            for dj in range(-k, k+1):
                ni = min(max(i+di, 0), h-1)
                nj = min(max(j+dj, 0), w-1)
                vals.append(int(img1[ni, nj]))
        vals.sort()
        out1[i, j] = vals[len(vals)//2]  # pick the middle value

cv2.imwrite('output_1.jpeg', out1)
print('image 1 done')


# ---- image 2: gaussian noise ----
# the noise looks like random grain everywhere, so gaussian filter

img2 = cv2.imread('Picture_P1/2.jpg', cv2.IMREAD_GRAYSCALE)
h, w = img2.shape

# build 5x5 gaussian kernel manually
sigma = 1.5
ks = 5
k = ks // 2
kernel = []
s = 0.0
for i in range(ks):
    row = []
    for j in range(ks):
        x = i - k
        y = j - k
        v = math.exp(-(x*x + y*y) / (2*sigma*sigma))
        row.append(v)
        s += v
    kernel.append(row)
# normalize
for i in range(ks):
    for j in range(ks):
        kernel[i][j] /= s

out2 = np.zeros((h, w), dtype=np.uint8)
for i in range(h):
    for j in range(w):
        total = 0.0
        for di in range(-k, k+1):
            for dj in range(-k, k+1):
                ni = min(max(i+di, 0), h-1)
                nj = min(max(j+dj, 0), w-1)
                total += kernel[di+k][dj+k] * img2[ni, nj]
        out2[i, j] = min(255, max(0, int(total)))

cv2.imwrite('output_2.jpeg', out2)
print('image 2 done')


# ---- image 3: periodic noise ----
# the dots look like they repeat in a pattern so i used frequency domain filter
# convert to frequency domain, remove high frequencies, convert back

img3 = cv2.imread('Picture_P1/3.jpg', cv2.IMREAD_GRAYSCALE)
h, w = img3.shape

F = np.fft.fft2(img3.astype(float))
Fshift = np.fft.fftshift(F)

# gaussian low pass mask centered at middle
cy = h // 2
cx = w // 2
cutoff = 40
mask = np.zeros((h, w))
for u in range(h):
    for v in range(w):
        d2 = (u - cy)**2 + (v - cx)**2
        mask[u, v] = math.exp(-d2 / (2 * cutoff * cutoff))

result = np.fft.ifft2(np.fft.ifftshift(Fshift * mask))

out3 = np.zeros((h, w), dtype=np.uint8)
for i in range(h):
    for j in range(w):
        out3[i, j] = min(255, max(0, int(abs(result[i, j]))))

cv2.imwrite('output_3.jpeg', out3)
print('image 3 done')
