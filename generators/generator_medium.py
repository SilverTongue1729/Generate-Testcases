import numpy as np
import random
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py output_file.txt")
    sys.exit(1)

output_file = sys.argv[1]

t_vals = [10, 10]

with open(output_file, 'w') as f:
    # Redirect stdout to the file
    sys.stdout = f

    for ind, t in enumerate(t_vals):
        print(f"{t}")

        if ind == 1:
            for _ in range(t):
                n = 1000
                print(f"{n}")
                array = "1 " * n
                print(array.strip())
        else:
            n_vals = np.random.randint(500, 1000, t)
            for n in n_vals:
                print(f"{n}")
                array = np.random.randint(1, n*2, n)
                print(" ".join(map(str, array)))

        print()


# Reset stdout to its original value (the console)
sys.stdout = sys.__stdout__
