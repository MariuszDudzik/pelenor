import re

class Validation(object):

    @staticmethod
    def validateText(text, max_length=15):
        text_without_special_chars = re.sub(r'[^a-zA-Z0-9]', '', text)
        return text_without_special_chars[:max_length]
    
