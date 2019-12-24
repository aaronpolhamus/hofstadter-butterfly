# Hofstadter Butterfly Fractal
# http://en.wikipedia.org/wiki/Hofstadter%27s_butterfly
# Wolfgang Kinzel/Georg Reents,"Physics by Computer" Springer Press (1998)
# FB36 - 20130922
import argparse
import math
from multiprocessing import Pool, cpu_count

from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--res", help="How many pixels should the length/width axes have? (l x w)",
                    type=int, default=200)
parser.add_argument("--out_path", help="Where would you like to print this thing?",
                    type=str, default='/tmp/butterly.png')
args = parser.parse_args()


def flatten_list_of_lists(ls):
    return [item for sublist in ls for item in sublist]


def apply_parallel(func, argument_tuples_iterator, n_workers=None):
    """See https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
    The arguments for each run must be packaged up as a tuple and bundled together in an iterator prior to pass in.
    For apply operations on group data frame, this means that each argument tuple should have a data frame corresponding
    to one of the groups
    """
    if not n_workers:
        n_workers = cpu_count()

    with Pool(n_workers) as pool:
        results = pool.starmap(func, argument_tuples_iterator)

    return results


def gcd(a, b):  # Greatest Common Divisor
    if b == 0:
        return a
    return gcd(b, a % b)


def get_color(polynew, polyold):
    poly_ls = [abs(polynew), abs(polyold)]
    poly_ls.sort()
    poly_delta = abs(poly_ls[0] - poly_ls[1])
    r = int(255 * poly_delta / poly_ls[1])
    b = int(255 * math.log(poly_ls[0] / poly_ls[1] + 1) / math.log(2))
    g = int(abs(r - b))
    return r, g, b


def pixel_generator(p, q, qmax):
    pi2 = math.pi * 2.0
    maxx = maxy = qmax + 1
    try:
        if gcd(p, q) <= 1:
            sigma = pi2 * p / q
            nold = 0
            locations_and_colors = list()
            for ie in range(0, maxy + 2):
                e = 8.0 * ie / maxy - 4.0 - 4.0 / maxy
                n = 0
                polyold = 1.0
                poly = 2.0 * math.cos(sigma) - e
                if polyold * poly < 0.0:
                    n += 1

                for m in range(2, int(q / 2)):
                    polynew = (2.0 * math.cos(sigma * m) - e) * poly - polyold
                    if poly * polynew < 0.0:
                        n += 1
                    polyold = poly
                    poly = polynew

                polyold = 1.0
                poly = 2.0 - e
                if polyold * poly < 0.0:
                    n += 1
                polynew = (2.0 * math.cos(sigma) - e) * poly - 2.0 * polyold
                if poly * polynew < 0.0:
                    n += 1
                polyold = poly
                poly = polynew

                for m in range(2, int(q / 2)):
                    polynew = (2.0 * math.cos(sigma * m) - e) * poly - polyold
                    if poly * polynew < 0.0:
                        n += 1
                    polyold = poly
                    poly = polynew

                polynew = (2.0 * math.cos(sigma * q / 2.0) - e) * poly - 2.0 * polyold
                if poly * polynew < 0.0:
                    n += 1

                polyold = 1.0
                poly = 2.0 - e
                if polyold * poly < 0.0:
                    n += 1
                polynew = (2.0 * math.cos(sigma) - e) * poly - 2.0 * polyold
                if poly * polynew < 0.0:
                    n += 1
                polyold = poly
                poly = polynew

                for m in range(2, int(q / 2)):
                    polynew = (2.0 * math.cos(sigma * m) - e) * poly - polyold
                    if poly * polynew < 0.0:
                        n += 1
                    polyold = poly
                    poly = polynew

                polynew = (2.0 * math.cos(sigma * q / 2.0) - e) * poly - 2.0 * polyold
                if poly * polynew < 0.0:
                    n += 1
                if n > nold:
                    locations_and_colors.append((int(maxy - ie), int(maxx * p / q), get_color(polynew, polyold)))
                    locations_and_colors.append((int(maxx * p / q), int(maxy - ie), get_color(polynew, polyold)))
                nold = n
            return locations_and_colors
        return None
    except:
        return None


if __name__ == '__main__':
    img_size = args.res

    # make argument space to parallelize function over
    arg_tups = []
    for Q in range(4, img_size, 2):
        for P in range(1, Q, 2):
            arg_tups.append((P, Q, img_size))

    # parallel process lists of locations and colors
    list_of_lists = apply_parallel(pixel_generator, arg_tups)

    # flatten list and send to image map
    list_of_lists = [ls for ls in list_of_lists if ls is not None]
    colors_and_coordinates = flatten_list_of_lists(list_of_lists)

    image = Image.new("RGB", (img_size, img_size))
    pixels = image.load()
    for color_and_coord in colors_and_coordinates:
        pixels[color_and_coord[0], color_and_coord[1]] = color_and_coord[2]

    image.save(args.out_path, "PNG")
