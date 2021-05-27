#app.py
from flask import Flask, flash, request, redirect, request , render_template , url_for
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
from keras.models import load_model

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>welcome to Eye Droctor</title>
    <h1>Welcome to A.I eye Droctor<h1>
    <h3>Please upload a close up image of your eye</h3>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/predict', methods=['GET', 'POST'])
def uploaded_file():
    filename = request.args.get('filename')
    detect_model_path = './mtcnn_weights/'
    diagnosis_model_path = './models/accuracy-92size100x100_Threshold_0.56.h5'
    image =  cv2.imread('./upload/' + filename)
    model = load_model(diagnosis_model_path) # load disease detection model 
    image = cv2.resize(image,(100, 100))  
    image = image.reshape(1 ,100 , 100 , -1)
    diagnosis = model.predict(image)
    diagnosis = str(diagnosis)
    diagnosis = diagnosis[4:6]
    results = str(' the probability of Cataract is ') +str(diagnosis) + str('%')
    return str(results)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000,debug = True)


