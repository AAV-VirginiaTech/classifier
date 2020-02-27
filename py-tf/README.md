# Python/Tensorflow Image Processing Folder

This folder has the code for the target detection training/data generation modules.

# Setup

You will need a few packages to run these. It is easiest to install them from Anaconda/Miniconda to avoid cluttering your default Python installation.

## Dependencies:

- Tensorflow (>= 2.1.0)
- OpenCV 2
- Numpy
- Pytest
- Matplotlib (needed for graph visualizations)
- Jupyter (only if you plan on running the jupyter notebooks)

## Installation

1. Download Anaconda and install <https://www.anaconda.com/>

2. Open a terminal, and navigate so `conda` is in your PATH or working directory. Make a new environment with all the dependencies (or add them to an existing environment with `conda activate <env>` and `conda install`)

    ```
    conda create -n tf tensorflow=2.1.0 opencv numpy pytest matplotlib jupyter
    ```

    creates an environment named `tf`. If you have an Nvidia CUDA-compatible GPU and would like to use that while working with Tensorflow,

    ```
    conda create -n tf tensorflow-gpu=2.1.0 opencv numpy pytest matplotlib jupyter
    ```

# Usage

To run a script, you need to first need to activate the environment, `conda activate tf`.

## Getting samples

To download the samples, navigate to _AAV Team Drive > 2019 - 2020 | Season 3 > Software | S3 > Classification Data_ and download `samples.zip`. Extract the folder inside to your desired working directory. The rest of this guide will assume it's extracted to the current working directory, giving the folder `./samples`.

The sample directory should have the structure

```
../samples
  ../samples
    ../*.JPG
  ../masks
    ../*-mask.JPG
  ../metadata.json
```

## Adding samples

To add a sample, place the original file `0123456.JPG` into the `./samples/samples` folder. Then, place the _binary mask_ (obtained through GIMP or something) named `0123456-mask.JPG` into the `./samples/masks` directory. Note: the numbers in the file names should match.

## Generating sample metadata

Typically, the samples will have a metadata file packaged with them when downloaded from Google Drive. However, if you wish to regenerate the metadata (e.g. added new image pairs), you can use

```
python genmetadata.py ./samples
```

and this will create a new metadata file (or overwrite the old one) at `./samples/metadata.json`.

## Creating a dataset

To create a dataset, use the `create_sample_images.py` file. (Note: you can probably find a dataset of `data.zip` under _AAV Team Drive > 2019 - 2020 | Season 3 > Software | S3 > Classification Data_.)

```
python create_sample_images.py [-val <%>] [-e <%>] [-p] [-x <width>] [-y <height>] [-o <dir>] [-i <dir>] N
```

Required parameters:
- `N`: Number of total image/mask pairs to generate

Optional parameters:
- `-val <%>`: Percent of total generated images to be made into a validation set. Default is 10.0.
- `-e <%>`: Percent of total images that should be empty (i.e. don't have a target present). Default is 50.0.
- `-p`: Permute the dataset. Setting this flag will apply random transformations/augmentations to the training set. Useful since we have a small dataset. This can also be done during training; however, doing it now will save time
- `-x <width>`: Width of each training sample. Default is 256.*
- `-y <height>`: Height of each training sample. Default is 256.*
- `-o <dir>`: Output generated data set to `<dir>`. Default is `./data`.
- `i <dir>`: Location of samples. Default is `./samples`.

\* These should be sufficient powers of 2 since the U-Net architecture halves the resolution several times.

## Training/Inference

TODO