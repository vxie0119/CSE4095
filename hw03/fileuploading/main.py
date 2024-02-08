from distutils.log import debug
from fileinput import filename
from flask import *
from datetime import datetime
import os 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/fileuploading/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return render_template("Acknowledgement.html", name = f.filename)
'''
def upload_file():
    if 'file' not in request.files:
        return render_template('Acknowledgement.html', message='No file part')
    
    file = request.files['file']

    if file.name == '':
        return render_template("Acknowledgement.html", message="No selected file")
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("Acknowledgement.html", message="File uploaded successfully")
    else:
        return render_template("Acknowledgement.html", message="File upload failed")
'''
@app.route('/files', methods = ["GET"])
def get_files():
    file_info = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_info.append({
            'filename': filename,
            'size': os.path.getsize(file_path),
            'modified_date': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:$M:$S')
        })
    return render_template("file_list.html", files=file_info)

if __name__ == '__main__':
    app.run(debug = True)