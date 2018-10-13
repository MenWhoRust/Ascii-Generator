import sys
import random
import argparse
import numpy as np
import math

from PIL import Image

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# 10 levels of gray
gscale2 = "@%#*+=-:. "


def getAverageL(image):
    """
    Given PIL Image, return average value of grayscale value
    """
    # get the image as a numpy array
    im = np.array(image)
    # get the dimentions
    w, h = im.shape
    # get the average
    return np.average(im.reshape(w*h))


def convertImageToAscii(fileName, columns, scale, moreLevels):
    """
    Given Image and dimensions (rows, cols), returns an m*n list of Images
    """

    # declare globals
    global gscale1, gscale2

    # Open the image and convert it to grayscale
    image = Image.open(fileName).convert('L')

    # store the image dimensions
    image_width, image_height = image.size[0], image.size[1]

    print(image_width)
    print(image_height)

    # Compute Tile width
    tile_width = image_width/columns

    # compute the tile height based on the aspect ratio and scale of the font
    tile_height = tile_width/scale

    # compute the number of rows to use in the final grid
    rows = int(image_height/tile_height)

    print('cols: %d, rows: %d' % (columns, rows))
    print('tile dims: %d x %d' % (tile_width, tile_height))

    # check if image size is too small
    if columns > image_width or rows > image_height:
        print('Image was to small for the specified columns')
        exit(0)

    # an ASCII image is a list of character strings
    ascii_image = []

    # generate the list of tile dimensions
    for j in range(rows):
        y1 = int(j * tile_height)
        y2 = int((j + 1) * tile_height)

        if j == rows - 1:
            y2 = image_height

        # append an empty string
        ascii_image.append("")
        for i in range(columns):
            # crop the image to fit the tile
            x1 = int(i * tile_width)
            x2 = int((i + 1) * tile_width)

            # correct the last tile
            if i == columns - 1:
                x2 = image_width

            # crop the image to extract the tile into another Image object
            img = image.crop((x1, y1, x2, y2))

            # get the average luminance
            avg = int(getAverageL(img))

            # look up the ASCII character for grayscale value (avg)
            if moreLevels:
                gsval = gscale1[int((avg * 69)/255)]
            else:
                gsval = gscale2[int((avg * 9)/255)]

            # append the ASCII character to the string
            ascii_image[j] += gsval

    # return text image
    return ascii_image


# main() function
def main():
    # create parser
    desc_str = 'This program converts an image into ASCII art.'
    parser = argparse.ArgumentParser(description=desc_str)

    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    # parse arguments
    args = parser.parse_args()

    imgFile = args.imgFile

    # set output file
    outFile = 'out.txt'

    if args.outFile:
        outFile = args.outFile

    # set scale default as 0.43, which suits a courier font
    scale = 0.43

    if args.scale:
        scale = float(args.scale)

    # set cols
    cols = 80

    if args.cols:
        cols = int(args.cols)

    print('Generating ASCII art...')

    # convert image to ASCII text
    aimg = convertImageToAscii(imgFile, cols, scale, args.moreLevels)

    # open a new text file
    f = open(outFile, 'w')

    # write each string in the list to the new file
    for row in aimg:
        f.write(row + '\n')

    # clean up
    f.close()
    print('ASCII art written to %s' % outFile)


# call main
if __name__ == '__main__':
    main()
