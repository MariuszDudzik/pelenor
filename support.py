import re

class Validation(object):

    @staticmethod
    def validateText(text, max_length=15):
        text_without_special_chars = re.sub(r'[^a-zA-Z0-9]', '', text)
        return text_without_special_chars[:max_length]
    
class Wrap(object):
    
    @staticmethod
    def wrap_text(text, font, max_width):
        sections = text.split('\n')
        lines = []

        for section in sections:
            words = section.split(' ')
            current_line = ""

            for word in words:
                test_line = f"{current_line} {word}".strip()
                if font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

        return lines
    