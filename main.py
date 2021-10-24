from image_classifier.server.server import app
import os

# очистка папки загрузок при запуске flask
folder = r'image_classifier\server\static\uploads'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        os.remove(file_path)
        print(file_path + " - удалён")
    except Exception as e:
        print('Ошибка - %s_%s' % (file_path, e))

app.run('localhost', 50670)
