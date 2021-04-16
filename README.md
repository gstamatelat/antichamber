# Antichamber moral wall

My attempt to vectorize and produce an Antichamber moral wall using Potrace and LaTeX.

Download the final result using the default settings via the links: [antichamber.pdf](docs/antichamber.pdf)
, [antichamber.svg](docs/antichamber.svg).

<img alt="Antichamber moral wall" src="docs/antichamber.svg" width="100%" />

## Requirements

1. Python
2. ImageMagick
3. Potrace
4. LaTeX

## How does it work?

1. The signs are vectorized using Potrace. This allows them to be magnified for printing in large posters.
2. The quotes are being generated using LaTeX. First the optimal number of lines is being determined so that the font
   size appears bigger on the output pdf. Using this number of lines, a minimum raggedness algorithm is applied to
   determine to most visually appealing split of the quote into this optimal number of lines. The quote is then rendered
   into pdf using LaTeX.
3. The signs along with their respective quotes are stitched into the final pdf.

## Usage

Type `antichamber --help` for usage. Because the minimum raggedness algorithm is implemented using a brute-force method,
the script may take a long time to complete.
