from flask import Flask, request, render_template_string
import time
import matplotlib.pyplot as plt
import io
import base64
from random import randint, choice

app = Flask(__name__)

# Sample employee data (1000 employees generated for the example)
designations = ['Developer', 'Manager', 'Intern', 'Analyst', 'Engineer']
employees = [
    {
        'id': i, 
        'name': f'Employee_{i}', 
        'salary': randint(30000, 150000), 
        'age': randint(20, 60),
        'mobile': f'{randint(6000000000, 9999999999)}',
        'designation': choice(designations)
    } for i in range(1, 1001)  # 1000 employee records
]

# Sorting employee data for binary search
employees_by_salary = sorted(employees, key=lambda x: x['salary'])
employees_by_age = sorted(employees, key=lambda x: x['age'])

# Linear Search
def linear_search(employees, key, value):
    start_time = time.perf_counter()
    for employee in employees:
        if employee[key] == value:
            end_time = time.perf_counter()
            return employee, (end_time - start_time)
    end_time = time.perf_counter()
    return None, (end_time - start_time)

# Recursive Binary Search
def binary_search_recursive(employees, key, value, low, high):
    if high >= low:
        mid = (high + low) // 2
        if employees[mid][key] == value:
            return mid
        elif employees[mid][key] > value:
            return binary_search_recursive(employees, key, value, low, mid - 1)
        else:
            return binary_search_recursive(employees, key, value, mid + 1, high)
    else:
        return None

def binary_search(employees, key, value):
    start_time = time.perf_counter()
    index = binary_search_recursive(employees, key, value, 0, len(employees) - 1)
    end_time = time.perf_counter()
    if index is not None:
        return employees[index], (end_time - start_time)
    else:
        return None, (end_time - start_time)

# Use Cases
def search_highest_salary():
    highest_salary = max(employees, key=lambda x: x['salary'])['salary']
    return linear_search(employees, 'salary', highest_salary), binary_search(employees_by_salary, 'salary', highest_salary)

def search_lowest_salary():
    lowest_salary = min(employees, key=lambda x: x['salary'])['salary']
    return linear_search(employees, 'salary', lowest_salary), binary_search(employees_by_salary, 'salary', lowest_salary)

def search_youngest_employee():
    youngest_age = min(employees, key=lambda x: x['age'])['age']
    return linear_search(employees, 'age', youngest_age), binary_search(employees_by_age, 'age', youngest_age)

def search_oldest_employee():
    oldest_age = max(employees, key=lambda x: x['age'])['age']
    return linear_search(employees, 'age', oldest_age), binary_search(employees_by_age, 'age', oldest_age)

# Flask Routes
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Search Comparison</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; padding: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            table, th, td { border: 1px solid black; }
            th, td { padding: 10px; text-align: left; }
            th { background-color: #f2f2f2; }
            h1 { color: #333; }
        </style>
    </head>
    <body>
        <h1>Employee Search Comparison</h1>
        <form action="/search" method="post">
            <label for="case">Select Search Case:</label>
            <select id="case" name="case" required>
                <option value="highest_salary">Designation with Highest Salary</option>
                <option value="lowest_salary">Name of Employee with Lowest Salary</option>
                <option value="youngest_employee">Mobile Number of Youngest Employee</option>
                <option value="oldest_employee">Salary of Oldest Employee</option>
            </select>
            <br><br>
            <button type="submit">Search and Compare</button>
        </form>
    </body>
    </html>
    ''')

@app.route('/search', methods=['POST'])
def search():
    case = request.form['case']

    if case == 'highest_salary':
        (result_linear, time_linear), (result_binary, time_binary) = search_highest_salary()
    elif case == 'lowest_salary':
        (result_linear, time_linear), (result_binary, time_binary) = search_lowest_salary()
    elif case == 'youngest_employee':
        (result_linear, time_linear), (result_binary, time_binary) = search_youngest_employee()
    elif case == 'oldest_employee':
        (result_linear, time_linear), (result_binary, time_binary) = search_oldest_employee()
    else:
        return "Invalid case selected."

    # Time Complexity Plot
    n_values = [i for i in range(100, 1001, 100)]
    times_linear = []
    times_binary = []

    for n in n_values:
        sub_list = employees[:n]
        key = 'salary'
        value = sub_list[-1][key]

        _, t_linear = linear_search(sub_list, key, value)
        _, t_binary = binary_search(sub_list, key, value)

        times_linear.append(t_linear)
        times_binary.append(t_binary)

    plt.figure(figsize=(10, 6))
    plt.plot(n_values, times_linear, marker='o', linestyle='-', color='blue', linewidth=2, markersize=8, label='Linear Search')
    plt.plot(n_values, times_binary, marker='o', linestyle='-', color='green', linewidth=2, markersize=8, label='Binary Search')
    plt.xlabel('Number of Elements (n)')
    plt.ylabel('Time Taken (seconds)')
    plt.title('Search Algorithms Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Render result and graph
    return render_template_string(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            table, th, td {{ border: 1px solid black; }}
            th, td {{ padding: 10px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            h1 {{ color: #333; }}
            img {{ width: 100%; max-width: 800px; }}
        </style>
    </head>
    <body>
        <h1>Employee Search Time Comparison</h1>
        <table>
            <tr>
                <th>Search Method</th>
                <th>Time Taken (seconds)</th>
                <th>Result</th>
            </tr>
            <tr>
                <td>Linear Search</td>
                <td>{time_linear:.6f}</td>
                <td>{result_linear}</td>
            </tr>
            <tr>
                <td>Binary Search</td>
                <td>{time_binary:.6f}</td>
                <td>{result_binary}</td>
            </tr>
        </table>
        <h2>Time Complexity Graph</h2>
        <img src="data:image/png;base64,{plot_url}" alt="Search Time Complexity Comparison">
        <br><br>
        <a href="/">Back to Home</a>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
