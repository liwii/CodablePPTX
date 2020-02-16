import yaml
import sys
from enum import Enum, auto
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from PIL import Image

SLIDE_WIDTH = Inches(13.33)
SLIDE_HEIGHT = Inches(7.5)
TOP_MARGIN = Inches(0.3)
SIDE_MARGIN = Inches(0.6)
TITLE_HEIGHT = Inches(1.5)

class Direction(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()

def add_center_title(slide, title):
    height = TITLE_HEIGHT
    left = SIDE_MARGIN
    width = SLIDE_WIDTH - 2 * left
    font_size = Pt(60)
    top = (SLIDE_HEIGHT - height) / 2
    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.clear()
    p = tf.add_paragraph()
    p.font.size = font_size
    p.alignment = PP_ALIGN.CENTER
    p.text = title

def add_title(slide, title, direction = Direction.VERTICAL):
    left = SIDE_MARGIN
    height = TITLE_HEIGHT
    top = TOP_MARGIN
    font_size = Pt(40)
    if direction == Direction.VERTICAL:
        width = SLIDE_WIDTH - 2 * left
    else:
        width = SLIDE_WIDTH / 2 - left - SIDE_MARGIN

    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.clear()
    p = tf.add_paragraph()
    p.font.size = font_size
    p.alignment = PP_ALIGN.LEFT
    p.text = title

def add_img(slide, img_file, direction = Direction.VERTICAL):
    img = Image.open(img_file)
    w, h = img.size
    ratio = h / w

    if direction == Direction.HORIZONTAL:
        max_width = SLIDE_WIDTH - SIDE_MARGIN * 2
        max_height = SLIDE_HEIGHT - TITLE_HEIGHT - TOP_MARGIN * 2
        if max_height / max_width > ratio:
            width = max_width
            height = max_width * ratio
        else:
            height = max_height
            width = height / ratio
        left = (SLIDE_WIDTH - width) / 2
        top = SLIDE_HEIGHT - height - TOP_MARGIN
    else:
        max_width = SLIDE_WIDTH / 2 - SIDE_MARGIN
        max_height = SLIDE_HEIGHT  - TOP_MARGIN * 2
        if max_height / max_width > ratio:
            width = max_width
            height = max_width * ratio
        else:
            height = max_height
            width = height / ratio
        left = SLIDE_WIDTH - SIDE_MARGIN - width
        top = (SLIDE_HEIGHT - height) / 2

    slide.shapes.add_picture(img_file, left, top, width=width)

def add_text(slide, text):
    font_size = Pt(24)
    height = SLIDE_HEIGHT - TOP_MARGIN * 3 - TITLE_HEIGHT
    width = SLIDE_WIDTH - SIDE_MARGIN * 2
    top = TOP_MARGIN * 2 + TITLE_HEIGHT
    left = SIDE_MARGIN
    tx_box = slide.shapes.add_textbox(left, top, width, height)
    tf = tx_box.text_frame
    tf.clear()
    p = tf.add_paragraph()
    p.font.size = font_size
    p.text = text

def apply_layout(slide, layout):
    if 'stackDirection' in layout and layout['stackDirection'] == 'horizontal':
        direction = Direction.HORIZONTAL
        if 'title' in layout:
            add_title(slide, layout['title'], direction)
        if 'centerTitle' in layout:
            add_center_title(slide, layout['centerTitle'])
        if 'img' in layout:
            add_img(slide, layout['img'], direction)
        if 'text' in layout:
            add_text(slide, layout['text'])
    else:
        direction = Direction.VERTICAL
        if 'title' in layout:
            add_title(slide, layout['title'], direction)
        if 'centerTitle' in layout:
            add_center_title(slide, layout['centerTitle'])
        if 'img' in layout:
            add_img(slide, layout['img'], direction)
        if 'text' in layout:
            add_text(slide, layout['text'])

def main(filename, output):
    f = open(filename, 'r')
    slides_dict = yaml.load(f, Loader=yaml.BaseLoader)
    f.close()
    layouts = slides_dict['slides']
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_slide_layout = prs.slide_layouts[6]
    for layout in layouts:
        slide = prs.slides.add_slide(blank_slide_layout)
        apply_layout(slide, layout)
    prs.save(output)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
