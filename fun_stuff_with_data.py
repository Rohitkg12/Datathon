from PIL import Image, ImageDraw, ImageEnhance
import glob
import os
import numpy as np
import demo

image_bit_depth = 16
scale_to_8bit = 255/image_bit_depth


def log_transform(image_path):
    img = Image.open(image_path)
    imgarray = np.asarray(img)
    # To explain the magic number:  the data values appear to be in a raw format
    # so in order to make a regular photo they first need to be a log base 2
    # operation applied depending on the bit depth this then needs to be scaled
    # so that they are withhin a range of 0 - 255.  According to the ESA website
    # the bit depth is 12, however the maximum value I found was around 25,000.
    # This would correspond to a bit depth of 15 bits. The
    imgarray = np.log2(imgarray)*scale_to_8bit
    return imgarray

def visible(red, blue, green):
    full_colour = np.dstack((red, green, blue))
    img = Image.fromarray(full_colour.astype('uint8'))
    return img
highest_val = 0


blue = demo.get_timeseries_image_paths(demo.TILE_X, demo.TILE_Y, "B02")
green = demo.get_timeseries_image_paths(demo.TILE_X, demo.TILE_Y, "B03")
red = demo.get_timeseries_image_paths(demo.TILE_X, demo.TILE_Y, "B04")



for i in range (len(blue)):
    r = log_transform(red[i])
    g = log_transform(green[i])
    b = log_transform(blue[i])
    img = visible(r,g,b)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(4.0)
    img.save('./processed/ts'+str(i)+'.jpg',"JPEG")


# This loop was for exploring the bit depth of the images.  Currently
# the highest value seen was 23,470 on the blue channel, 26,814 on the
# red channel and 24,216 on the green.  This indicates a bit depth of
# at least 15 bits

#for i in range (len(blue)):
#    img = Image.open(green[i])
#    imgarray = np.asarray(img)
#    high = np.amax(imgarray)
#    if high > highest_val:
#        highest_val = high
#
#print(highest_val)
