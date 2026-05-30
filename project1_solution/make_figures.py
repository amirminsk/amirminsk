"""Generate comparison figures for the Project 1 report."""
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def spectrum(img):
    F = np.fft.fftshift(np.fft.fft2(img.astype(float)))
    return 20 * np.log1p(np.abs(F))


pairs = [
    ('Picture_P1/1.jpg', 'output_1.jpeg',
     'Image 1', 'Salt Noise', 'Median Filter (5×5)'),
    ('Picture_P1/2.jpg', 'output_2.jpeg',
     'Image 2', 'Gaussian Noise', 'Gaussian Filter (7×7, σ=2.0)'),
    ('Picture_P1/3.jpg', 'output_3.jpeg',
     'Image 3', 'Mixed Noise', 'Median (3×3) + Freq-domain LPF'),
]

for orig_path, out_path, label, noise_label, method_label in pairs:
    orig = cv2.imread(orig_path, cv2.IMREAD_GRAYSCALE)
    out  = cv2.imread(out_path,  cv2.IMREAD_GRAYSCALE)

    fig, axes = plt.subplots(1, 4, figsize=(14, 4))
    fig.suptitle(f'{label}: {noise_label}  →  {method_label}', fontsize=12)

    axes[0].imshow(orig, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title('Original (noisy)')
    axes[0].axis('off')

    axes[1].imshow(spectrum(orig), cmap='hot')
    axes[1].set_title('Frequency Spectrum (original)')
    axes[1].axis('off')

    axes[2].imshow(out, cmap='gray', vmin=0, vmax=255)
    axes[2].set_title('Denoised output')
    axes[2].axis('off')

    axes[3].imshow(spectrum(out), cmap='hot')
    axes[3].set_title('Frequency Spectrum (denoised)')
    axes[3].axis('off')

    plt.tight_layout()
    fname = f'fig_{label.replace(" ", "").lower()}.png'
    plt.savefig(fname, dpi=120, bbox_inches='tight')
    plt.close()
    print(f'Saved {fname}')
