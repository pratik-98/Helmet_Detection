from flask import Flask, render_template, Response,  request, session, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename

from PIL import Image
import os
import sys
import cv2
from object_detection import *

__author__ = 'Pratik'
__source__ = ''

app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/Pratik Kailas Ghadge/OneDrive/Desktop/WEB DEV/OBJECT_DETECTION/static/uploads'
DETECTION_FOLDER = 'C:/Users/Pratik Kailas Ghadge/OneDrive/Desktop/WEB DEV/OBJECT_DETECTION/static/detections'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['DETECTION_FOLDER'] = DETECTION_FOLDER

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      # create a secure filename
      if f.filename=='':
        return " Oops!...you did not selecte a file. Please go back and uplaod!"
      else:
        filename = secure_filename(f.filename)
        print(filename)
        # save file to /static/uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(filepath)
        f.save(filepath)
        Predict(filepath, filename)
        
        return render_template("uploaded.html", display_detection = filename, fname = filename)      

if __name__ == '__main__':
   app.run()
