import yaml
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

SLIDE_WIDTH = Inches(13.33)
SLIDE_HEIGHT = Inches(7.5)

def add_shape(base, shape_config):
    if shape_config['type'] == 'rectangle':
        shape_type = MSO_SHAPE.RECTANGLE
    else:
        raise ValueError(f'Invalide shape type value: {shape_config["type"]}')
    l, t, w, h = frame_to_position(shape_config['frame'])
    shapes = base.shapes
    shape = shapes.add_shape(shape_type, l, t, w, h)
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(shape_config['color'][1:])
    shape.line.fill.background()
    shape.shadow.inherit = False
    shape.shadow.visible = False


def add_image(base, content, theme):
    default_config = {
        'aspect': 'fill'
    }
    if isinstance(content, dict):
        content_config = content
    else:
        content_config = { 'file': content }
    config = { **default_config, **theme, **content_config }
    img = Image.open(config['file'])
    l, t, w, h = frame_to_position(config['frame'])
    frame_ratio = h / w
    img_w, img_h = img.size
    img_ratio = img_h / img_w
    if config['aspect'] == 'fill':
        left = l
        top = t
        height = h
        width = w
        if frame_ratio > img_ratio:
            crop_horizontal = 0.5 - (img_ratio / frame_ratio) / 2
            crop_vertical = 0
        else:
            crop_horizontal = 0
            crop_vertical = 0.5 - (frame_ratio / img_ratio) / 2
    elif config['aspect'] == 'fit':
        crop_horizontal = 0
        crop_vertical = 0
        if frame_ratio > img_ratio:
            left = l
            width = w
            height  = width * img_ratio
            top = t + (h - height) / 2
        else:
            top = t
            height = h
            width = height / img_ratio
            left = l + (w - width) / 2
    else:
        raise ValueError(f'Invalid aspect value: {config["aspect"]}')
    picture = base.shapes.add_picture(config['file'], left, top, width=width, height=height)
    picture.crop_right = crop_horizontal
    picture.crop_left = crop_horizontal
    picture.crop_top = crop_vertical
    picture.crop_bottom = crop_vertical

def frame_to_position(frame):
    xl, xh = [float(f) for f in frame['x']] 
    yl, yh = [float(f) for f in frame['y']] 

    left = xl * SLIDE_WIDTH / 100
    width = xh * SLIDE_WIDTH / 100 - left
    top = yl * SLIDE_HEIGHT / 100
    height = yh * SLIDE_HEIGHT/ 100 - top
    return left, top, width, height

def add_text(base, content, theme):
    default_config = {
        'value' : '',
        'font' : 'Arial',
        'fontsize' : 26,
        'fontcolor': "#4D4D4D",
        'valign': 'top',
        'halign': 'left',
    }
    if isinstance(content, dict):
        content_config = content
    else:
        content_config = { 'value': content }
    config = { **default_config, **theme, **content_config }
    l, t, w, h = frame_to_position(config['frame'])
    tx_box = base.shapes.add_textbox(l, t, w, h)
    tf = tx_box.text_frame
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = config['value']
    p.font.name = config['font']
    p.font.size = Pt(int(config['fontsize']))
    p.font.color.rgb = RGBColor.from_string(config['fontcolor'][1:])

    if config['valign'] == 'top':
        tf.vertical_anchor = MSO_ANCHOR.TOP 
    elif config['valign'] == 'middle':
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    elif config['valign'] == 'bottom':
        tf.vertical_anchor = MSO_ANCHOR.BOTTOM
    else:
        raise ValueError(f'Invalid valign value: {config["valign"]}')

    if config['halign'] == 'left':
        p.alignment = PP_ALIGN.LEFT
    elif config['halign'] == 'center':
        p.alignment = PP_ALIGN.CENTER
    elif config['halign'] == 'right':
        p.alignment = PP_ALIGN.RIGHT
    else:
        raise ValueError(f'Invalid halign value: {config["halign"]}')

def apply_design(base, content, theme):
    if 'title' in content:
        for i, title in enumerate(content['title']):
            add_text(base, title, theme['title'][i])

    if 'subtitle' in content:
        for i, subtitle in enumerate(content['subtitle']):
            add_text(base, subtitle, theme['subtitle'][i])

    if 'text' in content:
        for i, text in enumerate(content['text']):
            add_text(base, text, theme['text'][i])

    if 'image' in content:
        for i, image in enumerate(content['image']):
            add_image(base, image, theme['image'][i])

    if 'shape' in theme:
        for shape in theme['shape']:
            add_shape(base, shape)

def draw_theme(theme, layouts):
    for layout in layouts:
        if layout['id'] == theme:
            return layout
    raise ValueError(f'Theme doesn\'t exist: {theme}')

def main(filename, output):
    f = open(filename, 'r')
    presentation_dict = yaml.load(f, Loader=yaml.BaseLoader)
    f.close()
    slides = presentation_dict['slides']
    layouts = []
    for layout_file in presentation_dict['import']:
        layout_f = open(layout_file, 'r')
        layout_dict = yaml.load(layout_f,  Loader=yaml.BaseLoader)
        layout_f.close()
        layouts = layout_dict['layouts'] +  layouts
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    blank_slide_layout = prs.slide_layouts[6]
    for slide in slides:
        blank_slide = prs.slides.add_slide(blank_slide_layout)
        if slide['theme']:
            theme = draw_theme(slide['theme'], layouts)
        apply_design(blank_slide, slide, theme)
    prs.save(output)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])