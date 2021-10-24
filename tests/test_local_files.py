import os
import shutil

from tests.constants import IN_DIR, OUT_DIR

from image_classifier.main_logic.local_files.local_files import LocalFiles


def test_constructor():
    try:
        LocalFiles("asdasd", "asd")
        assert False, "ValueError for incorrect paths must be raised"
    except ValueError:
        assert True


def test_make_out_dir():
    lf = LocalFiles(IN_DIR, OUT_DIR)
    lf._make_out_dir("test")
    assert os.path.isdir(os.path.join(OUT_DIR, "test")), "incorrect out dir creation"
    lf._make_out_dir("test")
    assert os.path.isdir(os.path.join(OUT_DIR, "test")), "incorrect out dir creation"


def test_move_files():
    lf = LocalFiles(IN_DIR, OUT_DIR)
    lf.move_files()
    assert len(os.listdir(OUT_DIR)) > 0, "no directories created"
    for directory in os.listdir(OUT_DIR):
        assert os.path.isdir(os.path.join(OUT_DIR, directory)), "not a directory"
    for directory in os.listdir(OUT_DIR):
        for file in os.listdir(os.path.join(OUT_DIR, directory)):
            assert os.path.isfile(os.path.join(OUT_DIR, directory, file)), "not a file"
    shutil.rmtree(OUT_DIR)
