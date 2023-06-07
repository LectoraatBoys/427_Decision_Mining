import pandas as pd
import argparse
import requests
import text2dm
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/endpoint', methods=['POST'])
@cross_origin()
def handle_post():
    """
    To access the /endpoint route and execute the handle_post function,
    you should send a POST request to http://127.0.0.1:5000/endpoint from the Java program.
    """
    # Retrieve the data from the POST request
    data = request.get_json()
    # Extract the necessary information from the data
    info = data['info']
    file_name = data['file_name']
    # Pass the information to the bar function
    # Perform any necessary operations or decisions based on the result

    full_DMN_extraction(info, filename=file_name)
    # hier vind de overgang naar Goossens plaats
    # Return a response
    response = {'message': 'Response from Python server'}
    return jsonify(response)

def full_DMN_extraction(text, filename):
    result_tuple, final_decision = text2dm.get_drd_graph(text)
    result_logic = text2dm.extract_logic_table(text)

    print(result_tuple)
    print(result_logic)

    result_tuple.format = 'png'
    result_tuple.render(f'output_folder/{filename}_result_tuple')
    result_logic.to_csv(f'output_folder/{filename}_test_result_logic.csv')

def parse_CMD_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input text to be processed")
    args = parser.parse_args()
    return args.input

def process_file(filename):
    # Your file processing logic goes here
    str_builder = []
    with open(filename, 'r') as file:
        # Process the file contents
        for line in file:
            str_builder.append(line)

    return "".join(str_builder)

def main():
    # dutch = 'input_folder/testcases Dutch.txt'
    # english = 'input_folder/testcases English.txt'
    # translator = Vertaler()
    # translator.translate_text_file(dutch, english)
    # english = translator.read_translated_file(english)*-+
    
    # print(english)
    # input_string = english


    # input_string = process_file(parse_CMD_arg())
    # input_name = "testcases_Dutch"
    # full_DMN_extraction(input_string,filename=input_name)
    pass

if __name__ == "__main__":
    print("START")
    # communicatie with Java
    # print(f"test print goossens {bar('foo')}")
    app.run()
    # main()
    print("EINDE")

