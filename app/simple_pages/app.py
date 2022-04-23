from flask import Flask,render_template,request
import os

app = Flask(__name__)

@app.route('/', methods =['GET','POST'])
def index():
    if request.method='POST':
        file = request.files['csvfile']
        return file.filename
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)