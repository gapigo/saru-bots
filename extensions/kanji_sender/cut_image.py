from PIL import Image
import math
import os
import pathlib

def generate_halfed_image():
    def get_img_path(img):
        return os.path.join(pathlib.Path(__file__).parent.absolute(), f'images/{img}')
    # Get image pixels and cut it

    img = Image.open(get_img_path("tanoshiijapanese.jpg"))
    n_squares = math.floor(img.width / 110)
    # im.crop((left, top, right, bottom))

    if n_squares % 2 == 1:
        half_w1 = math.ceil(math.ceil(n_squares/2)*110+(math.ceil(n_squares/2)+1)*3)
        half_w2 = math.ceil(math.ceil(n_squares/2)*110+(math.ceil(n_squares/2))*3)
    else:
        half_w1 = math.ceil((n_squares/2)*110+((n_squares/2)+1)*3)
        half_w2 = math.ceil((n_squares/2)*110+((n_squares/2))*3)
    half_h = math.floor(img.height/2) + 1
    im1 = img.crop((0, 0, half_w1, half_h-2))
    im2 = img.crop((half_w2, 0, img.width, half_h))
    
    # Shows the image in image viewer
    im1.save(get_img_path('im1.png'))
    im2.save(get_img_path('im2.png'))

    #resize, first image
    #image1 = image1.resize((426, 240))
    # im1_size = im1.size
    # im2_size = im2.size
    #new_image = Image.new('RGBA',(im1_size[0], im1_size[1]*2), (0,0,0,0))
    half_n_squares = math.ceil(n_squares/2)
    nim_width = half_n_squares*110+(half_n_squares+1)*3
    new_image = Image.new('RGBA',(nim_width, img.height), (0,0,0,0))
    new_image.paste(im1,(0,0))
    new_image.paste(im2,(0,im1.height))
    new_image.save(get_img_path("tanoshiijapanese.png"),"PNG")
    #new_image.show()
