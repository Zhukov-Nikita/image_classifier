import os
import shutil

from image_classifier.main_logic.api.api import API
from image_classifier.main_logic.api.constants import FILE_TYPES


class LocalFiles:
    def __init__(self, in_dir, out_dir='', color=False):
        if not os.path.isdir(in_dir):
            raise ValueError("Paths must be directories")
        self.in_dir = in_dir
        self.out_dir = in_dir if out_dir == '' else out_dir
        self.color = color
        self.api = API()

    def _make_out_dir(self, dir_name):
        if dir_name == '':
            raise ValueError("directory name must contain letters")
        full_path = os.path.join(self.out_dir, dir_name)
        if not os.path.isdir(full_path):
            os.makedirs(full_path)

    def move_files(self):
        if os.path.isdir(self.in_dir):
            images = [filename for filename in os.listdir(self.in_dir)
                      if os.path.isfile(os.path.join(self.in_dir, filename)) and
                      filename.split('.')[-1].lower() in FILE_TYPES]
            images_count = len(images)
            for iterator, file in enumerate(images):
                image_path = os.path.join(self.in_dir, file)
                dir_name = self.api.categorize_image(path=image_path, by_color=self.color)
                print('[%s / %s] %s - %s' % (iterator + 1, images_count, image_path, dir_name))
                if not dir_name.startswith('Ошибка'):
                    self._make_out_dir(dir_name)
                    shutil.copy(
                        os.path.join(self.in_dir, file),
                        os.path.join(self.out_dir, dir_name, file)
                    )


