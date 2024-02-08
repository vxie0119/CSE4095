from distutils.log import debug
from fileinput import filename
from flask import *
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
    for filename in os.listdir('.'):
        if os.path.isfile(filename):
            file_stat = os.stat(filename)
            info = {
                'filename': filename,
                'size': file_stat.st_size,
                'modified_date': file_stat.st_mtime
            }
            files.append(info)
    return render_template("file_list.html", files=files)



if __name__ == '__main__':
    app.run(debug = True)