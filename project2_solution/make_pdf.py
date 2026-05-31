from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    Table, TableStyle, HRFlowable,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

PAGE_W, PAGE_H = A4
MARGIN = 2.5 * cm

doc = SimpleDocTemplate(
    'report_project2.pdf', pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
)

title = ParagraphStyle('t',  fontSize=16, alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold')
sub   = ParagraphStyle('s',  fontSize=12, alignment=TA_CENTER, spaceAfter=4)
h1    = ParagraphStyle('h1', fontSize=13, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=5)
h2    = ParagraphStyle('h2', fontSize=11, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)
body  = ParagraphStyle('b',  fontSize=10, leading=15, spaceAfter=6)
cap   = ParagraphStyle('c',  fontSize=9,  alignment=TA_CENTER, textColor=colors.grey, spaceAfter=8)
code  = ParagraphStyle('k',  fontSize=9,  fontName='Courier', leading=13, spaceAfter=6, leftIndent=1*cm)

W = PAGE_W - 2 * MARGIN
story = []

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

story.append(Paragraph('1  Project Content', h1))
story.append(Paragraph(
    'The goal is to find the boundary of objects in a binary image. The input is '
    'Figure_P2.jpg which is a 1024×1024 grayscale image. First I need to binarize '
    'it and then use morphological operations to get the boundary.',
    body))

story.append(Paragraph('2  Method Description', h1))

story.append(Paragraph('Step 1: Binarization', h2))
story.append(Paragraph(
    'I used Otsu\'s method to find the threshold automatically instead of guessing '
    'a value manually. The idea is to try every possible threshold from 0 to 255 '
    'and pick the one that best separates the image into two groups.',
    body))
story.append(Paragraph(
    'For each threshold t I calculate the between-class variance:',
    body))
story.append(Paragraph(
    'variance = w0 * w1 * (mean0 - mean1)^2',
    code))
story.append(Paragraph(
    'where w0 and w1 are the fractions of pixels in each group. The threshold '
    'with the highest variance is the best one. For this image it came out to T=107.',
    body))

story.append(Paragraph('Step 2: Morphological Erosion', h2))
story.append(Paragraph(
    'Erosion shrinks the white regions by removing the outermost pixels. '
    'For each pixel, I check its 3×3 neighbourhood – if all 9 pixels are white '
    'the pixel stays white, otherwise it becomes black.',
    body))
story.append(Paragraph(
    'To find the boundary I subtract the eroded image from the original:',
    body))
story.append(Paragraph(
    'boundary = original - eroded',
    code))
story.append(Paragraph(
    'This leaves only the pixels that were on the edge. I did this for both the '
    'white regions and the black regions (by inverting) and then combined them '
    'to get all edges.',
    body))

story.append(Paragraph('3  Experiment Results and Analysis', h1))

fig = 'fig_p2_comparison.png'
if os.path.exists(fig):
    story.append(RLImage(fig, width=W, height=W*0.36))
story.append(Paragraph(
    'Figure 1. Original image, binary image after thresholding, and boundary output.',
    cap))

story.append(Paragraph(
    'The threshold of 107 worked well – the binary image clearly separates the '
    'white cat from the black cat and the gray background. The gray border around '
    'the image became background which makes sense.',
    body))
story.append(Paragraph(
    'The boundary image shows a thin line around all the shapes. You can see the '
    'outer circle, the curve between the two cats, the whiskers and the face details. '
    'Total boundary pixels were 27,460.',
    body))
story.append(Paragraph(
    'One problem I noticed is that very thin lines like the whiskers partly disappear '
    'after erosion because the 3×3 window is too big for them.',
    body))

story.append(Paragraph('4  Summary', h1))
story.append(Paragraph(
    'Implementing Otsu\'s method from scratch was the hardest part. I had to keep '
    'track of the running mean and weight for each threshold which was a bit tricky '
    'to get right.',
    body))
story.append(Paragraph(
    'I learned that erosion is a simple but effective way to find boundaries – you '
    'just subtract what was eroded and you get the edge. I also learned that Otsu\'s '
    'method is really useful because you don\'t need to manually choose the threshold.',
    body))

doc.build(story)
print('saved report_project2.pdf')
