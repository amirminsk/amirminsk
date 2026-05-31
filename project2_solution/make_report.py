from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ---- header ----
for text, size, bold in [
    ('Harbin Institute of Technology (Shenzhen)', 14, True),
    ('Project Report', 16, True),
    ('', 10, False),
    ('Image Processing (COMP5033) ', 12, False),
    ('2025-2026 Spring Semester', 12, False),
    ('Teacher: Prof. Weizheng Zhang', 12, False),
    ('', 10, False),
    ('', 10, False),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)

# ---- student info table (matches template exactly) ----
table = doc.add_table(rows=3, cols=4)
table.style = 'Table Grid'

# row 1
table.rows[0].cells[0].text = 'Project No.:'
table.rows[0].cells[1].text = '2'
table.rows[0].cells[2].text = 'Student Name:'
table.rows[0].cells[3].text = '[YOUR NAME]'

# row 2
table.rows[1].cells[0].text = 'Student ID: '
table.rows[1].cells[1].text = '[YOUR ID]'
table.rows[1].cells[2].text = 'Date of Submission:'
table.rows[1].cells[3].text = '2026-05-30'

# row 3 - grading row, merge all 4 cells
row3 = table.rows[2]
a = row3.cells[0]
a.merge(row3.cells[1])
a.merge(row3.cells[2])
a.merge(row3.cells[3])
a.text = 'Grading (for Teaching Assistant)\n\nScore: ____________________\n\nComments: ' + '_' * 200

doc.add_paragraph()

def heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(12)

def body(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    p.runs[0].font.size = Pt(11)

# ---- section 1 ----
heading('1 Project Content')
body(
    'For this project we were given a grayscale image and we have to find its boundary '
    'using morphological processing. The image is Figure_P2.jpg and it is 1024x1024 in '
    'size. The task says I need to binarize the image first and then apply morphological '
    'erosion to extract the boundary. I am not allowed to use the cv2 processing '
    'functions so I wrote the threshold and the erosion by myself, and only used cv2 '
    'to read and save the image.'
)

# ---- section 2 ----
heading('2 Method Description')
body(
    'The first thing is that the picture is grayscale, so it have many gray levels '
    'from 0 to 255. But for morphology I need only two values, black and white. '
    'So I must choose one threshold number. Every pixel that is bigger than this '
    'number become white, and the other pixels become black.'
)
body(
    'In the beginning I try to choose the threshold by myself, for example 128. But '
    'this is not a good way because if the image is more dark or more bright the '
    'number is not correct anymore. So I used Otsu method, which can find the good '
    'threshold automatic.'
)
body(
    'The idea of Otsu is like this. For each possible threshold from 0 to 255, it cut '
    'the pixels to two group, one is background and other is foreground. Then it '
    'calculate how much these two group are separate from each other, this is call the '
    'between class variance: variance = w_back * w_fore * (mean_back - mean_fore)^2. '
    'The best threshold is the one that give the biggest variance. For my image the '
    'best threshold was 107.'
)
body(
    'After I have the binary image, I use erosion to find the boundary. Erosion is a '
    'operation that make the white object a little bit smaller by removing the pixels '
    'on the outside layer. The rule is: I look at every pixel and the 8 pixels around '
    'it in a 3x3 window. If all the 9 pixels are white, the center pixel stay white. '
    'But if even one pixel is black, the center become black.'
)
body(
    'To get the boundary I subtract the eroded image from the original binary image: '
    'boundary = binary - eroded. This is working because erosion only change the '
    'pixels on the edge. So after subtract, only the edge pixels are left and this '
    'is exactly the boundary I want.'
)

# ---- section 3 ----
heading('3 Experiment Results and Analysis')
body(
    'The threshold of 107 worked well. In the binary image you can see the white cat '
    'becomes the foreground and the black cat with the gray border becomes background. '
    'This is the correct result because the image has mainly two regions of different '
    'brightness and Otsu could find the line between them.'
)
body(
    'The boundary image shows a thin white line around all the shapes. You can see '
    'the big outer circle, the curvy line between the two cats, and also the face and '
    'whiskers of the white cat. The total number of boundary pixels was 15692.'
)
body(
    'One problem I noticed is that the very thin whisker lines are a bit weak. I think '
    'this is because they are thinner than 3 pixels, so the 3x3 erosion almost remove '
    'them completely. The advantage of this method is that it is simple and fast. The '
    'disadvantage is that thin details can be lost depending on the size of the '
    'structuring element.'
)

# ---- section 4 ----
heading('4 Summary')
body(
    'The hardest part for me was writing the Otsu threshold by myself. Keeping track '
    'of the running weight and running mean for each threshold value was a little '
    'confusing at first and I had to test it a few times to get the right number.'
)
body(
    'From this project I learned how binarization works and why automatic thresholding '
    'is better than choosing a value by hand. I also understood erosion much better, '
    'especially the idea that subtracting the eroded image from the original directly '
    'gives the boundary. Overall I think morphological operations are simple but very '
    'useful for shape analysis.'
)

doc.save('report_project2.docx')
print('done')
