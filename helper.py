from email.mime import base
from genericpath import isdir
from heapq import merge
import os
import shutil
from PIL import Image, ImageFilter
import random 
import copy 

def get_layer_names():
    # print("layer name")
    rel_path = 'layers/'
    layer_list = get_filtered_dir('layers/')
    return layer_list


def get_weight(filename='abc#20.png'):
    sep = filename.split("#")
    sep = sep[-1].split(".")
    return sep[-2]
    

def get_image_list(layernamepath='layers/Background'):
    rel_path = layernamepath
    images_list = os.listdir(rel_path)
    images_list = [i for i in images_list if i.split('.')[-1]=='png']
    return images_list

def get_dir_names(layernamepath='layers'):
    dir_list = os.listdir(layernamepath)
    dir_list = [i for i in dir_list if os.path.isdir(layernamepath+"/"+i)]
    return dir_list 

def get_images_weight_list(layernamepath='layers/Background'):
    # give full path instead of just layername
    images_list = get_image_list(layernamepath)
    # print(images_list)
    weight_list=[]
    for e in images_list:
        weight = get_weight(e)
        # print(weight_list)
        weight_list.append(weight)
    weight_list = [int(i) for i in weight_list]
    # print(weight_list)
    return images_list, weight_list


def get_random_image_from_layer(layernamepath='layers/Background'):
    # print("choose image")
    images_list, weight_list = get_images_weight_list(layernamepath)
    # print(f"img,wt:: {images_list, weight_list}")
    if (len(images_list)==0 or len(weight_list)==0):
        return ''
    if (sum(weight_list) <=0):
        return ''
    choice = random.choices(images_list,weights=weight_list)
    path = layernamepath+'/'+choice[0]
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
    return newimg

def get_filtered_dir(base='layers'):
    dirs = os.listdir(base)
    exclude = ['.DS_Store','_pycache__']
    for i in exclude:
        if i in dirs:
            dirs.remove(i)
    # print(dirs) 
    return dirs 

    ## Process Directories to make one level tree 
def get_tree_process_dir(base_layer= 'layers', base_image=''):
    tree = {}
    filtered_dir = get_filtered_dir(base_layer)
    # print(f"Filtered dir: {filtered_dir}")
    if len(filtered_dir)==0:
        return tree 
    if base_image=='':
        base_img = get_random_image_from_layer(base_layer) ###
    else :
        base_img= base_image
    dirs = [d for d in filtered_dir if os.path.isdir(f"{base_layer}/{d}")]
    # print(f"dirs - {dirs}")
    img_list=[]
    for d in dirs:
        new_base= f"{base_layer}/{d}"
        filtered_dir = get_filtered_dir(new_base)
        if len(filtered_dir)==0:
            continue
        new_img = get_random_image_from_layer(new_base)
        if new_img != '':
            img_list.append(new_img) ###
        # print(f"Dirs loop 1 >> {filtered_dir}")
    tree[base_img] = img_list ###
    # print(f"\nImage tree: {tree}")
    return tree

def get_dir_from_image(img_path='layers/Background/bg_sea#15.png'):
    if img_path=='':
        return 
    lis = img_path.split('/')
    lis.pop()
    path = '/'.join(lis)
    return path 

# main tree
def compose_image_tree_iter(base_layer='layers'):
    layer1 = get_tree_process_dir(base_layer)
    merge_dict = layer1
    # print(f" Layer 1 : {layer1}")
    key = list(layer1.keys())[0] # get the first and only key
    base_images2 = layer1[key]
    if len(base_images2) == 0:
        return merge_dict
    # print(f"base image2: {base_images2}")
    
    for im in base_images2:
        # print(f"an image:: {im}")
        next_dir = get_dir_from_image(im)
        # print(f"\n{20*'*'}next dir::: {next_dir}")
        layer2 = get_tree_process_dir(base_layer=next_dir, base_image=im)
        # print(f"Layer2 dict:: {layer2}")
        key = list(layer2.keys())[0] #get the first and only key 
        base_images3 = layer2[key]
        if len(base_images3) == 0:
            continue
        merge_dict = {**merge_dict, **layer2}
        
        # print(f"base images 3 :: {base_images3}\n")
        for im3 in base_images3:
            next_dir3 = get_dir_from_image(im3)
            # print(f"\nnext dir 3:: {next_dir3}")
            layer3 = get_tree_process_dir(base_layer=next_dir3, base_image=im3)
            merge_dict= {**merge_dict, **layer3}
            key = list(layer3.keys())[0]
            base_image4 = layer3[key]
            if len(base_image4) == 0:
                    # print(f"\n*****len 04 *****")
                    continue
            for im4 in base_image4:
                next_dir4 = get_dir_from_image(im4)
                layer4 = get_tree_process_dir(base_layer=next_dir4, base_image=im4)
                key = list(layer4.keys())[0]
                base_image5 = layer4[key]
                if len(base_image5) == 0:
                    # print(f"\n*****len 0 *****")
                    continue
                merge_dict= {**merge_dict, **layer4} 
                # print(f"\nBase images 5 :: {base_image5}")
                for im5 in base_image5:
                    next_dir5 = get_dir_from_image(im5)
                    layer5 = get_tree_process_dir(base_layer=next_dir5, base_image=im5)
                    key = list(layer5.keys())[0]
                    base_image6 = layer5[key]
                    if len(base_image6) == 0:
                        continue
                    merge_dict = {**merge_dict, **layer5}

    # print(f"\nMErge Dict: {merge_dict}")
    return merge_dict



    

#Redundant (Recursive, no tail recursion elimination causes problems )
def compose_image_tree(iters=0,base_path='layers', tree_dict={},base_image='layers/empty_base_bg#100.png'):
    # print("compose image tree")
    ''' Have an empty background image as a base then paste the 
    other images recursively, including any non-empty background images.
    To do this firs this function will create a dictionary of
    parent:[list of children] '''
    total_iters = 20
    # basic_bg = 'layers/empty_base_bg.png'
    dir_list = get_filtered_dir(base_path)
    # print(len(dir_list))
    iters = iters + 1
    # iters += 1
    if len(dir_list) == 0:
        # print("len path = 0")
        return 
    if iters >= total_iters:
        # print("exceeds total iter")
        return 
   
    key = base_image
    dirs = get_dir_names(base_path)
    images_list_dict = {}
    for d in dirs:
        dir_path = f"{base_path}/{d}"
        dirlist = os.listdir(dir_path)
        img = get_random_image_from_layer(dir_path)
        if img != '':
            # images_list.append(img)
            images_list_dict[dir_path] = img 
        
    # print(images_list)
    tree_dict[key] = list(images_list_dict.values())
    # print(tree_dict)
    # print("+"*20)
    
    # print(f"-------- iter: {iters} -------")
    dir_iters = get_dir_names(base_path)
    # print(dir_iters)
    for d in dir_iters:
        new_base_path = f"{base_path}/{d}"
        if new_base_path in images_list_dict.keys():
            new_base_image = images_list_dict[new_base_path]
            compose_image_tree(iters=iters, base_path=new_base_path, tree_dict=tree_dict,base_image=new_base_image)
    # print("*"*20)
    # print(tree_dict)
    # tree_dict = [d for d in tree_dict if tree_dict ]
    filtered_tree_dict = {}
    for (key,value) in tree_dict.items():
        if len(value) != 0:
            filtered_tree_dict[key] = value
    # print(f"LENGTH OF DICT: {len(filtered_tree_dict)}")
    return filtered_tree_dict
   

# def compose_image_from_dict():
    #Returns a random image 
    #Deprecated 
    layer_dict = compose_image_tree()
    # my_dict = dict(reversed(my_dict.items()))
    layer_dict = dict(reversed(layer_dict.items()))
    for (key,value) in layer_dict.items():
        print(f" {key} : {value}")
        print("*"*50)
        im_base = Image.open(key)
        if key== list(layer_dict.keys())[0]:
            return_base_image = im_base
        for img in value:
            layer_img = Image.open(img)
            im_base.paste(layer_img, mask=layer_img)
    newsize = (512,512)
    newimg = return_base_image.resize(newsize, Image.AFFINE)
    return newimg
    

def compose_image_from_tree(final_size=(512,512)):
    # image_tree = compose_image_tree()
    image_tree = compose_image_tree_iter()
    image_tree= dict(reversed(image_tree.items()))
    image_dict = {}
    for k,v in image_tree.items():
        for imgpath in v:
            image_dict[imgpath] = Image.open(imgpath)
        # print(image_dict)
    for k,v in image_tree.items():
        if k not in image_dict.keys():
            image_dict[k] = Image.open(k)
    
    final_image = ''
    for k,v in image_tree.items():
        # print(f"KEY: {k}")
        img_base = image_tree[k]
        # print(f"image base: {img_base}")
        for item in v:
            # print(f" pasting {item} ON {k}")
            base_image = image_dict[k]
            pasted_image = image_dict[item]
            base_image.paste(pasted_image, mask=pasted_image)
            final_image = base_image
    final_image = final_image.resize(final_size, Image.AFFINE)  
    # final_image.show()  
    return final_image      
    



def save_image_from_tree(number_of_images=20):
    if not os.path.isdir('images'):
        os.mkdir('images')
    else:
        shutil.rmtree('images')
        os.mkdir('images')
    for i in range(number_of_images):
        img = compose_image_from_tree()
        path_to_save = 'images/'+str(i+1)+'.png'
        # print(path_to_save)
        img.save(path_to_save)

def save_images(number_of_images=20):
    if not os.path.isdir('images'):
        os.mkdir('images')
    else:
        shutil.rmtree('images')
        os.mkdir('images')
    for i in range(number_of_images):
        img = compose_image()
        path_to_save = 'images/'+str(i+1)+'.png'
        # print(path_to_save)
        img.save(path_to_save)
       


def test_show_image():
    im_bg = Image.open('layers/Background/bg_beach#4.png')
    im_body = Image.open('layers/Background/Body/batman_black_body#100.png')
    im_head = Image.open('layers/Background/Body/Head/head_black_girl#100.png')
    im_eyes = Image.open('layers/Background/Body/Head/Eyes/batman_black_eyes#100.png')
    im_legs= Image.open('layers/Background/Legs/ironman_legs#0.png')
    im_mouth = Image.open('layers/Background/Body/Head/Mouth/mouth_long#100.png')
    # im = Image.composite(im_body, im_bg, im_bg)
    
    
    im_head.paste(im_eyes,mask=im_eyes)
    im_head.paste(im_mouth,mask=im_mouth)
    im_body.paste(im_legs,mask=im_legs)
    im_bg.paste(im_head,mask=im_head)
    im_bg.paste(im_body, mask=im_body)
    
    
    
    # im_body.paste(im_bg)
    im_bg.show()


