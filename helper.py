from genericpath import isdir
import os
import shutil
from PIL import Image, ImageFilter
import random 

def get_layer_names():
    # print("layer name")
    rel_path = 'layers/'
    layer_list = os.listdir(rel_path)
    to_remove = '.DS_Store'
    if to_remove in layer_list:
       layer_list.remove(to_remove)
    print(layer_list)
    return layer_list


def get_weight(filename='abc#20.png'):
    sep = filename.split("#")
    sep = sep[-1].split(".")
    return sep[-2]
    

def get_image_list(layername='Background'):
    rel_path = 'layers/'+layername
    images_list = os.listdir(rel_path)
    return images_list
    

def get_images_weight_list(layername='Background'):
    images_list = get_image_list(layername)
    # print(images_list)
    weight_list=[]
    for e in images_list:
        weight = get_weight(e)
        # print(weight_list)
        weight_list.append(weight)
    weight_list = [int(i) for i in weight_list]
    # print(weight_list)
    return images_list, weight_list


def get_random_image_from_layer(layername='Background'):
    # print("choose image")
    images_list, weight_list = get_images_weight_list(layername)
    choice = random.choices(images_list,weights=weight_list)
    path = 'layers/'+layername+'/'+choice[0]
    return path
   


def compose_image():
    background = get_random_image_from_layer('Background')
    body = get_random_image_from_layer('Body')
    head = get_random_image_from_layer('Head')
    eyes = get_random_image_from_layer('Eyes')
    legs = get_random_image_from_layer('Legs')
    mouth = get_random_image_from_layer('Mouth')
    # print(mouth)
    im_bg=Image.open(background)
    im_body=Image.open(body)
    im_head = Image.open(head)
    im_eyes = Image.open(eyes)
    im_legs = Image.open(legs)
    im_mouth = Image.open(mouth)

    im_head.paste(im_eyes,mask=im_eyes)
    im_head.paste(im_mouth,mask=im_mouth)
    im_body.paste(im_legs,mask=im_legs)
    im_bg.paste(im_body, mask=im_body)
    im_bg.paste(im_head,mask=im_head)
    newsize = (512,512)
    newimg = im_bg.resize(newsize, Image.AFFINE)
    
    # im_bg.show()
    # print(type(im_bg))
    return newimg

def save_images(number_of_images=20):
    if not os.path.isdir('images'):
        os.mkdir('images')
    else:
        shutil.rmtree('images')
        os.mkdir('images')
    for i in range(number_of_images):
        img = compose_image()
        path_to_save = 'images/'+str(i+1)+'.png'
        print(path_to_save)
        img.save(path_to_save)
        # img.save('images/'+str(i+1)+'.png')



    pass





def test_show_image():
    im_bg = Image.open('layers/Background/bg_beach#4.png')
    im_body = Image.open('layers/Body/batman_black_body#100.png')
    im_head = Image.open('layers/Head/head_blonde_girl#100.png')
    im_eyes = Image.open('layers/Eyes/eyes_cross#100.png')
    im_legs= Image.open('layers/Legs/legs_rocket#100.png')
    im_mouth = Image.open('layers/Mouth/mouth_long#100.png')
    # im = Image.composite(im_body, im_bg, im_bg)
    im_head.paste(im_eyes,mask=im_eyes)
    im_head.paste(im_mouth,mask=im_mouth)
    im_body.paste(im_legs,mask=im_legs)
    im_bg.paste(im_body, mask=im_body)
    im_bg.paste(im_head,mask=im_head)
    
    # im_body.paste(im_bg)
    im_bg.show()


