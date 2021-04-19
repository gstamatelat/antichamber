import argparse

# Input values
parser = argparse.ArgumentParser(description='Vectorized Antichamber moral wall.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--magick', type=str, help='location of the magick executable', default='magick')
parser.add_argument('--potrace', type=str, help='location of the potrace executable', default='potrace')
parser.add_argument('--pdflatex', type=str, help='location of the pdflatex executable', default='pdflatex')
parser.add_argument('--xelatex', type=str, help='location of the xelatex executable', default='pdflatex')
parser.add_argument('--pdfinfo', type=str, help='location of the pdfinfo executable', default='pdfinfo')
parser.add_argument('--image-size', type=float, help='size in cm of each sign', default=1)
parser.add_argument('--quote-ratio', type=float, help='width to height ratio of each quote', default=3.75)
parser.add_argument('--horizontal-gap', type=float, help='horizontal margin between the images in cm', default=1 / 4)
parser.add_argument('--top-gap', type=float, help='vertical gap between the sign and its respective quote', default=0)
parser.add_argument('--bottom-gap', type=float, help='vertical gap between the sign and the quote of the top sign',
                    default=1 / 4)
parser.add_argument('--page-vertical-margin', type=float, help='top and bottom page margins', default=1 / 8)
parser.add_argument('--page-horizontal-margin', type=float, help='left side and right side page margins',
                    default=1 / 8)
parser.add_argument('--preview',
                    help='perform a preview only (without executing the quote optimization algorithm)', default=False,
                    action='store_true')
args = parser.parse_args()

# Print input values
print("Input arguments:", args)
print()

# Derived values
args.quote_height = args.image_size / args.quote_ratio
