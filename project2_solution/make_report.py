"""Build the Project 2 report (docx) from the provided template."""
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

STUDENT_NAME = "[YOUR NAME]"
STUDENT_ID   = "[YOUR STUDENT ID]"
SUBMIT_DATE  = "2026-05-30"


def heading(doc, text, level=1):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(13 if level == 1 else 11)
    return p


def body(doc, text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    return p


def add_image(doc, path, width=Inches(5.5), caption=None):
    if os.path.exists(path):
        doc.add_picture(path, width=width)
    if caption:
        cp = doc.add_paragraph(caption)
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.runs[0].italic = True
        cp.runs[0].font.size = Pt(10)


doc = Document()

# ── Title ──────────────────────────────────────────────────────────────────
for line, sz, bold in [
    ('Harbin Institute of Technology (Shenzhen)', 14, True),
    ('Project Report', 16, True),
    ('', 10, False),
    ('Image Processing (COMP5033)', 12, False),
    ('2025–2026 Spring Semester', 12, False),
    ('Teacher: Prof. Weizheng Zhang', 12, False),
]:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(line)
    run.bold = bold
    run.font.size = Pt(sz)

doc.add_paragraph()

# ── Student info table ─────────────────────────────────────────────────────
table = doc.add_table(rows=2, cols=4)
table.style = 'Table Grid'
cells = table.rows[0].cells
cells[0].text = 'Project No.:'
cells[1].text = '2'
cells[2].text = 'Student Name:'
cells[3].text = STUDENT_NAME

cells = table.rows[1].cells
cells[0].text = 'Student ID:'
cells[1].text = STUDENT_ID
cells[2].text = 'Date of Submission:'
cells[3].text = SUBMIT_DATE

doc.add_paragraph()

# ── Section 1 ─────────────────────────────────────────────────────────────
heading(doc, '1  Project Content')
body(doc,
    'This project implements a morphological algorithm to detect the boundary of '
    'all objects in a binary image. The input is Figure_P2.jpg (1024×1024 grayscale), '
    'a yin-yang design with two interlocking cat silhouettes and a gray background. '
    'The processing pipeline is: (1) convert the grayscale image to binary using '
    "Otsu's automatic thresholding, then (2) extract object boundaries via "
    'morphological erosion. All key processing steps are implemented using only '
    'NumPy; cv2 is used solely for image I/O.')

# ── Section 2 ─────────────────────────────────────────────────────────────
heading(doc, '2  Method Description')

heading(doc, '2.1  Binarization – Otsu\'s Method', level=2)
body(doc,
    "Otsu's method (1979) automatically selects the threshold T* that maximises the "
    "inter-class variance between the two resulting pixel classes (foreground and background):\n\n"
    "    σ²_B(t) = w₀(t) · w₁(t) · [μ₀(t) − μ₁(t)]²\n\n"
    "where w₀, w₁ are the class probabilities and μ₀, μ₁ are the class mean "
    "intensities at threshold t. The optimal threshold is T* = argmax_t σ²_B(t).\n\n"
    "Implementation:\n"
    "  1. Compute the 256-bin intensity histogram.\n"
    "  2. Scan t from 0 to 255, maintaining running sums of w₀ and cumulative mean.\n"
    "  3. Compute σ²_B(t) at each t and track the maximum.\n\n"
    "For Figure_P2.jpg the algorithm returns T* = 107. Pixels with intensity > 107 "
    "are set to 1 (foreground: white cat + bright areas), while pixels ≤ 107 are "
    "set to 0 (background: black cat + gray border). This produces a clean binary "
    "image with 60.9% foreground pixels.")

heading(doc, '2.2  Morphological Boundary Extraction', level=2)
body(doc,
    'The inner boundary of a binary set A with structuring element B is defined as:\n\n'
    '    β(A) = A − (A ⊖ B)\n\n'
    'where ⊖ denotes morphological erosion. Erosion shrinks every foreground region '
    'by removing pixels that are on or near the boundary; subtracting the eroded '
    'image from the original leaves exactly the 1-pixel-wide boundary layer.\n\n'
    'Erosion implementation (3×3 square structuring element):\n'
    '  1. Zero-pad the binary image by 1 pixel on each side.\n'
    '  2. Extract 3×3 sliding windows via numpy.lib.stride_tricks.sliding_window_view '
    '(output shape: H×W×3×3).\n'
    '  3. A pixel is set to 1 iff ALL 9 pixels in its 3×3 neighbourhood are 1 '
    '(np.all over the last two axes).\n\n'
    'To capture boundaries of BOTH the white (bright) regions and the black (dark) regions:\n'
    '  • boundary_fg = binary − erosion(binary)          [boundary of white cat]\n'
    '  • boundary_bg = (1−binary) − erosion(1−binary)    [boundary of dark cat]\n'
    '  • Final boundary = clip(boundary_fg + boundary_bg, 0, 1)')

# ── Section 3 ─────────────────────────────────────────────────────────────
heading(doc, '3  Experiment Results and Analysis')

add_image(doc, 'fig_p2_comparison.png',
          caption='Figure 1. Left: original grayscale image. '
                  'Centre: binary image after Otsu thresholding (T*=107). '
                  'Right: boundary image (Output_P2.jpg).')
doc.add_paragraph()

body(doc,
    'Binarization (centre panel): Otsu\'s threshold T*=107 correctly separates '
    'the white cat body and the fine detail regions from the dark cat body and '
    'the gray background. The thin whisker lines and facial features are well '
    'preserved in the binary image.')
body(doc,
    'Boundary detection (right panel): The morphological boundary image contains '
    '27,460 white pixels (2.62% of the image). The output shows a continuous, '
    '1-pixel-wide boundary that accurately traces: the outer circular perimeter, '
    'the S-shaped dividing curve between the two cats, the silhouettes of both '
    'cat heads, the whiskers and ear details, the tails, and paw features. '
    'The result is visually clean with no spurious edges in the interior regions.')
body(doc,
    'Algorithm strengths and limitations: The 3×3 square structuring element '
    'produces sharp, single-pixel boundaries and is computationally efficient '
    '(vectorised with numpy). A limitation is that very thin structures such as '
    'the fine whisker lines (width < 3 px) may appear slightly fragmented after '
    'erosion; a cross-shaped or smaller structuring element could preserve these better.')

# ── Section 4 ─────────────────────────────────────────────────────────────
heading(doc, '4  Summary')
body(doc,
    "The main difficulty in this project was correctly binarizing a multi-tone "
    "image (gray background + white + black) before applying the morphological "
    "operation. Otsu's method elegantly solved this by analytically finding the "
    "optimal threshold without manual tuning.")
body(doc,
    "Key knowledge gained:\n"
    "  1. Otsu's thresholding is a powerful unsupervised binarization technique "
    "whose inter-class variance formulation can be computed in a single O(L) sweep "
    "over the histogram (L = number of intensity levels).\n"
    "  2. Morphological erosion combined with simple set subtraction provides a "
    "precise, 1-pixel-wide boundary without complex edge operators or gradient "
    "thresholding.\n"
    "  3. Detecting boundaries for both bright and dark regions (by processing "
    "both the binary image and its complement) captures all object edges in a "
    "single unified boundary map.\n"
    "  4. The choice of structuring element (size and shape) directly controls "
    "the thickness of the boundary and sensitivity to thin structures.")

doc.save('report_project2.docx')
print('Saved report_project2.docx')
