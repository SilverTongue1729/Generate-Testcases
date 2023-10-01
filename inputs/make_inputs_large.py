import numpy as np
import random
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py output_file.txt")
    sys.exit(1)

output_file = sys.argv[1]

with open(output_file, 'w') as f:
    # Redirect stdout to the file
    sys.stdout = f
    
    #-- TC 1
    t = 1000
    print(f"{t}")
    for _ in range(t):
        n = 200
        print(f"{n}")
        array = "1 " * n
        print(array.strip())
    print()
    
    #-- TC 2
    t = 10000
    print(f"{t}")
    for _ in range(t):
        n = 20
        print(f"{n}")
        print(" 1 1 1 2 1 1 2 1000000000 100000000 1 1 4 1 1 1 100000 1 8 1 1000000000")
    print()
    
    #-- TC 3
    t = 1
    print(f"{t}")
    for _ in range(t):
        n = 200000
        print(f"{n}")
        array = "1 2 " * int(n/2)
        print(array.strip())
    print()
    
    #-- TC 4
    t = 1
    print(f"{t}")
    for _ in range(t):
        n = 200000
        print(f"{n}")
        array = "1000000000 " * n
        print(array.strip())
    print()
    
    #-- TC 5
    t = 1
    print(f"{t}")
    for _ in range(t):
        n = 200000
        print(f"{n}")
        array = np.random.randint(1, n*2, n)
        print(" ".join(map(str, array)))
    print()
        

# Reset stdout to its original value (the console)
sys.stdout = sys.__stdout__
