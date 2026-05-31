import cv2
import math
import numpy as np

# ---- image 1: i can see white dots everywhere, this is salt noise ----
# i tried 3x3 window first but some noise was still there, 5x5 worked better

pic1 = cv2.imread('Picture_P1/1.jpg', cv2.IMREAD_GRAYSCALE)
rows = pic1.shape[0]
cols = pic1.shape[1]
clean1 = np.zeros((rows, cols), dtype=np.uint8)

half = 2  # half of 5x5 kernel

for i in range(rows):
    for j in range(cols):
        neighbors = []
        for di in range(-half, half+1):
            for dj in range(-half, half+1):
                ni = min(max(i+di, 0), rows-1)
                nj = min(max(j+dj, 0), cols-1)
                neighbors.append(int(pic1[ni, nj]))
        neighbors.sort()
        clean1[i, j] = neighbors[len(neighbors)//2]  # take the middle value

cv2.imwrite('output_1.jpeg', clean1)
print('image 1 done')


# ---- image 2: looks like random grain, this is gaussian noise ----

pic2 = cv2.imread('Picture_P1/2.jpg', cv2.IMREAD_GRAYSCALE)
rows = pic2.shape[0]
cols = pic2.shape[1]

# make the gaussian kernel by hand
sigma = 1.5
ksize = 5
half = ksize // 2
weights = []
total_w = 0.0
for i in range(ksize):
    row = []
    for j in range(ksize):
        x = i - half
        y = j - half
        val = math.exp(-(x*x + y*y) / (2*sigma*sigma))
        row.append(val)
        total_w += val
    weights.append(row)

# normalize so all weights add to 1
for i in range(ksize):
    for j in range(ksize):
        weights[i][j] /= total_w

clean2 = np.zeros((rows, cols), dtype=np.uint8)
for i in range(rows):
    for j in range(cols):
        weighted_sum = 0.0
        for di in range(-half, half+1):
            for dj in range(-half, half+1):
                ni = min(max(i+di, 0), rows-1)
                nj = min(max(j+dj, 0), cols-1)
                weighted_sum += weights[di+half][dj+half] * pic2[ni, nj]
        clean2[i, j] = min(255, max(0, int(weighted_sum)))

cv2.imwrite('output_2.jpeg', clean2)
print('image 2 done')


# ---- image 3: it has salt and pepper dots AND grainy noise ----
# so i do two steps: median to remove the dots, then gaussian to smooth the rest

pic3 = cv2.imread('Picture_P1/3.jpg', cv2.IMREAD_GRAYSCALE)
rows = pic3.shape[0]
cols = pic3.shape[1]

# step 1: median filter 3x3 to remove the salt and pepper noise
denoised = np.zeros((rows, cols), dtype=np.uint8)
half = 1
for i in range(rows):
    for j in range(cols):
        neighbors = []
        for di in range(-half, half+1):
            for dj in range(-half, half+1):
                ni = min(max(i+di, 0), rows-1)
                nj = min(max(j+dj, 0), cols-1)
                neighbors.append(int(pic3[ni, nj]))
        neighbors.sort()
        denoised[i, j] = neighbors[len(neighbors)//2]

# step 2: gaussian filter 5x5 to smooth the remaining grain
# build the kernel by hand (same way as image 2)
sigma = 1.2
ksize = 5
half = ksize // 2
weights = []
total_w = 0.0
for i in range(ksize):
    row = []
    for j in range(ksize):
        x = i - half
        y = j - half
        val = math.exp(-(x*x + y*y) / (2*sigma*sigma))
        row.append(val)
        total_w += val
    weights.append(row)
for i in range(ksize):
    for j in range(ksize):
        weights[i][j] /= total_w

clean3 = np.zeros((rows, cols), dtype=np.uint8)
for i in range(rows):
    for j in range(cols):
        weighted_sum = 0.0
        for di in range(-half, half+1):
            for dj in range(-half, half+1):
                ni = min(max(i+di, 0), rows-1)
                nj = min(max(j+dj, 0), cols-1)
                weighted_sum += weights[di+half][dj+half] * denoised[ni, nj]
        clean3[i, j] = min(255, max(0, int(weighted_sum)))

cv2.imwrite('output_3.jpeg', clean3)
print('image 3 done')
