from flask import Flask, render_template, request
import time
import random
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def bubblesort(arr):
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(n-i-1):
            count += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return count

def insertionsort(arr):
    n = len(arr)
    count = 0
    for i in range(1, n):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            count += 1
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return count

def count(sort_function, arr):
    start_time = time.time()
    count = sort_function(arr.copy())
    end_time = time.time()
    elapsed_time = end_time - start_time
    return count, elapsed_time

def graph(size, bubblecount, insertioncount, bubbletime, insertiontime):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    ax1.plot(size, bubblecount, label='Bubble Sort', marker='o', color='b')
    ax1.plot(size, insertioncount, label='Insertion Sort', marker='s', color='g')
    ax1.set_xlabel('Number of Elements')
    ax1.set_ylabel('Number of Comparisons')
    ax1.set_title('Comparison of Sorting Algorithms')
    ax1.legend()
    ax1.grid(True)

    ax2.plot(size, bubbletime, label='Bubble Sort', marker='o', color='b')
    ax2.plot(size, insertiontime, label='Insertion Sort', marker='s', color='g')
    ax2.set_xlabel('Number of Elements')
    ax2.set_ylabel('Execution Time (seconds)')
    ax2.set_title('Time Complexity')
    ax2.legend()
    ax2.grid(True)
    
    
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)
    
    return plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        userinput = request.form['sizes']
        try:
            data_sizes = [int(size.strip()) for size in userinput.split(',')]
            if all(size > 0 for size in data_sizes):
                bubblecounts = []
                insertioncounts = []

                bubbletimes = []
                insertiontimes = []

                results = []

                for size in data_sizes:
                    arr = [random.randint(1, 10000) for _ in range(size)]
                    bubblecount, bubbletime = count(bubblesort, arr)
                    insertioncount, insertiontime = count(insertionsort, arr)

                    bubblecounts.append(bubblecount)
                    insertioncounts.append(insertioncount)

                    bubbletimes.append(bubbletime)
                    insertiontimes.append(insertiontime)

                    results.append({
                        'size': size,
                        'bubblecount': bubblecount,
                        'bubbletime': bubbletime,
                        'insertioncount': insertioncount,
                        'insertiontime': insertiontime
                    })

                plot_url = graph(data_sizes, bubblecounts, insertioncounts, bubbletimes, insertiontimes)

                return render_template('index.html', results=results, plot_url=plot_url)
            else:
                error = "Please enter positive values."
                return render_template('index.html', error=error)
        except ValueError:
            error = "Invalid input. Please enter a number."
            return render_template('index.html', error=error)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
