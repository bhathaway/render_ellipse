from flask import render_template, request
from app import app

@app.route("/")
@app.route("/index")
def index():
    user = {'username': 'Bryce'}
    #return render_template('index.html', title="Front Page", user=user)
    return render_template('index.html', user=user)

@app.route("/test_process", methods=['GET', 'POST'])
def test_process():
    if request.method == 'POST':
        x = int(request.form["x"])
        y =  x * 2
        return str(y)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
