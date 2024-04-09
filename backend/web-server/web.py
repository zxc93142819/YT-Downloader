from flask import Flask, render_template, request, Response, jsonify
import time
import sys 
import os  

#TODO Garbage collection (remove downloaded files)

current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(current_dir, '../api-server'))
 
 

app = Flask(__name__)


# 首頁
@app.route('/')
def index():
    return render_template('index.html')
 
 

if __name__ == '__main__':
    app.run(debug=True)  