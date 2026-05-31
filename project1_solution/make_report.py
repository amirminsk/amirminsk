from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

for text, size, bold in [
    ('Harbin Institute of Technology (Shenzhen)', 14, True),
    ('Project Report', 16, True),
    ('', 10, False),
    ('Image Processing (COMP5033) ', 12, False),
    ('2025-2026 Spring Semester', 12, False),
    ('Lecturer: Prof. Weizheng Zhang', 12, False),
    ('', 10, False),
    ('', 10, False),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)

# info table matching template exactly
table = doc.add_table(rows=3, cols=4)
table.style = 'Table Grid'

table.rows[0].cells[0].text = 'Project No.:'
table.rows[0].cells[1].text = '1'
table.rows[0].cells[2].text = 'Student Name:'
table.rows[0].cells[3].text = '[YOUR NAME]'

table.rows[1].cells[0].text = 'Student ID: '
table.rows[1].cells[1].text = '[YOUR ID]'
table.rows[1].cells[2].text = 'Date of Submission:'
table.rows[1].cells[3].text = '2026-05-30'

# grading row
row3 = table.rows[2]
cell = row3.cells[0]
cell.merge(row3.cells[1]).merge(row3.cells[2]).merge(row3.cells[3])
table.rows[2].cells[0].text = (
    'Grading (for Teaching Assistant)\n\nScore: ____________________\n\n'
    'Comments: ' + '_' * 200
)

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
    'In this project we are given three noisy images and we have to find what type '
    'of noise is in each one and then remove it. The images are 224x224 in size. '
    'I am not allowed to use the built-in processing functions from cv2, so I write '
    'all the filters by myself using only basic loops and math. I only use cv2 to '
    'read and save the images.'
)

# ---- section 2 ----
heading('2 Method Description')
body(
    'For image 1 I can see white dots scattered randomly, so this is salt noise. '
    'I use median filter with 5x5 window. For each pixel I collect the 25 values '
    'around it, sort them, and take the middle one. The median is good for this '
    'because isolated bright pixels get removed without blurring the edges. '
    'I first try 3x3 but some noise was still there so I change to 5x5.'
)
body(
    'For image 2 the noise look like fine random grain all over the image, this is '
    'gaussian noise. I build a 5x5 gaussian kernel by hand using the formula '
    'exp(-(x^2+y^2)/(2*sigma^2)) with sigma=1.5, then normalize it so the weights '
    'add to 1. Then I apply it by doing a weighted sum over each pixel neighborhood.'
)
body(
    'For image 3 it is more difficult because it has two kind of noise together. '
    'There is salt and pepper dots, and also the image is grainy. So I do it in two '
    'step. First I use a 3x3 median filter to remove the dots, because median is good '
    'for impulse noise. After that I use the gaussian filter again (same like image 2) '
    'with a small sigma to smooth the remaining grain without losing the text.'
)

# ---- section 3 ----
heading('3 Experiment Results and Analysis')
body(
    'After I run the code, image 1 look much cleaner. The white dots are gone and '
    'the edges of the van still look sharp. I think this is the advantage of median '
    'filter, it remove the outlier pixels but it does not blur the edge like a '
    'normal average filter would do. The only problem is it run a bit slow because '
    'of the double for loop over all pixels.'
)
body(
    'Image 2 become less noisy but a little bit soft. This is expected because '
    'gaussian filter is a kind of blur, so the random noise go away but the fine '
    'details also become a little smooth. If I use bigger sigma it remove more noise '
    'but the image become more blurry, so there is a tradeoff.'
)
body(
    'For image 3 the result is much better after I use two steps. At first I only use '
    'one filter but it was not enough, the dots were still there. After I do the median '
    'filter first the dots are gone, and then the gaussian filter smooth the grainy '
    'part. Now the text "ABUNDANCE" is clear and readable. The disadvantage of doing '
    'two step is that it take more time to run, and the gaussian also make the image a '
    'little bit soft.'
)

# ---- section 4 ----
heading('4 Summary')
body(
    'The most hard thing for me was the frequency domain filter for image 3. '
    'I did not immediately understand how the mask work in the spectrum, so I had '
    'to test different cutoff values until the result look good. The median and '
    'gaussian filters were more straightforward to implement.'
)
body(
    'From this project I learned that different types of noise need different methods '
    'to remove them. Salt noise need median filter, gaussian noise need gaussian '
    'filter, and periodic noise is best handled in the frequency domain. I also '
    'understand now that writing these filters from scratch help me understand much '
    'better how they actually work compared to just calling a library function.'
)

doc.save('report_project1.docx')
print('done')
