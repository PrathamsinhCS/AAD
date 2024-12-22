import time
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(1500)

def loop(N):
    total = 0
    for i in range(1, N + 1):
        total += i
    return total

def equation(N):
    return N * (N + 1) // 2
 
def recursion(N):
    if N == 0:
        return 0
    else:
        return N + recursion(N - 1)

def main():
    try:
        N = int(input("Enter a value for N: "))
        if N < 0:
            print("Please enter a non-negative integer.")
            return
        
        start = time.time()
        loop_result = loop(N)
        loop_time = time.time() - start

        start = time.time()
        equation_result = equation(N)
        equation_time = time.time() - start

        if N <= 1000:  
            start = time.time()
            recursion_result = recursion(N)
            recursion_time = time.time() - start
            print(f"Sum using recursion: {recursion_result} (Time taken: {recursion_time:.6f} seconds)")
        else:
            print(f"Recursion skipped for N = {N} due to depth limit.")

        print(f"Sum using loop: {loop_result} (Time taken: {loop_time:.6f} seconds)")
        print(f"Sum using equation: {equation_result} (Time taken: {equation_time:.6f} seconds)")

    except ValueError:
        print("Invalid input. Please enter an integer.")

def practical_2():
    N_values = [10, 100, 500, 1000] 
    loop_time = []
    equation_time = []
    recursion_time = []

    for N in N_values:
        start_time = time.time()
        loop(N)
        loop_time.append(time.time() - start_time)

        start_time = time.time()
        equation(N)
        equation_time.append(time.time() - start_time)

        if N <= 1000:  
            start_time = time.time()
            recursion(N)
            recursion_time.append(time.time() - start_time)
        else:
            recursion_time.append(None) 

    plt.figure(figsize=(15, 10))
    
    plt.subplot(3, 1, 1)
    plt.plot(N_values, loop_time, marker='o', color='b', label='Loop')
    plt.xlabel('N')
    plt.ylabel('Time (seconds)')
    plt.title('Time Complexity of Loop Method')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.plot(N_values, equation_time, marker='o', color='r', label='Equation')
    plt.xlabel('N')
    plt.ylabel('Time (seconds)')
    plt.title('Time Complexity of Equation Method')
    plt.grid(True)
    plt.legend()
    
    plt.subplot(3, 1, 3)
    plt.plot(N_values[:len(recursion_time)], recursion_time, marker='o', color='g', label='Recursion')
    plt.xlabel('N')
    plt.ylabel('Time (seconds)')
    plt.title('Time Complexity of Recursion Method')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
    practical_2()
