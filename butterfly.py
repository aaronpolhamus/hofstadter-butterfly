# Hofstadter Butterfly Fractal
# http://en.wikipedia.org/wiki/Hofstadter%27s_butterfly
# Wolfgang Kinzel/Georg Reents,"Physics by Computer" Springer Press (1998)
# FB36 - 20130922
import math
from multiprocessing import Pool, cpu_count
from PIL import Image
imgSize = 300
image = Image.new("RGB", (imgSize, imgSize))
pixels = image.load()

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

def gcd(a, b): # Greatest Common Divisor
    if b == 0: return a
    return gcd(b, a % b)

def get_color(polynew, polyold):
    poly_ls = [abs(polynew), abs(polyold)]
    poly_ls.sort()
    poly_delta = abs(poly_ls[0] - poly_ls[1])
    r = int(255 * poly_delta / poly_ls[1])
    ratio = poly_ls[0] / poly_ls[1]
    b = int(255 * math.log(ratio + 1) / math.log(2))
    g = int(abs(r - b))
    return r, g, b

if __name__ == '__main__':
    pi2 = math.pi * 2.0
    MAXX = imgSize + 1
    MAXY = imgSize + 1
    qmax = imgSize
    for q in range(4, qmax, 2):
        print(str(100 * q / qmax).zfill(2) + "%")
        for p in range(1, q, 2):
            if gcd(p, q) <= 1:
                sigma = pi2 * p / q
                nold = 0
                ie = 0
                for ie in range(0, MAXY + 2):
                    e = 8.0 * ie / MAXY - 4.0 - 4.0 / MAXY
                    n = 0
                    polyold = 1.0
                    poly = 2.0 * math.cos(sigma) - e
                    if polyold * poly < 0.0: n += 1

                    for m in range(2, int(q / 2)):
                        polynew = (2.0 * math.cos(sigma * m) - e) * poly - polyold
                        if poly * polynew < 0.0: n += 1
                        polyold = poly
                        poly = polynew

                    polyold = 1.0
                    poly = 2.0 - e
                    if polyold * poly < 0.0: n += 1
                    polynew = (2.0 * math.cos(sigma) - e) * poly - 2.0 * polyold
                    if poly * polynew < 0.0: n += 1
                    polyold = poly
                    poly = polynew

                    for m in range(2, int(q / 2)):
                        polynew = (2.0 * math.cos(sigma * m) - e) * poly - polyold
                        if poly * polynew < 0.0: n += 1
                        polyold = poly
                        poly = polynew

                    polynew = (2.0 * math.cos(sigma * q / 2.0) - e) * poly - 2.0 * polyold
                    if poly * polynew < 0.0: n += 1

                    polyold = 1.0
                    poly = 2.0 - e
                    if polyold * poly < 0.0: n += 1
                    polynew = (2.0 * math.cos(sigma) - e) * poly - 2.0 * polyold
                    if poly * polynew < 0.0: n += 1
                    polyold = poly
                    poly = polynew

                    for m in range(2, int(q / 2)):
                        polynew = (2.0 * math.cos(sigma * m) - e) * poly - polyold
                        if poly * polynew < 0.0: n += 1
                        polyold = poly
                        poly = polynew

                    polynew = (2.0 * math.cos(sigma * q / 2.0) - e) * poly - 2.0 * polyold
                    if poly * polynew < 0.0: n += 1
                    if n > nold:
                        pixels[int(MAXY - ie), int(MAXX * p / q)] = get_color(polynew, polyold)
                        pixels[int(MAXX * p / q), int(MAXY - ie)] = get_color(polynew, polyold)
                    nold = n

    image.save("/Users/aaronpolhamus/Downloads/HofstadterButterflyFractal_cached.png", "PNG")
