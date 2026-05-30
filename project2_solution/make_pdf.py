"""Generate report_project2.pdf using reportlab."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

PAGE_W, PAGE_H = A4
MARGIN = 2.5 * cm

doc = SimpleDocTemplate(
    'report_project2.pdf',
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN,  bottomMargin=MARGIN,
)

styles = getSampleStyleSheet()
title_style   = ParagraphStyle('title',  fontSize=16, alignment=TA_CENTER, spaceAfter=4,  fontName='Helvetica-Bold')
sub_style     = ParagraphStyle('sub',    fontSize=12, alignment=TA_CENTER, spaceAfter=4)
h1_style      = ParagraphStyle('h1',     fontSize=13, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=4)
h2_style      = ParagraphStyle('h2',     fontSize=11, fontName='Helvetica-Bold', spaceBefore=8,  spaceAfter=4)
body_style    = ParagraphStyle('body',   fontSize=10, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
caption_style = ParagraphStyle('cap',    fontSize=9,  alignment=TA_CENTER, textColor=colors.grey, spaceAfter=8)
code_style    = ParagraphStyle('code',   fontSize=9,  fontName='Courier', leading=13, spaceAfter=6,
                                leftIndent=1*cm, borderColor=colors.lightgrey, borderPadding=4)

story = []

# ── Cover ─────────────────────────────────────────────────────────────────
story += [
    Paragraph('Harbin Institute of Technology (Shenzhen)', title_style),
    Paragraph('Project Report', title_style),
    Spacer(1, 0.4*cm),
    Paragraph('Image Processing (COMP5033)', sub_style),
    Paragraph('2025–2026 Spring Semester', sub_style),
    Paragraph('Teacher: Prof. Weizheng Zhang', sub_style),
    Spacer(1, 0.6*cm),
]

info_table = Table(
    [['Project No.:', '2', 'Student Name:', '[YOUR NAME]'],
     ['Student ID:',  '[YOUR STUDENT ID]', 'Date of Submission:', '2026-05-30']],
    colWidths=[3*cm, 4*cm, 4*cm, 5*cm]
)
info_table.setStyle(TableStyle([
    ('GRID',      (0,0), (-1,-1), 0.5, colors.black),
    ('FONTNAME',  (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE',  (0,0), (-1,-1), 10),
    ('FONTNAME',  (0,0), (0,-1),  'Helvetica-Bold'),
    ('FONTNAME',  (2,0), (2,-1),  'Helvetica-Bold'),
    ('BACKGROUND',(0,0), (-1,-1), colors.whitesmoke),
    ('PADDING',   (0,0), (-1,-1), 5),
]))
story += [info_table, Spacer(1, 0.5*cm), HRFlowable(width='100%'), Spacer(1, 0.3*cm)]

# ── Section 1 ─────────────────────────────────────────────────────────────
story.append(Paragraph('1  Project Content', h1_style))
story.append(Paragraph(
    'This project implements a morphological algorithm to detect the boundaries of all '
    'objects in a binary image. The input is <i>Figure_P2.jpg</i> (1024×1024 grayscale): '
    'a yin-yang design with two interlocking cat silhouettes and a gray background. '
    'The pipeline is: (1) binarize the grayscale image using Otsu\'s automatic '
    'thresholding; (2) extract object boundaries via morphological erosion. All key '
    'processing is implemented with NumPy; cv2 handles only image I/O.',
    body_style))

# ── Section 2 ─────────────────────────────────────────────────────────────
story.append(Paragraph('2  Method Description', h1_style))

story.append(Paragraph('2.1  Binarization – Otsu\'s Method', h2_style))
story.append(Paragraph(
    "Otsu's method (1979) finds the threshold T* that maximises the inter-class variance "
    "between the two pixel classes (foreground / background):",
    body_style))
story.append(Paragraph(
    "σ²_B(t) = w₀(t) · w₁(t) · [μ₀(t) − μ₁(t)]²",
    code_style))
story.append(Paragraph(
    "where w₀, w₁ are class probabilities and μ₀, μ₁ are class mean intensities at "
    "threshold t. T* = argmax_t σ²_B(t).",
    body_style))
story.append(Paragraph(
    '<b>Implementation:</b> '
    '(1) Compute 256-bin histogram. '
    '(2) Scan t from 0 to 255 with running sums for w₀ and cumulative mean. '
    '(3) Derive w₁ = 1−w₀ and μ₁ = (total_mean − cumsum) / w₁. '
    '(4) Track maximum σ²_B. '
    'For Figure_P2.jpg: <b>T* = 107</b>. Pixels &gt; 107 → foreground (1); '
    'pixels ≤ 107 → background (0). Foreground fraction: 60.9%.',
    body_style))

story.append(Paragraph('2.2  Morphological Boundary Extraction', h2_style))
story.append(Paragraph(
    'The <b>inner boundary</b> of binary set A with structuring element B is:',
    body_style))
story.append(Paragraph('β(A) = A − (A ⊖ B)', code_style))
story.append(Paragraph(
    'where ⊖ denotes erosion. Erosion shrinks foreground regions by removing boundary '
    'pixels; subtracting from the original leaves a 1-pixel-wide boundary.',
    body_style))
story.append(Paragraph(
    '<b>Erosion (3×3 square SE):</b> '
    '(1) Zero-pad binary image by 1. '
    '(2) Extract 3×3 sliding windows via <i>sliding_window_view</i> (shape H×W×3×3). '
    '(3) Output pixel = 1 iff ALL 9 window pixels are 1 (<i>np.all</i> over last 2 axes).',
    body_style))
story.append(Paragraph(
    'To capture boundaries of <i>both</i> white and dark regions:',
    body_style))
story.append(Paragraph(
    'boundary_fg = binary − erosion(binary)          [white-cat edges]\n'
    'boundary_bg = (1−binary) − erosion(1−binary)    [dark-cat edges]\n'
    'Output      = clip(boundary_fg + boundary_bg, 0, 1)',
    code_style))

# ── Section 3 ─────────────────────────────────────────────────────────────
story.append(Paragraph('3  Experiment Results and Analysis', h1_style))

available_width = PAGE_W - 2 * MARGIN
fig = 'fig_p2_comparison.png'
if os.path.exists(fig):
    story.append(RLImage(fig, width=available_width, height=available_width * 0.36))
story.append(Paragraph(
    'Figure 1. Left: original grayscale image (Figure_P2.jpg).  '
    'Centre: binary image after Otsu thresholding (T*=107).  '
    'Right: boundary output (Output_P2.jpg).',
    caption_style))

story.append(Paragraph(
    '<b>Binarization:</b> T*=107 cleanly separates the white cat and fine details '
    'from the dark cat body and gray background. Thin whiskers and facial features '
    'are well preserved.',
    body_style))
story.append(Paragraph(
    '<b>Boundary detection:</b> The output contains 27,460 boundary pixels (2.62% of '
    'the image). A continuous, 1-pixel-wide boundary accurately traces: the outer '
    'circular perimeter, the S-shaped dividing curve, both cat silhouettes, whiskers, '
    'ear details, tails, and paw features. No spurious interior edges appear.',
    body_style))
story.append(Paragraph(
    '<b>Limitations:</b> Very thin structures (whisker lines &lt; 3 px wide) may appear '
    'slightly fragmented after 3×3 erosion. A cross-shaped (plus-sign) structuring '
    'element would preserve such fine details better.',
    body_style))

# ── Section 4 ─────────────────────────────────────────────────────────────
story.append(Paragraph('4  Summary', h1_style))
story.append(Paragraph(
    "The main difficulty was correctly binarizing a multi-tone image (gray background + "
    "white + black). Otsu's method elegantly solved this by analytically finding T*=107 "
    "without manual tuning.",
    body_style))
story.append(Paragraph(
    'Key knowledge gained: '
    '(1) Otsu\'s thresholding is an efficient unsupervised binarization technique '
    'computable in a single O(256) scan of the histogram. '
    '(2) Morphological erosion + set subtraction yields precise 1-pixel boundaries '
    'without complex edge operators. '
    '(3) Processing both the binary image and its complement captures all object edges '
    'in a single boundary map. '
    '(4) Structuring element choice (size/shape) controls boundary thickness and '
    'sensitivity to fine structures.',
    body_style))

doc.build(story)
print('Saved report_project2.pdf')
