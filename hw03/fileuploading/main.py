from distutils.log import debug
from fileinput import filename
from flask import Flask, request, render_template
from datetime import datetime
import os 

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template("Acknowledgement.html", name = f.filename)

@app.route('/file_list', methods = ["GET"])
def get_files():
    files = []
    non_image = False
    for filename in os.listdir('.'):
        if os.path.isfile(filename) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_stat = os.stat(filename)
            info = {
                'filename': filename,
                'size': round(file_stat.st_size / (1024 * 1024), 2),
                'modified_date': datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            }
            files.append(info)
        else: 
            non_image = True 
    return render_template("file_list.html", files=files)



if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')

