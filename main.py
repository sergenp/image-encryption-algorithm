import os
# numpy is a library that makes it easier to work with arrays and matrices 
import numpy as np
# a library for reading, writing, showing images
from PIL import Image
# import zigzag
from util import zigzag
#for flattening the 3D or 2D arrays and chaining them examples:
# itertools.chain('ABC', 'DEF') --> A B C D E F
# itertools.chain.from_iterable([[1,2,3], [4,5,6]]) --> [1,2,3,4,5,6]
import itertools
flatten = itertools.chain.from_iterable

from algorithm import encrypt_image

image_name, image_extension = os.path.splitext("duck.jpeg")
image_file = os.path.join(os.path.dirname(__file__), f"{image_name}{image_extension}")

im = Image.open(image_file)
# convert image to array
im_arr = np.asarray(im)
try:
    M, N, C = im_arr.shape
except ValueError:
    raise ValueError("Given image couldn't be read")

print(f"{im.size} {im.mode} image detected")
flattened_image = []
# STEP 2. Convert the image to array ziggag reading
for clr in im_arr:
    flattened_image.append(zigzag(clr))
flattened_image = list(flatten(flattened_image))

encrypted_blocks = list(flatten(encrypt_image(flattened_image)))


# flatten the blocks to a 1xMNC arr
enc = np.asarray(encrypted_blocks)
# recreate the image
reshaped = np.reshape(enc, (M,N,C)).astype(np.uint8)
img = Image.fromarray(reshaped)
img.save(f'encrypted_{image_name}{image_extension}')
img.show()