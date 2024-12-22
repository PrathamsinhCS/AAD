from flask import Flask, request, render_template, Response
import time
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import sys

app = Flask(__name__)
sys.setrecursionlimit(1000000)

def sum_using_loop(N):
    total = 0
    for i in range(1, N + 1):
        total += i
    return total

def sum_using_equation(N):
    return N * (N + 1) // 2

def sum_using_recursion(N):
    if N == 1:
        return 1
    return N + sum_using_recursion(N - 1)

def measure_time(func, N):
    start_time = time.time()
    try:
        result = func(N)
    except RecursionError:
        return float('inf'), None
    end_time = time.time()
    return end_time - start_time, result

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        try:
            N = int(request.form["N"])
            if N < 0:
                return render_template("index.html", error="Please enter a non-negative integer.")

            loop_time, loop_result = measure_time(sum_using_loop, N)
            equation_time, equation_result = measure_time(sum_using_equation, N)
            recursion_time, recursion_result = measure_time(sum_using_recursion, N)

            recursion_data = (recursion_result, recursion_time) if recursion_result is not None else ("Skipped due to depth limit", None)

            return render_template(
                "index.html",
                N=N,
                loop_data=(loop_result, loop_time),
                equation_data=(equation_result, equation_time),
                recursion_data=recursion_data,
            )
        except ValueError:
            return render_template("index.html", error="Invalid input. Please enter an integer.")
    return render_template("index.html")

@app.route("/practical_2.png")
def practical_2():
    input_sizes = [100, 1000, 5000, 10000, 20000, 50000, 100000]
    loop_times = []
    equation_times = []
    recursion_times = []

    for size in input_sizes:
        loop_times.append(measure_time(sum_using_loop, size)[0])
        equation_times.append(measure_time(sum_using_equation, size)[0])
        recursion_times.append(measure_time(sum_using_recursion, size)[0])

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(input_sizes, loop_times, label='Loop', marker='o')
    ax.plot(input_sizes, equation_times, label='Equation', marker='o')
    ax.plot(input_sizes, recursion_times, label='Recursion', marker='o')
    ax.set_xlabel('Input Size (N)')
    ax.set_ylabel('Execution Time (seconds)')
    ax.set_title('Comparison of Execution Time for Sum of 1 to N')
    ax.legend()
    ax.grid(True)

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
