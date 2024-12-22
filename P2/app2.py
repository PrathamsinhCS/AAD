from flask import Flask, request, render_template, Response
import time
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_recursive(n):
    if n <= 1:
        return n
    if n > 30: 
        raise RecursionError("Recursion depth limit exceeded.")
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

def measure_time(func, n):
    start_time = time.time()
    try:
        result = func(n)
        if isinstance(result, int):  
            end_time = time.time()
            return end_time - start_time, result
        else:
            return float('inf'), None
    except RecursionError:
        return float('inf'), None

@app.route("/", methods=["GET", "POST"])
def main():
    iterative_data = None
    recursive_data = None
    n = None
    error = None

    if request.method == "POST":
        try:
            n = int(request.form["n"])
            if n < 0:
                error = "Please enter a non-negative integer."
            else:
                iterative_time, iterative_result = measure_time(fibonacci_iterative, n)
                recursive_time, recursive_result = measure_time(fibonacci_recursive, n)
                iterative_data = (iterative_result, iterative_time)
                if recursive_result is None:
                    recursive_data = (None, float('inf'))
                else:
                    recursive_data = (recursive_result, recursive_time)
        except ValueError:
            error = "Invalid input. Please enter an integer."

    return render_template(
        "index2.html",
        n=n,
        iterative_data=iterative_data,
        recursive_data=recursive_data,
        error=error
    )

@app.route("/practical_2.png")
def practical_2():
    input_sizes = [5, 10, 15, 20, 25, 30, 35]
    iterative_times = []
    recursive_times = []

    for size in input_sizes:
        iterative_times.append(measure_time(fibonacci_iterative, size)[0])
        recursive_times.append(measure_time(fibonacci_recursive, size)[0])

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(input_sizes, iterative_times, label='Iterative', marker='o')
    ax.plot(input_sizes, recursive_times, label='Recursive', marker='o')
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Comparison of Execution Time for Fibonacci Calculation')
    ax.legend()
    ax.grid(True)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
