import cv2
import numpy as np

# read the image in grayscale
pic = cv2.imread('Figure_P2.jpg', cv2.IMREAD_GRAYSCALE)
rows = pic.shape[0]
cols = pic.shape[1]

# ---------- first i need to make it black and white ----------
# i used otsu method to pick the threshold automatically
# count how many pixels have each gray value (0 to 255)
counts = np.bincount(pic.ravel(), minlength=256)
num_pixels = rows * cols

# average gray value of the whole image
avg = 0
for g in range(256):
    avg += g * int(counts[g])
avg = avg / num_pixels

# try every threshold and keep the one that separates best
chosen = 0
maxv = 0
back_weight = 0.0     # weight of background group
back_sum = 0.0        # weighted sum for background

for t in range(256):
    back_weight += counts[t] / num_pixels
    back_sum += t * counts[t] / num_pixels
    if back_weight == 0 or back_weight == 1:
        continue
    fore_weight = 1 - back_weight
    back_mean = back_sum / back_weight
    fore_mean = (avg - back_sum) / fore_weight
    # between class variance
    v = back_weight * fore_weight * (back_mean - fore_mean) ** 2
    if v > maxv:
        maxv = v
        chosen = t

print("threshold i got:", chosen)

# now make the binary image, white where brighter than threshold
bw = np.zeros((rows, cols), dtype=np.uint8)
bw[pic > chosen] = 1
cv2.imwrite('binary_P2.jpg', bw * 255)


# ---------- now do erosion to find the boundary ----------
# erosion: keep a pixel white only if all 8 neighbours + itself are white
# i do this by shifting the image around and ANDing them together

def do_erosion(image):
    r = image.shape[0]
    c = image.shape[1]
    # add a black border so the edges dont break
    bigger = np.zeros((r + 2, c + 2), dtype=np.uint8)
    bigger[1:r+1, 1:c+1] = image

    out = np.ones((r, c), dtype=np.uint8)
    for a in range(3):
        for b in range(3):
            out = out & bigger[a:a+r, b:b+c]
    return out

shrunk = do_erosion(bw)

# the boundary is whatever erosion removed
edge = bw - shrunk

# save final result
cv2.imwrite('Output_P2.jpg', edge * 255)
print("finished. number of edge pixels:", int(edge.sum()))
