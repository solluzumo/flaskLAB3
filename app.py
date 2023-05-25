from flask import Flask, render_template, request, redirect, url_for, abort
from PIL import Image
import os
from werkzeug.utils import secure_filename
import numpy as np
from forms import MyForm

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdugDwmAAAAADXAM0stMt2dfH0RfU7oF5RQH1Tk'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdugDwmAAAAAC2IMPVgMu-SwxU9uY_EtW-JNy5r'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

@app.route('/protected')
def protected():
    # Проверяем, решена ли reCAPTCHA
    if not request.args.get('captcha') == 'solved':
        return 'Вы не решили капчу :('  # Возвращает ошибку 403 (Forbidden), если капча не решена
    # Здесь можно разместить содержимое защищенной страницы
    return redirect(url_for('image', captcha='solved'))

@app.route('/', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if request.method == "POST":
        return redirect(url_for('protected', captcha='solved'))

    return render_template('index.html', form=form)

@app.route('/image', methods=['GET', 'POST'])
def image():

    return render_template('upload-image.html')

@app.route('/image/upload', methods=['GET','POST'])
def upload():
    # Получаем загруженный файл из формы
    file = request.files['image']

    # Проверяем, что файл существует и имеет разрешенное расширение
    if file and allowed_file(file.filename):
        # Сохраняем файл на сервере
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Выполняем необходимые операции с изображением
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        image_changed_path = "static/changed"

        # Обработка изображения
        swap_and_save(image_path,filename,image_changed_path)
        return render_template("changed_image.html",filename = filename)
    else:
        return 'Недопустимый файл'


def allowed_file(filename):
    # Проверяем разрешенные расширения файлов
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def swap_and_save(image_path, file_name,image_folder):
    # Открываем изображение с помощью Pillow
    image = Image.open(image_path)

    # Преобразуем изображение в массив NumPy
    img_array = np.array(image)

    # Меняем местами левую и правую части
    height, width, _ = img_array.shape
    split_point = width // 2
    left_part = img_array[:, :split_point, :]
    right_part = img_array[:, split_point:, :]

    swapped_array_lr = np.concatenate((right_part, left_part), axis=1)

    # Создаем изображение для поменянных левой и правой частей
    swapped_image_lr = Image.fromarray(swapped_array_lr)

    # Сохраняем поменянные левую и правую части изображения
    swapped_image_lr.save(f"{image_folder}/left_right_{file_name}")

    # Меняем местами верхнюю и нижнюю части
    split_point = height // 2
    top_part = img_array[:split_point, :, :]
    bottom_part = img_array[split_point:, :, :]

    swapped_array_tb = np.concatenate((bottom_part, top_part), axis=0)

    # Создаем изображение для поменянных верхней и нижней частей
    swapped_image_tb = Image.fromarray(swapped_array_tb)

    # Сохраняем поменянные верхнюю и нижнюю части изображения
    swapped_image_tb.save(f"{image_folder}/up_down_{file_name}")


if __name__ == '__main__':
    app.run()