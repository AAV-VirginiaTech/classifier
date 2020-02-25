import numpy as np
from random import randint
import cv2
from multiprocessing import Pool
import json
from math import floor

CROP_HEIGHT = 256
CROP_WIDTH = 256
sample_dir_out = "./gen/samples/data/"
mask_dir_out = "./gen/masks/data/"
NUM_SAMPLES_PER_FILE = 100
with open("metadata.json", "r") as f:
    meta = json.load(f)

def load_image_and_mask(number):
    """Returns image and mask corresponding to the particular number in the file"""
    print(f"Loading file {number}")
    img = cv2.imread(f"./samples/samples\\{number}.JPG", cv2.IMREAD_GRAYSCALE)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.imread(f"./samples/masks\\{number}-mask.JPG", cv2.IMREAD_GRAYSCALE)
    # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    return (img, mask)

def randomCrop(img, mask, width, height, x0, y0):
    """Creates a random crop with x0, y0 guaranteed to be somewhere in the crop
       Parameters:
       img - image to crop
       mask - corresponding mask
       width - crop width
       height - crop height
       x0 - x coordinate of interest
       y0 - y coordinate of interest"""
    assert img.shape[0] >= height
    assert img.shape[1] >= width
    assert img.shape[0] == mask.shape[0]
    assert img.shape[1] == mask.shape[1]

    x0 = floor(x0)
    y0 = floor(y0)
    
    while True:
        rx = randint(
            max(0, width - x0),
            min(width, img.shape[1] - x0)
        )
        ry = randint(
            max(0, height - y0),
            min(height, img.shape[0] - y0)
        )
        new_img = img[
            ((y0 + ry) - height) : (y0 + ry),
            ((x0 + rx) - width) : (x0 + rx)
        ]
        new_mask = mask[
            ((y0 + ry) - height) : (y0 + ry),
            ((x0 + rx) - width) : (x0 + rx)
        ]
        
        return (new_img, new_mask)

def randomCropBatch(number):
    img, mask = load_image_and_mask(number)
    x0 = meta[number][0]
    y0 = meta[number][1]
    idx = list(meta.keys()).index(number)
    print(f"Cropping {number}...")
    for i in range(NUM_SAMPLES_PER_FILE):
        n = idx * 1000 + i
        crop_img, crop_mask = randomCrop(img, mask, CROP_WIDTH, CROP_HEIGHT, x0, y0)
        if i == 0:
            print(f"{sample_dir_out}{n:04}.png")
            print(f"{mask_dir_out}{n:04}.png")
        cv2.imwrite(f"{sample_dir_out}{n:04}.png", crop_img)
        cv2.imwrite(f"{mask_dir_out}{n:04}.png", crop_mask)
    
    return True

if __name__ == "__main__":
    
    p = Pool(4)
    res = p.map(randomCropBatch, meta.keys())
