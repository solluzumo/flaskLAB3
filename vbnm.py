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
        resize_image(image_path,filename,image_changed_path)
        graname = filename.split('.')[0]+"_graph.png"
        plot_color_distribution(image_path,graname)
        return render_template("changed_image.html",filename = filename, graph_name = graname)
    else:
        return 'Недопустимый файл'

def upload():
    form = MyForm()
    if form.validate_on_submit():
        # Получаем загруженный файл из формы
        file = form.image.data

        # Получаем числовое значение из формы
        number = form.number.data

        # Проверяем, что файл существует и имеет разрешенное расширение
        if file and allowed_file(file.filename):
            # Сохраняем файл на сервере
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Выполняем необходимые операции с изображением
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            image_changed_path = "static/changed"
            # Обработка изображения
            resize_image(image_path, filename, image_changed_path)
            graname = filename.split('.')[0] + "_graph.png"
            plot_color_distribution(image_path, graname)
            return render_template("changed_image.html", filename=filename, graph_name=graname)
        else:
            return 'Недопустимый файл'