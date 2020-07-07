
class InputProcessorHelper:
    @staticmethod
    def remove_latin_space(text: str):
        return text.replace(u'\xa0', u' ')