import uuid
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
FILE_PATH = os.getcwd() + '\\temp\\image'


@app.route('/upload', methods=['POST'])
def uploaded_file():
    try:
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        if not os.path.exists(FILE_PATH):
            os.makedirs(FILE_PATH, 0o555)
        file.save(os.path.join(FILE_PATH, uuid.uuid4().hex + '-' + filename))
    except IOError:
        return Result(code=500, message='io error', data=None).__dict__
    except BaseException:
        return Result(code=500, message='error', data=None).__dict__
    else:
        return Result(code=200, message='ok', data=None).__dict__


if __name__ == '__main__':
    app.run(debug=True)


class Result:
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data
