import json
import numpy as np
import cv2
from glob import glob

# Take the file name and remove *-mask.jpg part
def nameToKey(name):
    return name.split("-")[0].split("\\")[1]

def process_image(name):
    img = cv2.imread(name) # read image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # make black & white
    
    # img has shape (h, w)

    if img.any():
        # Compute average target location
        indices = img.nonzero()
        avg = [np.mean(indices[1]), np.mean(indices[0])]
        return (True, avg)
    else:
        return (False, None)

json_file = "./metadata.json"
files = glob("./samples/masks/*.jpg")

names = list(map(nameToKey, files))
out = list(map(process_image, files))

result = {}
for i in range(len(files)):
    if out[i][0]:
        result[names[i]] = out[i][1]

with open(json_file, "w") as f:
    json.dump(result, f)