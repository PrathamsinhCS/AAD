import time
import matplotlib.pyplot as plt

def iterative(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

def recursive(n):
    if n <= 1:
        return 1
    else:
        return recursive(n - 1) + recursive(n - 2)

def main():
    try:
        months = int(input("Enter the number of months (up to 12 for 1 year): "))
        if months < 1 or months > 12:
            print("Please enter a value between 1 and 12.")
            return
        
        start = time.time()
        iterative_result = iterative(months)
        iterative_time = time.time() - start

        start = time.time()
        recursive_result = recursive(months)
        recursive_time = time.time() - start

        print(f"Number of rabbit pairs after {months} months (iterative): {iterative_result} (Time taken: {iterative_time:.6f} seconds)")
        print(f"Number of rabbit pairs after {months} months (recursive): {recursive_result} (Time taken: {recursive_time:.6f} seconds)")

    except ValueError:
        print("Invalid input. Please enter an integer.")

def practical_2():
    months_values = range(1, 13)
    iterative_time = []
    recursive_time = []

    for months in months_values:
        start_time = time.perf_counter()
        iterative(months)
        end_time = time.perf_counter()
        iterative_time.append(end_time - start_time)

        start_time = time.perf_counter()
        recursive(months)
        end_time = time.perf_counter()
        recursive_time.append(end_time - start_time)

    plt.figure(figsize=(12, 6))
    plt.plot(months_values, iterative_time, marker='o', color='b', label='Iterative')
    plt.xlabel('Number of Months')
    plt.ylabel('Time (seconds)')
    plt.title('Time Complexity of Iterative Method')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(months_values, recursive_time, marker='o', color='r', label='Recursive')
    plt.xlabel('Number of Months')
    plt.ylabel('Time (seconds)')
    plt.title('Time Complexity of Recursive Method')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
    practical_2()
