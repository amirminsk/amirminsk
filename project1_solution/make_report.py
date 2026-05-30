"""Build the Project 1 report (docx) from the provided template."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import copy, os

STUDENT_NAME = "[YOUR NAME]"
STUDENT_ID   = "[YOUR STUDENT ID]"
SUBMIT_DATE  = "2026-05-30"


def heading(doc, text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(13 if level == 1 else 11)
    return p


def body(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    return p


def add_image(doc, path, width=Inches(5.5), caption=None):
    if os.path.exists(path):
        doc.add_picture(path, width=width)
    if caption:
        cp = doc.add_paragraph(caption)
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].italic = True
        cp.runs[0].font.size = Pt(10)


doc = Document()

# ── Title ──────────────────────────────────────────────────────────────────
for line, sz, bold in [
    ('Harbin Institute of Technology (Shenzhen)', 14, True),
    ('Project Report', 16, True),
    ('', 10, False),
    ('Image Processing (COMP5033)', 12, False),
    ('2025–2026 Spring Semester', 12, False),
    ('Lecturer: Prof. Weizheng Zhang', 12, False),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(line)
    run.bold = bold
    run.font.size = Pt(sz)

doc.add_paragraph()

# ── Student info table ─────────────────────────────────────────────────────
table = doc.add_table(rows=2, cols=4)
table.style = 'Table Grid'
cells = table.rows[0].cells
cells[0].text = 'Project No.:'
cells[1].text = '1'
cells[2].text = 'Student Name:'
cells[3].text = STUDENT_NAME

cells = table.rows[1].cells
cells[0].text = 'Student ID:'
cells[1].text = STUDENT_ID
cells[2].text = 'Date of Submission:'
cells[3].text = SUBMIT_DATE

doc.add_paragraph()

# ── Section 1 ─────────────────────────────────────────────────────────────
heading(doc, '1  Project Content')
body(doc,
    'This project addresses image enhancement and restoration. Three 224×224 '
    'grayscale images are provided, each corrupted by a different type of noise. '
    'The objectives are: (1) identify the noise model in each image through visual '
    'and statistical analysis, and (2) apply appropriate denoising filters—implemented '
    'entirely from scratch using NumPy—to recover image quality. '
    'Only cv2 I/O functions and NumPy arithmetic are used; no library denoising '
    'functions (e.g. cv2.medianBlur, cv2.GaussianBlur) are called.')

# ── Section 2 ─────────────────────────────────────────────────────────────
heading(doc, '2  Method Description')

heading(doc, '2.1  Image 1 – Salt Noise → 5×5 Median Filter', level=2)
body(doc,
    'Noise analysis: Image 1 contains isolated, anomalously bright pixels scattered '
    'across the scene (a van on a cobbled street). Statistical analysis reveals '
    '~3,353 pixels (6.7% of the image) with intensity > 250, and the noise appears '
    'as discrete white specks with no spatial correlation. This is characteristic of '
    'salt noise (impulse noise).')
body(doc,
    'Chosen method – Median filter (kernel 5×5): '
    'The median is an order-statistic estimator that is highly robust to outliers; '
    'it replaces each pixel with the median of its neighbourhood, so isolated bright '
    'impulses are eliminated without blurring edges. '
    'A 5×5 kernel handles clusters of up to ~2 adjacent noise pixels.\n'
    'Implementation: reflect-pad the image by 2, extract 5×5 windows via '
    'numpy.lib.stride_tricks.sliding_window_view, then compute np.median across '
    'axes (−2, −1).')

heading(doc, '2.2  Image 2 – Gaussian Noise → 7×7 Gaussian Filter (σ=2.0)', level=2)
body(doc,
    'Noise analysis: Image 2 (a dog) shows uniformly distributed fine-grained '
    'intensity variations across all regions, including flat backgrounds. The image '
    'standard deviation is σ≈41.6 DN, and the noise exhibits no spatial pattern or '
    'directionality. This is consistent with additive zero-mean Gaussian noise, '
    'typically caused by thermal noise in camera sensors.')
body(doc,
    'Chosen method – Gaussian spatial filter (7×7, σ=2.0): '
    'For additive zero-mean Gaussian noise, linear averaging reduces the noise '
    'variance by a factor proportional to kernel area. The Gaussian weighting '
    'minimises the spatial-frequency bandwidth product (Heisenberg uncertainty), '
    'making it the optimal linear estimator for Gaussian noise while limiting edge '
    'blurring. A larger kernel (7×7, σ=2.0) is chosen given the high noise level.\n'
    'Implementation: construct the kernel K(x,y) = exp(−(x²+y²)/(2σ²)) / ΣK, '
    'reflect-pad the image, then convolve via sliding_window_view: '
    'output(i,j) = Σ K(x,y)·I(i+x, j+y).')

heading(doc, '2.3  Image 3 – Mixed Noise → Median (3×3) + Frequency-Domain LPF', level=2)
body(doc,
    'Noise analysis: Image 3 (an "ABUNDANCE" sign) exhibits both isolated impulse '
    'pixels (~1,682 extreme pixels) and a quasi-periodic dot pattern visible as '
    'concentric rings in the Fourier spectrum. This indicates mixed noise comprising '
    'salt-and-pepper components and periodic / structured noise arising from '
    'imaging artifacts.')
body(doc,
    'Chosen method – Two-stage approach:\n'
    '  Stage 1 (3×3 Median filter): removes isolated impulse pixels first, '
    'preventing them from corrupting the frequency-domain analysis.\n'
    '  Stage 2 (Frequency-domain Gaussian LPF): suppresses periodic and '
    'high-frequency components globally. The algorithm computes the 2D DFT '
    'F = FFT2(I), centres the spectrum, multiplies by the Gaussian envelope '
    'H(u,v) = exp(−D(u,v)²/(2D₀²)) with D₀ = 0.25·min(H,W), then recovers '
    'the image via the inverse DFT. The Gaussian mask provides a smooth '
    'roll-off in the frequency domain, avoiding ringing artefacts that '
    'ideal low-pass filters would introduce.')

# ── Section 3 ─────────────────────────────────────────────────────────────
heading(doc, '3  Experiment Results and Analysis')

for fig, cap in [
    ('fig_image1.png',
     'Figure 1. Image 1 (van): original, Fourier spectrum, denoised output, '
     'and denoised spectrum. SNR improvement: +10.6 dB.'),
    ('fig_image2.png',
     'Figure 2. Image 2 (dog): original, Fourier spectrum, denoised output, '
     'and denoised spectrum. SNR improvement: +20.6 dB.'),
    ('fig_image3.png',
     'Figure 3. Image 3 (sign): original, Fourier spectrum, denoised output, '
     'and denoised spectrum. SNR improvement: +13.0 dB.'),
]:
    add_image(doc, fig, caption=cap)
    doc.add_paragraph()

body(doc,
    'Image 1 analysis: The 5×5 median filter cleanly eliminates the salt noise '
    'while preserving the sharp edges of the vehicle and the cobblestone texture. '
    'The SNR improvement of 10.6 dB reflects effective suppression of the high-intensity '
    'outliers. Slight residual softening in very dense noise clusters is the only limitation.')
body(doc,
    'Image 2 analysis: The Gaussian filter reduces the high-frequency noise energy '
    'significantly (SNR +20.6 dB). The frequency spectrum confirms that '
    'high-frequency components are attenuated. Some blurring of fine fur details '
    'is inevitable; a larger kernel trades sharpness for noise suppression.')
body(doc,
    'Image 3 analysis: The two-stage approach yields SNR +13.0 dB and clearly '
    'reveals the sign text and decorative elements. The Fourier spectrum comparison '
    'confirms the removal of periodic high-frequency components. The remaining image '
    'retains good contrast and legibility of the "ABUNDANCE" lettering.')

# ── Section 4 ─────────────────────────────────────────────────────────────
heading(doc, '4  Summary')
body(doc,
    'The primary challenge was implementing efficient image-processing primitives '
    'without library support. The solution leverages numpy.lib.stride_tricks.'
    'sliding_window_view to extract local patches in a fully vectorised manner, '
    'avoiding slow Python loops for the 224×224 images.')
body(doc,
    'Key knowledge gained:\n'
    '  1. Different noise types require fundamentally different filters: impulse '
    'noise → non-linear order-statistics (median); Gaussian noise → linear Gaussian '
    'averaging; periodic noise → frequency-domain suppression.\n'
    '  2. Frequency-domain analysis (Fourier spectrum) provides a powerful diagnostic '
    'tool to distinguish noise types—impulse noise appears as broad spectral elevation '
    'while periodic noise appears as bright spots at specific frequencies.\n'
    '  3. A two-stage pipeline (spatial then frequency domain) can address mixed noise '
    'more effectively than any single filter.\n'
    '  4. Filter parameter selection (kernel size, σ, D₀) involves a trade-off between '
    'noise suppression and preservation of image detail.')

doc.save('report_project1.docx')
print('Saved report_project1.docx')
