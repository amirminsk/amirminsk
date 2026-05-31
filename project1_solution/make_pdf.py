from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os

PAGE_W, PAGE_H = A4
MARGIN = 2.5 * cm

doc = SimpleDocTemplate(
    'report_project1.pdf', pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
)

title = ParagraphStyle('t',  fontSize=16, alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold')
sub   = ParagraphStyle('s',  fontSize=12, alignment=TA_CENTER, spaceAfter=4)
h1    = ParagraphStyle('h1', fontSize=13, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=5)
h2    = ParagraphStyle('h2', fontSize=11, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)
body  = ParagraphStyle('b',  fontSize=10, leading=15, spaceAfter=6)
cap   = ParagraphStyle('c',  fontSize=9,  alignment=TA_CENTER, textColor=colors.grey, spaceAfter=8)

W = PAGE_W - 2 * MARGIN
story = []

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

story.append(Paragraph('1  Project Content', h1))
story.append(Paragraph(
    'In this project we are given three noisy images and we need to figure out what '
    'type of noise is in each one and then remove it. We can\'t use the built-in '
    'processing functions from cv2, so I implemented everything myself using loops '
    'and basic math.',
    body))

story.append(Paragraph('2  Method Description', h1))

story.append(Paragraph('Image 1 – Median Filter', h2))
story.append(Paragraph(
    'Looking at image 1 I can clearly see white dots randomly scattered across the '
    'image. This is salt noise where some pixels get replaced with a very bright value.',
    body))
story.append(Paragraph(
    'I used a median filter with a 5×5 window. For each pixel I collect all 25 values '
    'in the surrounding area, sort them, and take the middle one. I first tried 3×3 '
    'but some noise clusters were still visible, so I increased it to 5×5 and that '
    'worked better. The median is good here because one or two bright outliers '
    'don\'t affect the result much.',
    body))

story.append(Paragraph('Image 2 – Gaussian Filter', h2))
story.append(Paragraph(
    'Image 2 has fine random noise all over it, not isolated dots like image 1. '
    'The whole image looks grainy. This is Gaussian noise which comes from the camera sensor.',
    body))
story.append(Paragraph(
    'I built a 5×5 Gaussian kernel using the formula: '
    'w(x,y) = exp(-(x²+y²) / (2σ²)) then normalized it so all weights add up to 1. '
    'I used σ=1.5. Then I applied it by doing a weighted sum over each pixel\'s '
    'neighbourhood. The result is a bit blurry but the noise is gone.',
    body))

story.append(Paragraph('Image 3 – Frequency Domain Filter', h2))
story.append(Paragraph(
    'Image 3 has a repeating dot pattern which looked like periodic noise to me. '
    'I learned in class that periodic noise shows up as bright spots in the frequency '
    'spectrum, so the best way to remove it is to filter in the frequency domain.',
    body))
story.append(Paragraph(
    'I took the 2D FFT of the image, shifted it so the low frequencies are in the '
    'centre, then applied a Gaussian low-pass mask. The mask reduces the high '
    'frequencies where the noise lives. Then I did the inverse FFT to get back '
    'the filtered image.',
    body))

story.append(Paragraph('3  Experiment Results and Analysis', h1))

for fig, captext in [
    ('fig_image1.png', 'Figure 1. Image 1 before and after median filter (5×5).'),
    ('fig_image2.png', 'Figure 2. Image 2 before and after Gaussian filter (5×5, σ=1.5).'),
    ('fig_image3.png', 'Figure 3. Image 3 before and after frequency domain low-pass filter.'),
]:
    if os.path.exists(fig):
        story.append(RLImage(fig, width=W, height=W*0.28))
    story.append(Paragraph(captext, cap))

story.append(Paragraph(
    'Image 1: the white dots are completely removed and the van and background '
    'look clean. Edges are still sharp which is what I expected from median filtering.',
    body))
story.append(Paragraph(
    'Image 2: the noise is reduced but the image is a bit soft. This is the tradeoff '
    'with Gaussian filtering – it smooths out noise but also blurs edges slightly. '
    'Using a smaller kernel would keep more detail but also more noise.',
    body))
story.append(Paragraph(
    'Image 3: the repeating dot pattern is mostly gone and the text is readable. '
    'I experimented with different cutoff values and 40 gave the best balance between '
    'removing the noise and keeping the image sharp.',
    body))

story.append(Paragraph('4  Summary', h1))
story.append(Paragraph(
    'I found the frequency domain filter the most interesting part. It was helpful to '
    'see how different types of noise look in the Fourier spectrum. The main difficulty '
    'was writing the median filter loop efficiently enough since 224×224 with a 5×5 '
    'window is a lot of iterations.',
    body))
story.append(Paragraph(
    'The key thing I learned is that you need to choose the right filter for the noise '
    'type – median for salt noise, Gaussian for random noise, and frequency domain for '
    'periodic patterns.',
    body))

doc.build(story)
print('saved report_project1.pdf')
