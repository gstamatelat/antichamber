import os
import pathlib
import shutil

import functions
import settings

# Constants
IMAGES = 120  # How many images there are
OUTPUT = "out"  # Output directory

# Change working directory
current_path = pathlib.Path(__file__).parent.absolute()
current_path = current_path.joinpath("../")
os.chdir(current_path)

# Check if output directory exists
if os.path.exists(OUTPUT):
    print("Output directory already exists")
    exit()

# Create directories
shutil.rmtree(OUTPUT, ignore_errors=True)
os.makedirs("{}/img_bmp".format(OUTPUT))
os.makedirs("{}/img_potrace".format(OUTPUT))
os.makedirs("{}/quote_pdf".format(OUTPUT))
os.makedirs("{}/grid_pdf".format(OUTPUT))

# Create bmp files of the images
for i in range(1, IMAGES + 1):
    functions.convert('data/img/{i}.png'.format(i=i), '{out}/img_bmp/{i}.bmp'.format(out=OUTPUT, i=i))
    functions.negate('{out}/img_bmp/{i}.bmp'.format(out=OUTPUT, i=i))

# Create pdf of the images by running potrace
for i in range(1, IMAGES + 1):
    functions.potrace('{out}/img_bmp/{i}.bmp'.format(out=OUTPUT, i=i),
                      '{out}/img_potrace/{i}.pdf'.format(out=OUTPUT, i=i))

# Create the quotes pdf
line_no = 1
with open("data/quotes", 'r') as quotes_file:
    for quote in quotes_file:
        print("Creating quote {}".format(line_no))
        if settings.args.preview:
            functions.quote_pdf(quote, "{out}/quote_pdf/{i}.pdf".format(out=OUTPUT, i=line_no))
        else:
            functions.quote_pdf_best(quote, "{out}/quote_pdf/{i}.pdf".format(out=OUTPUT, i=line_no),
                                     settings.args.quote_ratio)
        line_no += 1

# Create the grid tex code
grid_tex = "\\documentclass[border={{{side_margin}cm {top_margin}cm {side_margin}cm {top_margin}cm}}]{{standalone}}\n\\usepackage{{tikz}}\n\\usepackage{{adjustbox}}\n\\begin{{document}}\n\\begin{{tikzpicture}}\n".format(
    top_margin=settings.args.vertical_margin,
    side_margin=settings.args.horizontal_margin
)
for i in range(0, 15):
    for j in range(0, 8):
        x = i * (settings.args.image_size + settings.args.horizontal_gap)
        y_img = -j * (
                settings.args.image_size + settings.args.quote_height + settings.args.top_gap + settings.args.bottom_gap)
        y_quote = y_img - settings.args.image_size / 2 - settings.args.quote_height / 2 - settings.args.top_gap
        grid_tex += "\\node at ({x},{y}) {{\\adjustimage{{width={img_size}cm,height={img_size}cm,keepaspectratio,valign=m}}{{{current_path}/tmp/img_potrace/{i}.pdf}}}};\n".format(
            current_path=os.getcwd().replace("\\", "/"),
            x=x,
            y=y_img,
            img_size=settings.args.image_size,
            i=15 * j + i + 1
        )
        grid_tex += "\\node at ({x},{y}) {{\\adjustimage{{width={img_size}cm,height={quote_height}cm,keepaspectratio,valign=m}}{{{current_path}/tmp/quote_pdf/{i}.pdf}}}};\n".format(
            current_path=os.getcwd().replace("\\", "/"),
            x=x,
            y=y_quote,
            img_size=settings.args.image_size,
            quote_height=settings.args.quote_height,
            i=15 * j + i + 1
        )
grid_tex += '\\end{tikzpicture}\n\\end{document}\n'

# Compile the grid
functions.pdflatex(grid_tex, "{out}/grid_pdf/grid.pdf".format(out=OUTPUT))
