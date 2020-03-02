import yaml
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

SLIDE_WIDTH = Inches(13.33)
SLIDE_HEIGHT = Inches(7.5)

def main(filename, output):
    f = open(filename, 'r')
    layouts_dict = yaml.load(f, Loader=yaml.BaseLoader)
    layouts = layouts_dict['layouts']
    f.close()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    for layout in layouts:
        slide = prs.slides.add_slide(blank_slide_layout)
        apply_layout(slide, layout)
    prs.save(output)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])