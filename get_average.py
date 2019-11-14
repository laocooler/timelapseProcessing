import os
import numpy
import PIL
from PIL import Image


def rgb2gray(rgb):
    return numpy.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


sources_dir = "sources"
results_dir = "results"

# Access all PNG files in directory
allfiles = os.listdir(os.getcwd())
imlist = [filename for filename in allfiles if filename[-4:]
          in [".JPG"] and filename.startswith("G00")]

# N = 10
N = len(imlist)  # 10 # 185 #

# Assuming all images are the same size, get dimensions of first image
w, h = Image.open(imlist[0]).size

# Create a numpy array of floats to store the average (assume RGB images)
arr = numpy.zeros((N, h, w, 3), numpy.uint8)
gray = numpy.zeros((N, h, w), numpy.uint8)

# Build up average pixel intensities, casting each image as an array of floats
print("- Reading images")
for i, im in enumerate(imlist):
    if i == N:
        break

    # Store each image
    arr[i] = numpy.array(Image.open(im), dtype=numpy.uint8)
    gray[i] = rgb2gray(arr[i])

    if (i+1) % 10 == 0 or i == N-1:
        print('-', i + 1)

print("- Processing images")
for i in range(186, N+1):
    # if True:
    # i = N
    print('iteration', i)

    # Average
    avg = numpy.array(numpy.round(numpy.average(
        arr[:i], axis=0)), dtype=numpy.uint8)
    out = Image.fromarray(avg, mode="RGB")
    out.save(f"Average/_Average_{i}.png")

    # Max
    max = numpy.array(numpy.round(numpy.amax(
        arr[:i], axis=0)), dtype=numpy.uint8)
    out = Image.fromarray(max, mode="RGB")
    out.save(f"Max/_Max_{i}.png")

    # Average max gray
    print("- Getting mask")
    max_gray = numpy.amax(gray[:i], axis=0)
    out = Image.fromarray(numpy.array(
        numpy.round(max_gray), dtype=numpy.uint8), mode="L")
    out.save(f"Mask/_Mask_{i}.png")

    # Average gray
    avg_gray = numpy.array(numpy.round(
        numpy.average(gray[:i], axis=0)), dtype=numpy.uint8)
    out = Image.fromarray(avg_gray, mode="L")
    out.save(f"AverageGray/_AverageGray_{i}.png")

    # Average with weights
    if False:
        # print("- Getting average by mask")
        max_w = numpy.amax(max_gray)
        weights = max_gray / (max_w / 2) / N

        avg_weightened = numpy.zeros((h, w, 3), numpy.float)
        for j, im in enumerate(arr[:i]):
            if (j+1) % 10 == 0 or j == N-1:
                print('-', j+1)

            red, green, blue = im[:, :, 0], im[:, :, 1], im[:, :, 2]
            red_w = red * weights
            green_w = green * weights
            blue_w = blue * weights

            weightened = numpy.zeros((h, w, 3), numpy.float)
            weightened[:, :, 0], weightened[:, :,
                                            1], weightened[:, :, 2] = red_w, green_w, blue_w

            avg_weightened += weightened

        avg_weightened = numpy.array(
            numpy.round(avg_weightened), dtype=numpy.uint8)
        out = Image.fromarray(avg_weightened, mode="RGB")
        out.save(f"AverageWeightened/_AverageWeightened_{i}.png")

# colors = [[x * p for x in cs] for cs, p in zip(colors, probs)]

        # for ri,r in enumerate(im):
        #     if ri % 500 == 0 or i == N-1: print('-',i)

        #     for ci,c in enumerate(r):
        #         avg_weightened[ri][ci] += c * weights[ri][ci]

        # weightened = [[x * p for x in cs] for cs, p in zip(im, weights)]
        # avg_weightened += weightened

    # red, green, blue = arr[:i,:,:,0], arr[:i,:,:,1], arr[:i,:,:,2]
    # red_avg = numpy.array(numpy.round(numpy.average(red, axis=1, weights=weights)),dtype=numpy.uint8)
    # green_avg = numpy.array(numpy.round(numpy.average(green, axis=0, weights=weights)),dtype=numpy.uint8)
    # blue_avg = numpy.array(numpy.round(numpy.average(blue, axis=0, weights=weights)),dtype=numpy.uint8)

    # avg_weightened = numpy.zeros((h,w,3),numpy.uint8)
    # avg_weightened[:,:,0], avg_weightened[:,:,1], avg_weightened[:,:,2] = red_avg, green_avg, blue_avg

   # r1, g1, b1 = 40, 40, 40 # Light value
    # r2, g2, b2 = 255, 0, 0 # White value

    # red, green, blue = imarr[:,:,0], imarr[:,:,1], imarr[:,:,2]
    # mask = (red < r1) & (green < g1) & (blue < b1)
    # imarr[:,:,:3][mask] = [r2, g2, b2]
    # out=Image.fromarray(imarr,mode="RGB")
    # out.save(f"{count}.png")

    # colors = [list(p.get_ordered_colors()) for p in palettes]
    # probs = [probs[str(p.id)] for p in palettes]
    # colors = [[x * (p / sum(probs)) for x in cs] for cs, p in zip(colors, probs)]
    # colors = [sum(x, RgbColor()) for x in zip(*colors)]


# for i,_ in enumerate(arr):
#     for y,_ in enumerate (arr[i]):
#         for x,p in enumerate(arr[i][y]):

#             if (p[0]>t and p[1]>t and p[2]>t):
#                 res[y][x] = p
#             else:
#                 res[y][x] += p/count

# Round values in array and cast as 8-bit integer
# res=numpy.array(numpy.round(arr),dtype=numpy.uint8)


# colors = [[1,2],[3,4]]
# probs = [0.5,0.25]
# z = zip(colors, probs)

# colors = [[x * p for x in cs] for cs, p in zip(colors, probs)]

# stop = True


# gray = numpy.array(numpy.round(gray),dtype=numpy.float)
