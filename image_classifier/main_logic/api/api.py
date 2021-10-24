import datetime
import requests
import re
from image_classifier.main_logic.api.constants import API_KEY, API_SECRET, USAGE_URL, CATEGORIES_URL,\
     COLOR_URL, TAGS_URL


class API:
    def __init__(self, key=API_KEY, secret=API_SECRET,
                 ctg_url=CATEGORIES_URL, color_url=COLOR_URL, tags_url=TAGS_URL, usage_url=USAGE_URL):

        self.auth = (key, secret)
        self.ctg_url = ctg_url
        self.color_url = color_url
        self.tags_url = tags_url
        self.usage_url = usage_url

    def usage(self):
        try:
            response = requests.get(self.usage_url, auth=self.auth)
        except Exception as ex:
            return self._parse_ex(ex)
        info = response.json()
        if 'result' in info and info['status']['type'] == 'success':
            return 'Использовано запросов: %s из %s (конец расчетного периода: %s).' % \
                   (str(info['result']['monthly_processed']), str(info['result']['monthly_limit']),
                    datetime.datetime.strptime(info['result']['billing_period_end'],
                                               '%d of %b, %Y').strftime('%d.%m.%Y'))
        else:
            return 'Ошибка - %s.' % info

    def categorize_image(self, path, by_color=False):
        try:
            response = requests.post(self.color_url if by_color else self.ctg_url,
                                     auth=self.auth, files={'image': open(path, 'rb')})
            info = response.json()
        except Exception as ex:
            return self._parse_ex(ex)

        if by_color:
            if 'result' in info and info['status']['type'] == 'success':
                return info['result']['colors']['image_colors'][0]['closest_palette_color_parent']
        else:
            if 'result' in info and info['status']['type'] == 'success':
                if int(info['result']['categories'][0]['confidence']) > 50:
                    return info['result']['categories'][0]['name']['en']
                else:
                    return 'undefined'
            else:
                return 'Ошибка - %s.' % info

    def image_tags(self, path):
        try:
            response = requests.post(self.tags_url, auth=self.auth, files={'image': open(path, 'rb')})
            info = response.json()
        except Exception as ex:
            return self._parse_ex(ex)

        result = []
        if 'result' in info and info['status']['type'] == 'success':
            for tags in info['result']['tags']:
                if tags['confidence'] > 50:
                    result.append(tags['tag']['en'])
            if len(result) < 1:
                return 'undefined'
            return ", ".join(result)
        else:
            return 'Ошибка - %s.' % info

    def _parse_ex(self, message):
        pattern = r"\[.+?(?=')"
        result = re.findall(pattern, str(message))
        try:
            err = result[0]
        except IndexError:
            err = message
        return 'Ошибка - %s.' % err


