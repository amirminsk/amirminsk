"""Simple before/after figures for the report."""
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

pairs = [
    ('Picture_P1/1.jpg', 'output_1.jpeg', 'fig_image1.png',
     'Image 1 – Salt noise', 'Denoised (5×5 Median filter)'),
    ('Picture_P1/2.jpg', 'output_2.jpeg', 'fig_image2.png',
     'Image 2 – Gaussian noise', 'Denoised (5×5 Gaussian filter, σ=1.5)'),
    ('Picture_P1/3.jpg', 'output_3.jpeg', 'fig_image3.png',
     'Image 3 – Periodic noise', 'Denoised (Freq-domain low-pass filter)'),
]

for orig_path, out_path, save_path, label_orig, label_out in pairs:
    orig = cv2.imread(orig_path, cv2.IMREAD_GRAYSCALE)
    out  = cv2.imread(out_path,  cv2.IMREAD_GRAYSCALE)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    ax1.imshow(orig, cmap='gray', vmin=0, vmax=255)
    ax1.set_title(label_orig)
    ax1.axis('off')
    ax2.imshow(out,  cmap='gray', vmin=0, vmax=255)
    ax2.set_title(label_out)
    ax2.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f'Saved {save_path}')
