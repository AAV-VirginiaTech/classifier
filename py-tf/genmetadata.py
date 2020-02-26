import json
import numpy as np
import cv2
from glob import glob
import argparse
from pathlib import Path
from multiprocessing import Pool

def get_args(args=None):
    """
    Parses the command line args according to
    $ python genmetadata.py [dir]
    """
    parser = argparse.ArgumentParser(description='Creates metadata for samples for later use in create_sample_images.py')
    parser.add_argument('dir', type=str, default='./samples',
                        help="Input directory of initial samples to process")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help="Verbose output")
    return parser.parse_args() if args is None else parser.parse_args(args)

# Take the file name and remove *-mask part
def nameToKey(name):
    return name.split("-")[0]

def process_image(path):
    """
    Computes average target location of an image (or returns [-1, -1] if there is no target in the mask)
    """
    name = str(path)
    img = cv2.imread(name) # read image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # make black & white
    
    # img has shape (h, w)

    if img.any():
        # Compute average target location
        indices = img.nonzero()
        avg = [np.mean(indices[1]), np.mean(indices[0])]
        return avg
    else:
        return [-1, -1]

if __name__ == "__main__":
    args = get_args()
    samples_dir = Path(args.dir)

    # Obviously we can't do anything if the path doesn't exist
    assert samples_dir.exists()

    # Metadata output file
    json_file = samples_dir / 'metadata.json'

    # Detected sample files
    files = list((samples_dir / 'masks').glob("*.jpg"))

    if args.verbose:
        print("Detected files: ")
        for f in files:
            print(f'- {f}')

    # Directory is empty and has no samples
    assert len(files) > 0

    names = [nameToKey(x.stem) for x in files]

    # Use multiprocessing to speed this stuff up
    p = Pool(4)
    out = p.map(process_image, files)

    # Create metadata
    result = {}
    for pair in zip(names, out):
        result[pair[0]] = pair[1]

    # Write metadata
    with open(json_file, "w") as f:
        json.dump(result, f)