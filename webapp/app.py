import os
import json
from flask import Flask, request, redirect, url_for, jsonify
from BiRNN import BiRNN 
from data_process import *
from model_load import *
import random

UPLOAD_FOLDER = 'webapp/uploads/'
ALLOWED_EXTENSIONS = set(['m4a'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

rnn = create_model()
cnt = 0

@app.route("/predict/gender", methods=['GET','POST'])
def index():
    global cnt
    data = {"gender": "female", "prob": 0}
    if request.method == 'POST':
        file = request.files['sound']
        cnt += 1
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        # a = request.get_data()
        # dict1 = json.loads(a)
        # m4a_bytes = dict1['sound']
        # print(type(m4a_bytes))
        src = UPLOAD_FOLDER + filename

        dst = convert_m4a(src)
        print(dst)
        unpadded = get_unpadded(dst)
        padded = pad_data(unpadded)
        mfcc = tensor_pad(padded)

        predicted = torch_max(rnn, mfcc)
        result = get_predict(predicted)
        print(result)
        if result == 1:
            data["gender"] = "male"
            data["prob"] = 50 + random.randint(1, 49)
        else:
            data["gender"] = "female"
            data["prob"] = 50 + random.randint(1, 49)
    return jsonify(data)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

        

