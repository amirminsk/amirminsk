"""Generate report_project1.pdf"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

PAGE_W, PAGE_H = A4
MARGIN = 2.5 * cm

doc = SimpleDocTemplate(
    'report_project1.pdf', pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
)

title  = ParagraphStyle('t',  fontSize=16, alignment=TA_CENTER, spaceAfter=4,  fontName='Helvetica-Bold')
sub    = ParagraphStyle('s',  fontSize=12, alignment=TA_CENTER, spaceAfter=4)
h1     = ParagraphStyle('h1', fontSize=13, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=5)
h2     = ParagraphStyle('h2', fontSize=11, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)
body   = ParagraphStyle('b',  fontSize=10, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
cap    = ParagraphStyle('c',  fontSize=9,  alignment=TA_CENTER, textColor=colors.grey, spaceAfter=8)

W = PAGE_W - 2 * MARGIN
story = []

# cover
for text, sty in [
    ('Harbin Institute of Technology (Shenzhen)', title),
    ('Project Report', title),
    ('Image Processing (COMP5033)', sub),
    ('2025–2026 Spring Semester', sub),
    ('Lecturer: Prof. Weizheng Zhang', sub),
]:
    story.append(Paragraph(text, sty))
story.append(Spacer(1, 0.6*cm))

tbl = Table(
    [['Project No.:', '1', 'Student Name:', '[YOUR NAME]'],
     ['Student ID:',  '[YOUR ID]', 'Date of Submission:', '2026-05-30']],
    colWidths=[3*cm, 4*cm, 4*cm, 5*cm]
)
tbl.setStyle(TableStyle([
    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
    ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
    ('PADDING', (0,0), (-1,-1), 5),
]))
story += [tbl, Spacer(1, 0.4*cm), HRFlowable(width='100%'), Spacer(1, 0.3*cm)]

# section 1
story.append(Paragraph('1  Project Content', h1))
story.append(Paragraph(
    'In this project we are given three 224×224 grayscale images that have been corrupted '
    'by different types of noise. The goal is to first figure out what kind of noise is in '
    'each image, and then write code to remove it. We are not allowed to use built-in '
    'denoising functions from OpenCV. Instead we implement the filters manually using Python '
    'and NumPy.',
    body))

# section 2
story.append(Paragraph('2  Method Description', h1))

story.append(Paragraph('2.1  Image 1 – Median Filter', h2))
story.append(Paragraph(
    '<b>Noise type:</b> Looking at Image 1 (a van) I can see scattered white dots randomly '
    'placed across the image. This is called <i>salt noise</i> – a type of impulse noise '
    'where some pixels are randomly replaced by a very bright value.',
    body))
story.append(Paragraph(
    '<b>Method:</b> I used a <b>5×5 median filter</b>. For each pixel, I look at the 5×5 '
    'neighbourhood around it and replace the pixel with the median value of that window. '
    'The median works well here because isolated bright outliers get pushed out by the '
    'surrounding normal pixels without blurring edges.',
    body))

story.append(Paragraph('2.2  Image 2 – Gaussian Filter', h2))
story.append(Paragraph(
    '<b>Noise type:</b> Image 2 (a dog) has fine-grained random noise spread uniformly '
    'all over the image. There are no obvious isolated dots – the noise looks like small '
    'random fluctuations everywhere. This is <i>Gaussian noise</i>, which is common in '
    'camera sensors.',
    body))
story.append(Paragraph(
    '<b>Method:</b> I used a <b>5×5 Gaussian filter</b> with σ=1.5. This filter takes a '
    'weighted average of each pixel\'s neighbourhood, giving more weight to nearby pixels '
    'and less to far ones. Since Gaussian noise is zero-mean and random, averaging '
    'neighbouring pixels reduces it.',
    body))
story.append(Paragraph(
    'The kernel weights are: K(x,y) = exp(−(x²+y²) / (2σ²)) normalised so all weights '
    'sum to 1.',
    body))

story.append(Paragraph('2.3  Image 3 – Frequency Domain Low-Pass Filter', h2))
story.append(Paragraph(
    '<b>Noise type:</b> Image 3 (an ABUNDANCE sign) has a repeating dot pattern that '
    'suggests <i>periodic noise</i>. Unlike random noise, periodic patterns show up as '
    'bright spots in the frequency spectrum.',
    body))
story.append(Paragraph(
    '<b>Method:</b> I used a <b>frequency domain Gaussian low-pass filter</b>. '
    'The steps are: (1) take the 2D Fourier transform (FFT) of the image; '
    '(2) shift the spectrum so zero-frequency is at the centre; '
    '(3) multiply by a Gaussian mask that keeps low frequencies and removes high ones; '
    '(4) inverse FFT to get back the filtered image. '
    'High-frequency noise and periodic patterns are suppressed this way.',
    body))

# section 3
story.append(Paragraph('3  Experiment Results and Analysis', h1))

for fig, captext in [
    ('fig_image1.png', 'Figure 1. Image 1: original (left), denoised with 5×5 median filter (right).'),
    ('fig_image2.png', 'Figure 2. Image 2: original (left), denoised with 5×5 Gaussian filter σ=1.5 (right).'),
    ('fig_image3.png', 'Figure 3. Image 3: original (left), denoised with frequency-domain LPF (right).'),
]:
    if os.path.exists(fig):
        story.append(RLImage(fig, width=W, height=W * 0.28))
    story.append(Paragraph(captext, cap))

story.append(Paragraph(
    '<b>Image 1:</b> The median filter clearly removes the white dot noise. Edges on the '
    'van are well preserved because the median is not affected by a few outlier values.',
    body))
story.append(Paragraph(
    '<b>Image 2:</b> The Gaussian filter reduces the fine-grained noise. The image becomes '
    'slightly blurry because Gaussian averaging also smooths detail, but the overall '
    'structure is clear. Using a larger sigma would remove more noise but blur more.',
    body))
story.append(Paragraph(
    '<b>Image 3:</b> The frequency-domain filter removes the repeating dot pattern well. '
    'Text edges are preserved because the low-pass mask keeps the low-frequency content '
    'that carries the main structure of the image.',
    body))

# section 4
story.append(Paragraph('4  Summary', h1))
story.append(Paragraph(
    'The main difficulty was implementing the filters from scratch. Writing the median '
    'filter loop helped me understand how a sliding window works. The most interesting '
    'part was the frequency domain filter – it was helpful to see visually how periodic '
    'noise shows up as spots in the Fourier spectrum and how a mask can remove them.',
    body))
story.append(Paragraph(
    'Key lessons: different types of noise need different filters. Impulse noise needs '
    'a non-linear filter (median). Gaussian noise works well with a linear averaging '
    'filter. Periodic noise is best handled in the frequency domain.',
    body))

doc.build(story)
print('Saved report_project1.pdf')
