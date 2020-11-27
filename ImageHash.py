# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 15:51:36 2020

@author: danie
(lost old implementation, trying with another library)
Image hashing, now with ImageHash library
"""

import cv2
import hashlib
from PIL import Image
import imagehash
import os
from pathlib import Path

def is_image(filename):
    return filename.lower().endswith((".png",".jpg",".jpeg",".bmp",".gif",".jpg",".svg"))

def getFilepaths(root):
    for path, subdirs, files in os.walk(root):
        # just ensuring that root is in correct format and the file has the right extension
        return [Path(root)/str(name) for name in files if is_image(name)]

def toHex(*str2hex):
    try:
        return [hashlib.md5(str(x).encode()).hexdigest() for x in str2hex]
    except TypeError:
        return hashlib.md5(str(str2hex).encode()).hexdigest()

def hamming_distance(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

def dhash(image, hash_size = 8):
    # Convert to grayscale to only analyze one channel
    BWimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize image to (size+1)x(size) in order to get (horizontal) gradient
    resized = cv2.resize(BWimage, (hash_size+1,hash_size))
    
    # compute gradient
    # check if adjacent pixels are brighter or darker (simple binary check)
    diff = resized[:,1:] > resized[:,:-1]
    
    # convert diff image to hash
    return sum([2 ** i for (i,v) in enumerate(diff.flatten()) if v])

def hashImages(root, hashfunc = imagehash.phash):
    filenames = getFilepaths(folder_path)
    images = {}
    for img in sorted(filenames):
        try:
            imHash = str(hashfunc(Image.open(img)))
        except Exception as e:
            print('Problem:', e, 'with', str(img))
            continue
        #if imHash in images:
            #print(str(img), '  already exists as', ' '.join(str(images[imHash])))
            #if 'dupPictures' in str(img):
            #    print('rm -v', str(img))
        images[imHash] = images.get(imHash, []) + [img]
    return images
    #for k, img_list in six.iteritems(images):
    #    if len(img_list) > 1:
    #        print(" ".join(img_list))



folder_path = Path('C:/Users/danie/Desktop/ImageHash/')

hash_dict = hashImages(folder_path)

key_list = list(hash_dict)