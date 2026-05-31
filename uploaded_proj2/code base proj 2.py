import cv2
import numpy as np


pic = cv2.imread('Figure_P2.jpg', cv2.IMREAD_GRAYSCALE)
rows = pic.shape[0]
cols = pic.shape[1]


counts = np.bincount(pic.ravel(), minlength=256)
num_pixels = rows * cols


avg = 0
for g in range(256):
    avg += g * int(counts[g])
avg = avg / num_pixels


chosen = 0
maxv = 0
back_weight = 0.0     
back_sum = 0.0       

for t in range(256):
    back_weight += counts[t] / num_pixels
    back_sum += t * counts[t] / num_pixels
    if back_weight == 0 or back_weight == 1:
        continue
    fore_weight = 1 - back_weight
    back_mean = back_sum / back_weight
    fore_mean = (avg - back_sum) / fore_weight

    v = back_weight * fore_weight * (back_mean - fore_mean) ** 2
    if v > maxv:
        maxv = v
        chosen = t

print("threshold i got:", chosen)


bw = np.zeros((rows, cols), dtype=np.uint8)
bw[pic > chosen] = 1
cv2.imwrite('binary_P2.jpg', bw * 255)




def do_erosion(image):
    r = image.shape[0]
    c = image.shape[1]

    bigger = np.zeros((r + 2, c + 2), dtype=np.uint8)
    bigger[1:r+1, 1:c+1] = image

    out = np.ones((r, c), dtype=np.uint8)
    for a in range(3):
        for b in range(3):
            out = out & bigger[a:a+r, b:b+c]
    return out

shrunk = do_erosion(bw)
edge = bw - shrunk


cv2.imwrite('Output_P2.jpg', edge * 255)
print("finished. number of edge pixels:", int(edge.sum()))
