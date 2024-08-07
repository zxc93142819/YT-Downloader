from flask import Flask, render_template, request, Response, jsonify
import time
import sys 
import os
from progress import run_socket_server

#TODO Garbage collection (remove downloaded files)

current_dir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.append(os.path.join(current_dir, '../api-server'))
 


app = Flask(__name__, template_folder='../../frontend/', static_folder='../../frontend/static/')
env_port = os.getenv("PORT", 5000)

# 首頁
@app.route('/')
def index():
    return render_template('index.html')
 
 

if __name__ == '__main__':
    # run_socket_server()
    app.run(debug=True, host='https://youtubedownload-8c304a4e20ec.herokuapp.com', port=env_port)
