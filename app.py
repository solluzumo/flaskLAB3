from flask import Flask, render_template, request, redirect, url_for, g,abort
from PIL import Image
import os
from werkzeug.utils import secure_filename
import numpy as np
from forms import MyForm,ChoiceForm
import matplotlib.pyplot as plt
import tkinter as tk

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdugDwmAAAAADXAM0stMt2dfH0RfU7oF5RQH1Tk'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdugDwmAAAAAC2IMPVgMu-SwxU9uY_EtW-JNy5r'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

@app.before_request
def setup_tkinter():
    if not hasattr(g, 'tkinter_initialized'):
        root = tk.Tk()
        root.withdraw()
        root.quit()
        g.tkinter_initialized = True

@app.route('/protected')
def protected():
    # Проверяем, решена ли reCAPTCHA
    if request.args.get('captcha') == 'solved':
        return redirect(url_for('image', captcha='solved'))

    # Возвращает ошибку 403 (Forbidden), если капча не решена
    return "Captcha not succed"
@app.route('/', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect(url_for('protected', captcha='solved'))

    return render_template('index.html', form=form)

@app.route('/image', methods=['GET'])
def image():
    form = ChoiceForm()
    return render_template('upload-image.html',form=form)

@app.route('/image/upload', methods=['GET','POST'])
def upload():
    # Получаем загруженный файл из формы
    file = request.files['image']
    form = ChoiceForm()
    # Проверяем, что файл существует и имеет разрешенное расширение
    if file and allowed_file(file.filename):
        flip_direction = form.flip_direction.data
        # Сохраняем файл на сервере
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Выполняем необходимые операции с изображением
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #Получаем имя для графика и рисуем его
        graname = filename.split('.')[0] + "_graph.png"
        plot_color_distribution(image_path, graname)

        image_changed_path = "static/changed"
        # Обработка изображения
        if flip_direction == 'lr':
            # Меняем местами левую и правую часть изображения
            swap_left_and_save(image_path,filename,image_changed_path)
            filename = "left_right_" + filename

        elif flip_direction == 'ud':
            # Меняем местами верхнюю и нижнюю часть изображения
            swap_up_and_save(image_path,filename,image_changed_path)
            filename = "up_down_" + filename


        return render_template("changed_image.html",filename = filename, graph_name = graname)
    else:
        return 'Недопустимый файл'


def allowed_file(filename):
    # Проверяем разрешенные расширения файлов
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def swap_up_and_save(image_path, file_name,image_folder):
    # Открываем изображение с помощью Pillow
    image = Image.open(image_path)

    # Преобразуем изображение в массив NumPy
    img_array = np.array(image)

    # Меняем местами левую и правую части
    height, width, _ = img_array.shape

    # Меняем местами верхнюю и нижнюю части
    split_point = height // 2
    top_part = img_array[:split_point, :, :]
    bottom_part = img_array[split_point:, :, :]

    swapped_array_tb = np.concatenate((bottom_part, top_part), axis=0)

    # Создаем изображение для поменянных верхней и нижней частей
    swapped_image_tb = Image.fromarray(swapped_array_tb)

    # Сохраняем поменянные верхнюю и нижнюю части изображения
    swapped_image_tb.save(f"{image_folder}/up_down_{file_name}")
def swap_left_and_save(image_path, file_name,image_folder):
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
    swapped_image_lr.save(f"{image_folder}/left_right_{file_name}")
def plot_color_distribution(image_path,name):
    # Загрузка изображения с помощью Pillow
    image = Image.open(image_path)

    # Преобразование изображения в массив NumPy
    image_array = np.array(image)

    # Получение гистограммы распределения цветов по каналам
    red_hist = np.histogram(image_array[:, :, 0], bins=256, range=(0, 256))
    green_hist = np.histogram(image_array[:, :, 1], bins=256, range=(0, 256))
    blue_hist = np.histogram(image_array[:, :, 2], bins=256, range=(0, 256))

    # Рисование графика распределения цветов
    plt.figure(figsize=(10, 6))
    plt.title('Color Distribution')
    plt.xlabel('Color Intensity')
    plt.ylabel('Frequency')
    plt.xlim(0, 255)
    plt.plot(red_hist[1][:-1], red_hist[0], color='red', label='Red')
    plt.plot(green_hist[1][:-1], green_hist[0], color='green', label='Green')
    plt.plot(blue_hist[1][:-1], blue_hist[0], color='blue', label='Blue')
    plt.legend()

    plt.savefig(f"static/graph/{name}", dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    app.run()