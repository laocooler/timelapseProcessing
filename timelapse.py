import os
import numpy
import PIL
from PIL import Image

# Convert an rgb image to a grayscale one
def rgb2gray(rgb):
    return numpy.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

def create_dir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def process_images(name, func, images_arr, grayscale = False):
    create_dir_if_not_exists(f'{results_dir}/{name}')

    result_image = func(images_arr)
    out = Image.fromarray(result_image, mode=("L" if grayscale == True else "RGB"))
    out.save(f"{results_dir}/{name}/{name}_{i}.png")

def average(images_arr):
    return numpy.array(numpy.round(numpy.average(images_arr, axis=0)), dtype=numpy.uint8)

def maximize(images_arr):
    return numpy.array(numpy.round(numpy.amax(images_arr, axis=0)), dtype=numpy.uint8)

# Paths
sources_dir = "sources"
results_dir = "results"

create_dir_if_not_exists(results_dir)

# Access all image files in the source directory
imlist = [f"{sources_dir}/{filename}" for filename in os.listdir(sources_dir)]
N = len(imlist)

# Assume all images are of the same size, get dimensions of first image
# Assert that all images are of the same size
w, h = Image.open(imlist[0]).size
for i in range(1, N):
    assert(w,h == Image.open(imlist[i]).size)

# Create a numpy array of floats to store the average of grayscale and color images
color_arr = numpy.zeros((N, h, w, 3), numpy.uint8)
grayscale_arr = numpy.zeros((N, h, w), numpy.uint8)

# Build up average pixel intensities, casting each image as an array of floats
print("- Reading images")
for i, im in enumerate(imlist):
    if i == N:
        break

    # Store each image
    color_arr[i] = numpy.array(Image.open(im), dtype=numpy.uint8)
    grayscale_arr[i] = rgb2gray(color_arr[i])

    if (i+1) % 10 == 0 or i == N-1:
        print('-', i + 1)

print("- Processing images")
for i in range(1, N):
    # if True:
    # i = N
    print('iteration', i)

    # Average color images
    process_images('average', average, color_arr[:i])

    # Maximize color images
    process_images('max', maximize, color_arr[:i])

    # Average gray
    process_images('average_gray', average, grayscale_arr[:i], grayscale=True)

    # Max gray
    process_images('average_max', maximize, grayscale_arr[:i], grayscale=True)