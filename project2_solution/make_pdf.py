"""Generate report_project2.pdf"""
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
    'report_project2.pdf', pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
)

title = ParagraphStyle('t',  fontSize=16, alignment=TA_CENTER, spaceAfter=4,  fontName='Helvetica-Bold')
sub   = ParagraphStyle('s',  fontSize=12, alignment=TA_CENTER, spaceAfter=4)
h1    = ParagraphStyle('h1', fontSize=13, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=5)
h2    = ParagraphStyle('h2', fontSize=11, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)
body  = ParagraphStyle('b',  fontSize=10, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
cap   = ParagraphStyle('c',  fontSize=9,  alignment=TA_CENTER, textColor=colors.grey, spaceAfter=8)
code  = ParagraphStyle('k',  fontSize=9,  fontName='Courier', leading=13, spaceAfter=6, leftIndent=1*cm)

W = PAGE_W - 2 * MARGIN
story = []

# cover
for text, sty in [
    ('Harbin Institute of Technology (Shenzhen)', title),
    ('Project Report', title),
    ('Image Processing (COMP5033)', sub),
    ('2025–2026 Spring Semester', sub),
    ('Teacher: Prof. Weizheng Zhang', sub),
]:
    story.append(Paragraph(text, sty))
story.append(Spacer(1, 0.6*cm))

tbl = Table(
    [['Project No.:', '2', 'Student Name:', '[YOUR NAME]'],
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
    'In this project we are given a 1024×1024 grayscale image (a yin-yang design with '
    'two cats) and we need to find its boundary using morphological image processing. '
    'The main steps are: first convert the grayscale image into a binary (black and white) '
    'image, then use morphological erosion to extract the boundary.',
    body))

# section 2
story.append(Paragraph('2  Method Description', h2))

story.append(Paragraph('2.1  Step 1: Binarization using Otsu\'s Method', h2))
story.append(Paragraph(
    'To turn the grayscale image into binary I used <b>Otsu\'s thresholding</b>. '
    'The idea is to automatically find the best threshold value T that separates the '
    'image into foreground (bright) and background (dark) pixels.',
    body))
story.append(Paragraph(
    'Otsu\'s method tries every possible threshold from 0 to 255 and picks the one that '
    'maximises the variance between the two groups of pixels (foreground and background). '
    'A higher inter-class variance means the two groups are more separated.',
    body))
story.append(Paragraph(
    'Formula:  σ²_between = w0 × w1 × (mean0 − mean1)²\n'
    'where w0 and w1 are the proportions of pixels in each group.',
    code))
story.append(Paragraph(
    'For Figure_P2.jpg the algorithm found <b>T = 107</b>. Pixels brighter than 107 '
    'become white (1), the rest become black (0).',
    body))

story.append(Paragraph('2.2  Step 2: Boundary Extraction using Erosion', h2))
story.append(Paragraph(
    'Morphological <b>erosion</b> shrinks all white regions inward. For each pixel, '
    'I look at its 3×3 neighbourhood: if all 9 pixels are white, the pixel stays white; '
    'otherwise it becomes black.',
    body))
story.append(Paragraph(
    'Once I have the eroded image I can find the boundary by subtracting:',
    body))
story.append(Paragraph(
    'boundary = original_binary − eroded_binary',
    code))
story.append(Paragraph(
    'This leaves only the pixels that were removed by erosion – which are exactly the '
    'pixels on the edge of each white region.',
    body))
story.append(Paragraph(
    'I also do the same for the black regions (by inverting the binary image) to get '
    'the boundaries of the dark cat as well, then combine both results.',
    body))

# section 3
story.append(Paragraph('3  Experiment Results and Analysis', h1))

fig = 'fig_p2_comparison.png'
if os.path.exists(fig):
    story.append(RLImage(fig, width=W, height=W * 0.36))
story.append(Paragraph(
    'Figure 1. Left: original grayscale image. Centre: binary image (T=107). '
    'Right: boundary output (Output_P2.jpg).',
    cap))

story.append(Paragraph(
    '<b>Binarization result:</b> Otsu\'s threshold of 107 works well for this image. '
    'The white cat body is correctly identified as foreground and the black cat as '
    'background. The gray border around the circle also becomes background.',
    body))
story.append(Paragraph(
    '<b>Boundary result:</b> The output shows a thin white line tracing all edges of '
    'the image – the outer circle, the S-curve between the two cats, the cat faces, '
    'whiskers, and tails. The total number of boundary pixels is 27,460.',
    body))
story.append(Paragraph(
    '<b>Limitation:</b> Very thin lines like the whiskers (thinner than 3 pixels) can '
    'disappear after erosion because the 3×3 neighbourhood removes them completely. '
    'A smaller structuring element would help in that case.',
    body))

# section 4
story.append(Paragraph('4  Summary', h1))
story.append(Paragraph(
    'The hardest part was implementing Otsu\'s thresholding from scratch. I had to '
    'carefully compute the inter-class variance for each threshold value using the '
    'histogram. Once the binary image was correct, the erosion step was straightforward.',
    body))
story.append(Paragraph(
    'From this project I learned: (1) how to automatically binarize an image without '
    'manually choosing a threshold; (2) how erosion works and how subtracting an eroded '
    'image from the original gives the boundary; (3) that morphological operations are '
    'simple but very effective for shape analysis tasks.',
    body))

doc.build(story)
print('Saved report_project2.pdf')
