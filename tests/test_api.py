from image_classifier.main_logic.api.api import API


def test_categorize_image():
    api = API()
    path = r'tests/resources/test.jpg'
    assert isinstance(api.categorize_image(path), str), "Should return 'nature landscape' value"
    api = API(ctg_url='sdfsdf')
    assert api.categorize_image(path).startswith('Ошибка - Invalid URL')


def test_color_image():
    api = API()
    path = r'tests/resources/test.jpg'
    assert isinstance(api.categorize_image(path, True), str), "Should return 'blue' value"
    api = API(color_url='sdfsdf')
    assert api.categorize_image(path, True).startswith('Ошибка - Invalid URL')
    

def test_usage():
    api = API()
    assert isinstance(api.usage(), str), "Should return 'request' value"
    api = API(usage_url='sdfsdf')
    assert api.usage().startswith('Ошибка - Invalid URL')
