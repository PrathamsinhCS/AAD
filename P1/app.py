from flask import Flask,  render_template , request
 
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/myguod', methods=['POST'])
def home():
    c = [int(request.form.get(f'c{i}')) for i in range(3)]
    d = [int(request.form.get(f'd{i}')) for i in range(3)]
    
    count1 = sum(1 for i in range(3) if c[i] > d[i])
    count2 = sum(1 for i in range(3) if c[i] < d[i])
    
    e = [count1,count2]
    print(" BE LAND")
    
    return render_template('index.html' , result= e)

if __name__ == '__main__':
    app.run(debug=True)
    
