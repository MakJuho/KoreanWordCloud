import os
from flask import Flask, render_template, request
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import scipy.misc

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
#from utils import label_map_util
#from utils import visualization_utils as vis_util
#from object_detection.utils import ops as utils_ops

def load_image_into_numpy_array(image):
  		(im_width, im_height) = image.size
  		return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

#def 종인,주호가 짤 함수

app=Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config["CACHE_TYPE"] = "null"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
	return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    file=request.files["file"]
    file.save('test/image1.jpg')

    image = Image.open('test/image1.jpg')
    image_np = load_image_into_numpy_array(image)

    scipy.misc.imsave(r'C:\Users\Hyejin Park\Desktop\오픈소스\static\outfile.jpg', image_np)

    return render_template("complete.html")

if __name__  ==  "__main__":
    app.run(debug=True)
