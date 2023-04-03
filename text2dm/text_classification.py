import pandas as pd
from transformers import DistilBertTokenizerFast
import torch
import torch.nn.functional as F
import nltk
from sklearn.metrics import classification_report
import os
# to indo printing of warnings
import warnings
warnings.simplefilter(action='ignore', category= UserWarning)
warnings.simplefilter(action='ignore', category= FutureWarning)

nltk.download('punkt')

target_path_1 = os.path.join(os.path.dirname(__file__), 'pipeline_models/bert_classifier1.pt')
# loading models is possible with torch if models trained on torch 1.4.0 (compatibility with adapted-NERDA package)
classifier1 = torch.load(target_path_1)
classifier1.eval()

target_path_2 = os.path.join(os.path.dirname(__file__), 'pipeline_models/bert_classifier2.pt')
classifier2 = torch.load(target_path_2, map_location=torch.device('cpu'))
classifier2.eval()


# defining tokenizer
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')


# function to predict label (irrelevant, dependency, logic) for each sentence of text
# input: string (can be multiple sentences)
# output: dataframe (columns: sentence, prediction)
def extract_labels(text):

    #global df_results
    tokenizer_split_sentences = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer_split_sentences.tokenize(text)  # split text into list of sentences

    predictions = []
    length = len(sentences)

    for i in range(0, length):
        inputs = tokenizer(sentences[i], return_tensors="pt")
        outputs = classifier1(**inputs)

        loss = outputs.loss
        logits = outputs.logits
        output =F.softmax(torch.tensor(logits))

        output = output.tolist()
        output = output[0]
        max_value = max(output)
        max_index = output.index(max_value)
        predictions.append(max_index)

    predictions = ["irrelevant" if i == 0 else "relevant" for i in predictions]

    for i in range(0, length):
        if predictions[i] == "relevant":
            inputs = tokenizer(sentences[i], return_tensors="pt")
            outputs = classifier2(**inputs)

            logits = outputs.logits
            output =F.softmax(torch.tensor(logits))

            output = output.tolist()
            output = output[0]
            max_value = max(output)
            max_index = output.index(max_value)

            predictions[i] = "dependency" if max_index == 0 else "logic"

    df_results = pd.DataFrame({'sentence':sentences, 'prediction': predictions})
    return df_results


# function to remove rows with prediction irrelevant
# input: dataframe (columns: sentence, prediction)
# output: dataframe (columns: sentence, prediction)
def remove_irrelevant_sentences(df):
    df_relevant = df[df.prediction != 'irrelevant']
    return df_relevant


# function to evaluate classifier 1: relevant vs irrelevant
# input: csv file (columns: sentence, labels), see testset1.csv
# output: classification report, dataframe with mistakes
def evaluate_classifier1(csv_file):
    test_data = pd.read_csv(csv_file)
    list_pred = []
    total_rows = len(test_data)

    for i in range(0, total_rows):
        inputs = tokenizer(test_data.loc[i, 'sentence'], return_tensors="pt")
        outputs = classifier1(**inputs)

        logits = outputs.logits
        output = F.softmax(torch.tensor(logits))

        output = output.tolist()
        output = output[0]
        max_value = max(output)
        max_index = output.index(max_value)
        list_pred.append(max_index)

    testdfy = test_data['label'].replace({'None': 'None', 'Dependency': 'Relevant', 'Logic': 'Relevant'}) # labels: irrelevant 0, relevant 1
    list_testlabels = testdfy.values.tolist()
    list_pred = ['None' if value == 0 else 'Relevant' for value in list_pred]

    # getting classification report
    report = classification_report(list_testlabels, list_pred)

    return report, list_pred


# function to evaluate classifier 2: logic vs dependency
# input: csv file (columns: sentence, labels), see testset1.csv
# output: classification report, dataframe with mistakes
def evaluate_classifier2(csv_file):
    test_data = pd.read_csv(csv_file)

    test_data = test_data[test_data.label != 'None']
    list_pred = []
    total_rows2 = len(test_data)
    test_sentences = test_data['sentence'].values

    for i in range(0, total_rows2):
        inputs = tokenizer(test_sentences[i], return_tensors="pt")
        outputs = classifier2(**inputs)

        logits = outputs.logits
        output = F.softmax(torch.tensor(logits))

        output = output.tolist()
        output = output[0]
        max_value = max(output)
        max_index = output.index(max_value)
        list_pred.append(max_index)

    list_testlabels = test_data['label'].values.tolist()
    list_pred = ['Dependency' if value == 0 else 'Logic' for value in list_pred]

    # getting classification report
    report = classification_report(list_testlabels, list_pred)

    return report


# function to evaluate text classification (pipeline of classifiers)
# input: csv file (columns: sentence, label), see testset1.csv to reproduce results paper
# output: classification report, dataframe with mistakes
def evaluate_text_classification(csv_file):
    test_data = pd.read_csv(csv_file)
    test_data_sentence = test_data['sentence'].values
    test_data_label = test_data['label'].values

    a, list_pred_classifier1 = evaluate_classifier1(csv_file)
    test_label_done = []
    test_pred_done = []
    test_sentence_class2 = []
    test_label_class2 = []

    for i in range(0, len(list_pred_classifier1)):
        if list_pred_classifier1[i] == 'None':
            test_label_done.append(test_data_label[i])
            test_pred_done.append("None")

        if list_pred_classifier1[i] == "Relevant":
            test_sentence_class2.append(test_data_sentence[i])
            test_label_class2.append(test_data_label[i])

    test_pred_class2 = []
    for i in range(0, len(test_sentence_class2)):
        inputs = tokenizer(test_sentence_class2[i], return_tensors="pt")
        outputs = classifier2(**inputs)

        logits = outputs.logits
        output = F.softmax(torch.tensor(logits))

        output = output.tolist()
        output = output[0]
        max_value = max(output)
        max_index = output.index(max_value)
        test_pred_class2.append(max_index)

    # 0 is "Dependency" and 1 is "Logic"
    test_pred_class2 = ["Dependency" if i == 0 else "Logic" for i in test_pred_class2]

    test_pipe_label = test_label_done + test_label_class2
    test_pipe_pred = test_pred_done + test_pred_class2

    report = classification_report(test_pipe_label, test_pipe_pred)

    return report
