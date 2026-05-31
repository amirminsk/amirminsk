from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

doc = Document()

for text, size, bold, center in [
    ('Harbin Institute of Technology (Shenzhen)', 14, True, True),
    ('Project Report', 16, True, True),
    ('Image Processing (COMP5033)', 12, False, True),
    ('2025–2026 Spring Semester', 12, False, True),
    ('Teacher: Prof. Weizheng Zhang', 12, False, True),
]:
    p = doc.add_paragraph()
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)

doc.add_paragraph()

table = doc.add_table(rows=2, cols=4)
table.style = 'Table Grid'
table.rows[0].cells[0].text = 'Project No.:'
table.rows[0].cells[1].text = '2'
table.rows[0].cells[2].text = 'Student Name:'
table.rows[0].cells[3].text = '[YOUR NAME]'
table.rows[1].cells[0].text = 'Student ID:'
table.rows[1].cells[1].text = '[YOUR ID]'
table.rows[1].cells[2].text = 'Date of Submission:'
table.rows[1].cells[3].text = '2026-05-30'

doc.add_paragraph()

def heading(text, size=13):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(size)

def body(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    p.runs[0].font.size = Pt(11)

def add_img(path, caption, width=6):
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(width))
    p = doc.add_paragraph(caption)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].italic = True
    p.runs[0].font.size = Pt(10)

heading('1  Project Content')
body(
    'The goal is to find the boundary of objects in a binary image. The input is '
    'Figure_P2.jpg which is a 1024×1024 grayscale image. First I need to binarize '
    'it and then use morphological operations to get the boundary.'
)

heading('2  Method Description')

heading('Step 1: Binarization', size=11)
body(
    'I used Otsu\'s method to find the threshold automatically instead of guessing '
    'a value manually. The idea is to try every possible threshold from 0 to 255 '
    'and pick the one that best separates the image into two groups.'
)
body(
    'For each threshold t I calculate the between-class variance:\n'
    '     variance = w0 * w1 * (mean0 - mean1)^2\n'
    'where w0 and w1 are the fractions of pixels in each group. The threshold '
    'with the highest variance is the best one. For this image it came out to T=107.'
)

heading('Step 2: Morphological Erosion', size=11)
body(
    'Erosion shrinks the white regions by removing the outermost pixels. '
    'For each pixel, I check its 3×3 neighbourhood – if all 9 pixels are white '
    'the pixel stays white, otherwise it becomes black.'
)
body(
    'To find the boundary I subtract the eroded image from the original:\n'
    '     boundary = original - eroded\n'
    'This leaves only the pixels that were on the edge. I did this for both the '
    'white regions and the black regions (by inverting) and then combined them '
    'to get all edges.'
)

heading('3  Experiment Results and Analysis')
add_img('fig_p2_comparison.png', 'Figure 1. Original image, binary image after thresholding, and boundary output.')
doc.add_paragraph()

body(
    'The threshold of 107 worked well – the binary image clearly separates the '
    'white cat from the black cat and the gray background. The gray border around '
    'the image became background which makes sense.'
)
body(
    'The boundary image shows a thin line around all the shapes. You can see the '
    'outer circle, the curve between the two cats, the whiskers and the face details. '
    'Total boundary pixels were 27,460.'
)
body(
    'One problem I noticed is that very thin lines like the whiskers partly disappear '
    'after erosion because the 3×3 window is too big for them.'
)

heading('4  Summary')
body(
    'Implementing Otsu\'s method from scratch was the hardest part. I had to keep '
    'track of the running mean and weight for each threshold which was a bit tricky '
    'to get right.'
)
body(
    'I learned that erosion is a simple but effective way to find boundaries – you '
    'just subtract what was eroded and you get the edge. I also learned that Otsu\'s '
    'method is really useful because you don\'t need to manually choose the threshold.'
)

doc.save('report_project2.docx')
print('saved report_project2.docx')
