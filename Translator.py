from googletrans import Translator

class Vertaler:
    def __init__(self):
        dutch = ""
        english = ""

    @staticmethod
    def translate_text_file(input_file, output_file):
        vertaler = Translator()
        with open(input_file, 'r') as input_file:
            rows = input_file.readlines()
            translated_rows = []
            for row in rows:
                translation = vertaler.translate(row.strip(), src='nl', dest='en')
                translated_rows.append(translation.text + '\n')
        with open(output_file, 'w') as output_file:
            output_file.writelines(translated_rows)

    @staticmethod
    def read_translated_file(output_file):
        with open(output_file, 'r') as file:
            data = file.read().replace('\n', ' ')
        return data

# TEST functionality
# translator = Vertaler()
# dutch = 'input_folder/testcases Dutch.txt'
# english = 'input_folder/testcases English.txt'
# translate_text_file(dutch, english)
# english = read_translated_file(english)
# print(english)
