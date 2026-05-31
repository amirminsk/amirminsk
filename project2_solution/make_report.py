from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

doc = Document()

for text, size, bold in [
    ('Harbin Institute of Technology (Shenzhen)', 14, True),
    ('Project Report', 16, True),
    ('Image Processing (COMP5033)', 12, False),
    ('2025–2026 Spring Semester', 12, False),
    ('Teacher: Prof. Weizheng Zhang', 12, False),
]:
    p = doc.add_paragraph()
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
    'For this project we were given a binary image and we have to find its boundary '
    'using morphological processing. The image is Figure_P2.jpg and it is 1024x1024 in '
    'size. It is actually a yin yang picture made of two cats, one white and one black. '
    'The task says I need to binarize the image first and then find the boundary. '
    'I am not allowed to use the cv2 functions for the processing so I wrote the '
    'threshold and the erosion myself, and only used cv2 to read and save the image.'
)

heading('2  Method Description')

heading('Step 1 - Making it black and white', size=12)
body(
    'The original image is grayscale so before doing morphology I had to turn it into '
    'a proper binary image (only 0 and 1). At first I just picked a threshold like 128 '
    'by hand but that did not feel right because it depends on the image. So I used '
    'Otsu method which finds the threshold automatically.'
)
body(
    'The way Otsu works is it tries every threshold from 0 to 255 and for each one it '
    'splits the pixels into two groups (background and foreground). Then it calculates '
    'the variance between the two groups using this formula:'
)
body(
    '        variance = back_weight * fore_weight * (back_mean - fore_mean)^2'
)
body(
    'The best threshold is the one that gives the biggest variance, because that means '
    'the two groups are the most separated. I looped through all 256 values and kept '
    'the best one. For this image the threshold came out to 107. After that, every '
    'pixel brighter than 107 becomes white (1) and the rest become black (0).'
)

heading('Step 2 - Erosion and finding the boundary', size=12)
body(
    'To get the boundary I used erosion. Erosion makes the white shapes a little bit '
    'smaller by eating away the outside layer of pixels. The rule I used is: a pixel '
    'stays white only if all the pixels in its 3x3 area are also white, otherwise it '
    'turns black.'
)
body(
    'Instead of looping over every pixel one by one (which would be really slow for a '
    '1024x1024 image), I did it by shifting the whole image in the 9 directions and '
    'doing an AND between them. I also added a black border around the image first so '
    'the edge pixels would not cause problems.'
)
body(
    'Once I had the eroded image, the boundary is just the difference between the '
    'original binary image and the eroded one:'
)
body(
    '        boundary = binary - eroded'
)
body(
    'This makes sense because the only pixels that changed are the ones on the edge of '
    'the shapes, which is exactly the boundary I want.'
)

heading('3  Experiment Results and Analysis')
add_img('fig_p2_comparison.png',
        'Figure 1. From left to right: the original image, the binary image after '
        'Otsu thresholding, and the boundary I got at the end.')
doc.add_paragraph()
body(
    'The threshold of 107 worked really well. In the binary image you can clearly see '
    'the white cat as foreground and the black cat plus the gray border become '
    'background, which is what I expected.'
)
body(
    'The boundary image shows a thin white outline around the shapes. You can see the '
    'big circle, the curvy line in the middle where the two cats meet, and also the '
    'face and whiskers of the white cat. The number of boundary pixels I got was 15692.'
)
body(
    'One thing I noticed is that the very thin whisker lines are a bit weak in the '
    'result. I think this is because they are thinner than 3 pixels so the 3x3 erosion '
    'almost removes them completely. If I used a smaller structuring element they would '
    'show up better, but 3x3 is the normal choice so I kept it.'
)

heading('4  Summary')
body(
    'The hardest part for me was writing the Otsu threshold by myself. Keeping track of '
    'the running weight and the running mean for each threshold value was a little '
    'confusing at first and I had to test it a few times before the number looked '
    'correct.'
)
body(
    'From this project I learned how binarization works and why automatic thresholding '
    'is better than just guessing a value. I also understood erosion much better, '
    'especially the trick that subtracting the eroded image from the original gives you '
    'the boundary directly. Overall it was a good exercise to see how simple '
    'morphological operations can do something useful like edge finding.'
)

doc.save('report_project2.docx')
print('saved report_project2.docx')
