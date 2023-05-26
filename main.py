import pandas as pd
import argparse
import requests
import text2dm
from flask import Flask, request, jsonify
from Goossens import bar

app = Flask(__name__)

@app.route('/endpoint', methods=['POST'])
def handle_post():
    """
    To access the /endpoint route and execute the handle_post function,
    you should send a POST request to http://127.0.0.1:5000/endpoint from the Java program.
    """
    # Retrieve the data from the POST request
    data = request.get_json()
    # Extract the necessary information from the data
    info = data['info']
    # Pass the information to the bar function
    # Perform any necessary operations or decisions based on the result
    goossens = bar(info)
    # hier vind de overgang naar Goossens plaats
    main()
    # Return a response
    response = {'message': 'Response from Python server'}
    return jsonify(response)

def full_DMN_extraction(text):
    result_tuple = text2dm.text2drd(text)
    result_logic = text2dm.extract_logic_table(text)

    print(result_tuple)
    print(result_logic)



def send_post_message_to_localhost(DRD_path, logic_table_path):
    url = "http://localhost:5000/api/v1.0/"
    payload = {"path_to_DRD": DRD_path,
               "path_to_logic_table": logic_table_path}
    response = requests.post(url, json=payload, timeout=5)
    print(response.text)
    return response.text

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
    input_string = """
    1 Het bevoegd gezag van een instelling is verplicht, ho-studenten die zijn ingeschreven voor een opleiding voor het beroep van leraar waarop de Wet op het hoger onderwijs en wetenschappelijk onderzoek betrekking heeft, of die anderszins studeren voor een bewijs van voldoende pedagogische bekwaamheid, en die in opleiding zijn voor een functie in het onderwijs, gelegenheid te bieden de als onderdeel van hun opleiding vereiste ervaring in de instelling te verkrijgen.

    2 De in het eerste lid bedoelde verplichting omvat 5% van het in het desbetreffende studiejaar door de instelling in totaal te verzorgen beroepsonderwijs en educatie. Het bevoegd gezag kan een hoger percentage vaststellen mits dat in overeenstemming is met de goede gang van zaken binnen de instelling.

    3 Het bevoegd gezag kan een ho-student de verdere toegang tot de instelling ontzeggen, indien deze in de instelling in strijd handelt met de grondslag en doelstellingen van de instelling. Van een besluit tot ontzegging van de toegang tot de instelling wordt mededeling gedaan door toezending of uitreiking van een afschrift aan het bevoegd gezag van de betrokken opleidingsinstelling dan wel aan de betrokken staatsexamencommissie, en aan de inspectie. Indien het bevoegd gezag van een bijzondere school een ho-student de toegang weigert, maakt het dit besluit, schriftelijk en met redenen omkleed, bekend door toezending of uitreiking aan de ho-student, onverminderd het bepaalde in de vorige volzin.

    4 Het bevoegd gezag van de instelling regelt de werkzaamheden in verband met de begeleiding door de leraren van de ho-studenten in de instelling in overeenstemming met de leraren, alsmede in overeenstemming met de betrokken opleidingsinstellingen, dan wel, indien het betreft ho-studenten die zich voorbereiden op het afleggen van een staatsexamen ter verkrijging van een bewijs van bekwaamheid of een bewijs van voldoende pedagogische en didactische voorbereiding, in overeenstemming met de betrokken staatsexamencommissie.

    5 Onze Minister kan het bevoegd gezag op grond van bijzondere omstandigheden gehele of gedeeltelijke ontheffing van de in het eerste lid bedoelde verplichting verlenen. De ontheffing geldt voor een studiejaar.

    6 De instellingen waarbij ho-studenten als bedoeld in het eerste lid zijn toegelaten, zijn toegankelijk voor de inspectie, belast met het toezicht op de opleidingsinstellingen, voor de directieleden en de door deze aan te wijzen docenten van die opleidingsinstellingen, alsmede voor de leden van de betrokken staatsexamencommissies, een en ander voor zover dat voor de uitoefening van het toezicht op de praktische vorming onderscheidenlijk de begeleiding van de praktische vorming van de in de instelling aanwezige ho-studenten noodzakelijk is.
    """

    input_string = process_file(parse_CMD_arg())

    full_DMN_extraction(input_string)

if __name__ == "__main__":
    # communicatie with Java
    print(f"test print goossens {bar('foo')}")
    app.run()
    # main()

