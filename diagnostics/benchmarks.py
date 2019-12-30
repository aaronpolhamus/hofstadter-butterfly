import timeit

RESOLUTIONS = range(100, 1100, 100)
REPETITIONS = 3

if __name__ == '__main__':
    with open('/tmp/runtimes.csv', 'a') as outfile:
        outfile.write('resolution,avg_time\n')
        for res in RESOLUTIONS:
            for rep in range(REPETITIONS):
                print(f'Calculating runtime for resolution {res} x {res} pixels...')
                time = timeit.timeit(f"os.system('python butterfly.py --res {res}')", setup='import os', number=1)
                print(f'Run time of {time} seconds')
                outfile.write(f'{res},{time}\n')
                outfile.flush()
