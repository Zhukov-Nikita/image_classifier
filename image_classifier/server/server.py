import os
from flask import Flask, flash, request, redirect, url_for, render_template
from time import sleep
from image_classifier.main_logic.api.api import API
from image_classifier.main_logic.api.constants import FILE_TYPES


UPLOAD_FOLDER = r'image_classifier\server\static\uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"
global path


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in FILE_TYPES


@app.route('/')
def upload_form():
    return render_template('page.html')


# загрузка файла на сервер для работы с api
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('Изображение не выбрано.')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('Изображение не выбрано.')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global path
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return render_template('page.html', filename=filename)
    else:
        flash('Допустимые типы файлов - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/category')
def category():
    global path
    api = API()
    data = api.categorize_image(path)
    print("Категория - " + data)
    return "Категория - " + data


@app.route('/color')
def color():
    global path
    api = API()
    sleep(3)
    # imagga не разрешает делать несколько запросов одновременно с бесплатной учетной записью
    data = api.categorize_image(path, True)
    print("Цвет - " + data)
    return "Цвет - " + data


@app.route('/tags')
def tags():
    global path
    api = API()
    sleep(5)
    data = api.image_tags(path)
    print("Теги - " + data)
    return "Теги - " + data


@app.route('/usage')
def usage():
    api = API()
    sleep(6)
    return api.usage()


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
