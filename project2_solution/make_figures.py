"""Generate comparison figures for the Project 2 report."""
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

img    = cv2.imread('Figure_P2.jpg',  cv2.IMREAD_GRAYSCALE)
binary = cv2.imread('binary_P2.jpg', cv2.IMREAD_GRAYSCALE)
output = cv2.imread('Output_P2.jpg', cv2.IMREAD_GRAYSCALE)

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle('Project 2 – Morphological Boundary Detection', fontsize=13)

axes[0].imshow(img,    cmap='gray'); axes[0].set_title('Original image (grayscale)'); axes[0].axis('off')
axes[1].imshow(binary, cmap='gray'); axes[1].set_title('Binary image (Otsu T*=107)'); axes[1].axis('off')
axes[2].imshow(output, cmap='gray'); axes[2].set_title('Boundary image (Output_P2)'); axes[2].axis('off')

plt.tight_layout()
plt.savefig('fig_p2_comparison.png', dpi=120, bbox_inches='tight')
plt.close()
print('Saved fig_p2_comparison.png')
