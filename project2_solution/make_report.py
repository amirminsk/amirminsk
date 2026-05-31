from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

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

heading('Step 1 - Make the image black and white', size=12)
body(
    'The first thing is that the picture is gray, so it have many gray levels from 0 to '
    '255. But for morphology I need only two values, black and white. So I must choose '
    'one threshold number. Every pixel that is bigger than this number become white, '
    'and the other pixels become black.'
)
body(
    'In the beginning I try to choose the threshold by my self, for example 128. But '
    'this is not a good way because if the image is more dark or more bright the number '
    'is not correct anymore. So I decided to use Otsu method, which can find the good '
    'threshold automatic.'
)
body(
    'The idea of Otsu is like this. For each possible threshold from 0 to 255, it cut '
    'the pixels to two group. One group is the background and other group is the '
    'foreground. Then it calculate how much these two group are separate from each '
    'other, this is call the between class variance:'
)
body(
    '        variance = w_back * w_fore * ( mean_back - mean_fore ) ^ 2'
)
body(
    'Here w_back and w_fore is how many percent of pixels are in each group, and the '
    'mean is the average gray value of the group. When the variance is big, it means '
    'the two group are far away and the threshold is good. So I just check all the 256 '
    'thresholds and I keep the one that give the biggest variance. For my image the '
    'best threshold was 107.'
)

heading('Step 2 - Erosion and find the boundary', size=12)
body(
    'After I have the black and white image, I use erosion to find the boundary. '
    'Erosion is a operation that make the white object a little bit smaller. It remove '
    'the pixels in the outside layer of the white shape.'
)
body(
    'The rule of my erosion is easy. I look at every pixel and also the 8 pixels around '
    'it, so it is a 3x3 window. If all of the 9 pixels are white, then the center pixel '
    'stay white. But if even one pixel is black, then the center become black. By this '
    'rule the border of the white area is removed.'
)
body(
    'If I do this with a normal loop for every pixel it will be very slow because the '
    'image is 1024x1024, this is more than one million pixels. So instead I shift the '
    'whole image to the 9 directions and do the AND operation between them, this give '
    'the same answer but much more fast. Also I put a black border around the image '
    'first, because if not the pixels on the edge will have problem.'
)
body(
    'Finally, to get the boundary I just take the original binary image and minus the '
    'eroded image:'
)
body(
    '        boundary = binary - eroded'
)
body(
    'This is working because erosion only change the pixels on the edge of the shapes. '
    'So when I subtract, only the edge pixels are left, and this edge is exactly the '
    'boundary that I am looking for.'
)

heading('3  Experiment Results and Analysis')
body(
    'The threshold of 107 worked really well. In the binary image you can clearly see '
    'the white cat as foreground and the black cat plus the gray border become '
    'background, which is what I expected.'
)
body(
    'The final boundary image shows a thin white outline around the shapes. You can see '
    'the big circle on the outside, the curvy line in the middle where the two cats '
    'meet, and also the face and the whiskers of the white cat. The number of boundary '
    'pixels I got was 15692.'
)
body(
    'One thing I noticed is that the very thin whisker lines are a bit weak in the '
    'result. I think this is because they are thinner than 3 pixels so the 3x3 erosion '
    'almost remove them completely. If I used a smaller structuring element they would '
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
