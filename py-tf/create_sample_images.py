# Numerical imports
import numpy as np
import cv2

# File I/O imports
from pathlib import Path
import shutil
import json

# Misc
from random import randint, random
from math import floor
import argparse
from multiprocessing import Pool
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_args(args=None):
    """
    Parses the command line args according to
    $ python create_sample_images.py [-v] [-val <%>] [-e <%>] [-p] [-x <width>] [-y <height>] [-o <dir>] [-i <dir>] N
    """
    parser = argparse.ArgumentParser(description='Generates training/validation data')
    parser.add_argument('-v', action="store_true",
                        help="Enable verbose logging")
    parser.add_argument('-val', action='store', type=float, default=10.0,
                        help="Percent of samples to make validation")
    parser.add_argument('--empty', '-e', action='store', type=float, default=50.0,
                        help="Percent of samples that are empty")
    parser.add_argument('--permute', '-p', action='store_true',
                        help='Whether or not to permute/mutate training data samples')
    parser.add_argument('--width', '-x', action='store', type=int, default=256,
                        help='width of each sample')
    parser.add_argument('--height', '-y', action='store', type=int, default=256,
                        help='Height of each sample')
    parser.add_argument('--output', '-o', type=str, default='./data',
                        help="Output directory for samples")
    parser.add_argument('--input', '-i', type=str, default='./samples',
                        help="Input directory of initial samples to process")
    parser.add_argument('samples', metavar="N", type=int,
                        help="Number of training samples")
    
    return parser.parse_args() if args is None else parser.parse_args(args)

def prepare_directories(out_dir, in_dir, delete_if_exists=True):
    # Define the input and output directories
    # Note: the /data on the end is necessary for the Keras ImageDataGenerator during training
    # Output file structure:
    #
    # ../data_dir
    #   ../train
    #     ../samples/data
    #     ../masks/data
    #   ../validation
    #     ../samples/data
    #     ../masks/data
    in_dir_path = Path(in_dir)
    data_dir = Path(out_dir)
    train_dir = data_dir / 'train'
    val_dir = data_dir / 'validation'

    # Clear output directory if it exists, mostly to prevent keeping old samples
    if data_dir.exists():
        shutil.rmtree(data_dir)
    
    in_dirs = {
        "top": in_dir_path,
        "samples": in_dir_path / 'samples',
        "masks": in_dir_path / 'masks'
    }

    out_dirs = {
        "top": data_dir,
        "train": train_dir,
        "train_samples": train_dir / 'samples' / 'data',
        "train_masks": train_dir / 'masks' / 'data',
        "val": val_dir,
        "val_samples": val_dir / 'samples' / 'data',
        "val_masks": val_dir / 'masks' / 'data'
    }

    # Make output directories
    for folder in out_dirs.values():
        folder.mkdir(parents=True)
    
    return (in_dirs, out_dirs)


def load_image_and_mask(number, samples_dict, verbose=False):
    """Returns image and mask corresponding to the particular number in the file with shape (h, w)"""

    if verbose:
        print(f"Loading file {number}..")

    img = cv2.imread(
        str(samples_dict["samples"] / f"{number}.JPG"), 
        cv2.IMREAD_GRAYSCALE
    )
    mask = cv2.imread(
        str(samples_dict["masks"] / f"{number}-mask.JPG"),
        cv2.IMREAD_GRAYSCALE
    )

    return (img, mask)

def randomCropGenerator(n, img, mask, width, height, x0, y0):
    """
    Creates a generator yielding random crops with x0, y0 guaranteed to be somewhere in the crop

    Parameters:
        img: image to crop
        mask: corresponding mask
        width: crop width
        height: crop height
        x0: x coordinate of interest
        y0: y coordinate of interest
    """
    assert img.shape[0] >= height
    assert img.shape[1] >= width
    assert img.shape[0] == mask.shape[0]
    assert img.shape[1] == mask.shape[1]

    x0 = floor(x0)
    y0 = floor(y0)
    
    for _ in range(n):
        if x0 >= 0 and y0 >= 0:
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
            
            yield (new_img, new_mask)
        else:
            rx = randint(0, img.shape[1] - width - 1)
            ry = randint(0, img.shape[0] - height - 1)
            new_img = img[rx:rx+width, ry:ry+height]
            new_mask = mask[rx:rx+width, ry:ry+height]

            yield (new_img, new_mask)

def randomCropBatch(param, idx, target):
    img, mask = load_image_and_mask(param["number"], param["in_dir"], param["verbose"])
    center = param["loc"]
    x0 = center[0] if target else -1
    y0 = center[1] if target else -1
    
    num = param["number"]

    if param["verbose"]:
        print(f"[{num}] Cropping, target = {target}...")

    label = idx
    n_validation = 0

    N = param["ntarget"] if target else param["N"] - param["ntarget"]

    mutations = dict(rescale = 1./255,
                rotation_range=90,
                width_shift_range=0.1,
                height_shift_range=0.1,
                zoom_range=0.2,
                horizontal_flip=True,
                vertical_flip=True)
    permutor = ImageDataGenerator(**mutations)

    for crop_img, crop_mask in randomCropGenerator(N, img, mask, param["width"], param["height"], x0, y0):
        # Save validation image
        if random() < param['val']:
            n_validation += 1
            cv2.imwrite(str(param["out_dir"]["val_samples"] / f"{label}.png"), crop_img)
            cv2.imwrite(str(param["out_dir"]["val_masks"] / f"{label}.png"), crop_mask)
        # Save training image
        else:
            # Mutate image and mask
            if param['permute']:
                # Expand dimension to (h, w, 1) to make compatible with tensorflow
                crop_img = np.expand_dims(crop_img, axis=2)
                crop_mask = np.expand_dims(crop_mask, axis=2)
                
                # Create random transformation
                transformation = permutor.get_random_transform(crop_img.shape)

                # Apply transformation
                crop_img = permutor.apply_transform(crop_img, transformation)
                crop_mask = permutor.apply_transform(crop_mask, transformation)

                # Remove third dimension
                crop_img = np.squeeze(crop_img)
                crop_mask = np.squeeze(crop_mask)

            cv2.imwrite(str(param["out_dir"]["train_samples"] / f"{label}.png"), crop_img)
            cv2.imwrite(str(param["out_dir"]["train_masks"] / f"{label}.png"), crop_mask)
        
        label += 1
    
    if param["verbose"]:
        print(f"[{num}] Created {N} images, {n_validation * 100.0 / N:.2f}% validation")
    
    return True

def execute(param):
    """
    Main function that does everything for each set of parameters
    """
    # do images with target
    randomCropBatch(param, param["idx"], target=True)
    # do images without target
    randomCropBatch(param, param["idx"] + param["ntarget"], target=False)


def _compute(N, e, n, m, k):
    """Used in distribution"""
    assert e >= 0 and e <= 1
    assert k >= 0 and k <= 1

    d = (N * e) / (n * (1-k) + m * k)

    pn = N * (1 - e) / n + (1 - k) * d
    pm = k * d

    pn = round(pn)
    pm = round(pm)

    return (pn, pm)

if __name__ == "__main__":

    args = get_args()

    # Extract parameters
    N = args.samples
    PERCENT_VALIDATION = args.val
    PERMUTE = args.permute
    CROP_WIDTH = args.width
    CROP_HEIGHT = args.height
    OUTPUT_DIR_PATH = args.output
    INPUT_DIR_PATH = args.input
    PERCENT_EMPTY = args.empty
    VERBOSE = args.v
    
    in_dirs, out_dirs = prepare_directories(OUTPUT_DIR_PATH, INPUT_DIR_PATH)

    # Load target location metadata
    with open(in_dirs["top"] / 'metadata.json', "r") as f:
        meta = json.load(f)

    # Compute the generation load for each source type
    e = PERCENT_EMPTY / 100
    target_sources = {k: meta[k] for k in meta.keys() if meta[k] != [-1, -1]} # images with a target
    blank_sources = {k: meta[k] for k in meta.keys() if meta[k] == [-1, -1]} # images without a target
    n = len(target_sources)
    m = len(blank_sources)

    pn, pm = _compute(N, e, n, m, 0.6)

    if VERBOSE:
        print(target_sources)
        print(blank_sources)

    # Prepare parameters for each process
    params = []
    for idx, num in enumerate(target_sources.keys()):
        param = {
            "number": num,
            "loc": target_sources[num],
            "N": pn,
            "e": e,
            "ntarget": round(N * (1-e) / n),
            "val": PERCENT_VALIDATION/100,
            "idx": idx * pn,
            "in_dir": in_dirs,
            "out_dir": out_dirs,
            "verbose": VERBOSE,
            "permute": PERMUTE,
            "height": CROP_HEIGHT,
            "width": CROP_WIDTH
        }

        params.append(param)
    
    for idx, num in enumerate(blank_sources.keys()):
        param = {
            "number": num,
            "loc": blank_sources[num],
            "N": pm,
            "e": 1,
            "ntarget": 0,
            "val": PERCENT_VALIDATION/100,
            "idx": idx * pm + n * pn,
            "in_dir": in_dirs,
            "out_dir": out_dirs,
            "verbose": VERBOSE,
            "permute": PERMUTE,
            "height": CROP_HEIGHT,
            "width": CROP_WIDTH
        }

        params.append(param)

    p = Pool(4)
    res = p.map(execute, params)
