from NERDA.models import NERDA
import pandas as pd
import nltk
import os

import warnings
warnings.simplefilter(action='ignore', category= UserWarning)
warnings.simplefilter(action='ignore', category= FutureWarning)

# LOAD IN BOTH MODELS DEPENDENCY EXTRACTION
tag_scheme = ['B-DER', 'I-DER', 'B-BAS', 'I-BAS', 'B-ACT']
transformer = 'bert-base-uncased'
# model for dependency tag extraction from  explicit dependency
target_path_1 = os.path.join(os.path.dirname(__file__), 'pipeline_models/nerda_concept_from_dep.pt')
model_concepts_dependency = NERDA(dataset_training=None, dataset_validation=None, tag_scheme=tag_scheme, tag_outside='O', transformer=transformer)
model_concepts_dependency.load_network_from_file(model_path=target_path_1)
# model for dependency tag extraction from conditional sentence
tag_scheme = ['B-DER', 'I-DER', 'B-BAS', 'I-BAS']
target_path_2 = os.path.join(os.path.dirname(__file__), 'pipeline_models/nerda_concept_from_log.pt')
model_concepts_logic = NERDA(dataset_training=None, dataset_validation=None, tag_scheme=tag_scheme, tag_outside='O', transformer=transformer)
model_concepts_logic.load_network_from_file(model_path=target_path_2)


def extract_concept_tags(df_relevant):

    """
    function to extract dependency IOB-tags from sentences
    :param df_relevant: dataframe with relevant sentences, columns 'sentence' and 'prediction' (logic or dependency)
    :return: list of sentences and list of corresponding tags
    """

    # lowercase of sentences
    lower_cased = df_relevant['sentence'].apply(str.lower)
    df_relevant = pd.concat([lower_cased, df_relevant['prediction']], axis=1)

    tags = []
    texts = []

    for index, row in df_relevant.iterrows():
        if row['prediction'] == 'dependency':
            prediction = model_concepts_dependency.predict_text(row['sentence'])

        if row['prediction'] == 'logic':
            prediction = model_concepts_logic.predict_text(row['sentence'])

        text, tag = prediction[0][0], prediction[1][0]
        tags.append(tag)
        texts.append(text)

    return texts, tags


def tokenized_list(dataframe):
    """
    helper function to tokenize sentences and sequences of tags
    :param dataframe: dataframe with columns 'sentence' and sequence of IOB-tags ('tags')
    :return: list of tokenized sentences and list of corresponding tokenized tags
    """
    sentences = dataframe['sentence'].tolist()
    tags = dataframe['tags'].tolist()

    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tokenized_tags = [nltk.word_tokenize(tag) for tag in tags]

    return tokenized_sentences, tokenized_tags


def errors_in_data(tokenized_sentences, tokenized_tags):
    """
    helper function: to identify errors in your data (length tags should be equal to length tokens)
    :param tokenized_sentences: list of tokens
    :param tokenized_tags: list of tokens
    :return: /
    """
    count = 0
    i = 0
    for sentence in tokenized_sentences:
        if len(sentence) != len(tokenized_tags[i]):
            print("Error occurred in data")
            print(str(i + 2) + ": " + str(sentence))
            print(tokenized_tags[i])
            count = count + 1
        i = i + 1


def evaluate_dep_tag_extraction_from_dep(testset_csv):
    """
    function to evaluate dependency IOB-tag extraction from dependency sentences
    to reproduce results thesis: use 'data/problem specific datasets/2. dependency extraction/from dependency sentences/testset_2d_tags.csv'
    :param testset_csv: csv file with columns 'sentence' and 'tags'
    :return: classification report (precision, recall and f1 score per tag + macro and micro average)
    """
    df_test = pd.read_csv(testset_csv)
    tokenized_sentences_test, tokenized_tags_test = tokenized_list(df_test)
    errors_in_data(tokenized_sentences_test, tokenized_tags_test)
    test = {'sentences': tokenized_sentences_test, 'tags': tokenized_tags_test}
    evaluation = model_concepts_dependency.evaluate_performance(test)

    return evaluation


def evaluate_dep_tag_extraction_from_log(testset_csv):
    """
    function to evaluate dependency IOB-tag extraction from logic sentences
    to reproduce results thesis: use 'data/problem specific datasets/2. dependency extraction/from conditional sentences/testset_2l_tags.csv'
    :param testset_csv: csv file with columns 'sentence' and 'tags'
    :return: classification report (precision recall and f1 score per tag + macro and micro average)
    """
    df_test = pd.read_csv(testset_csv)
    tokenized_sentences_test, tokenized_tags_test = tokenized_list(df_test)
    errors_in_data(tokenized_sentences_test, tokenized_tags_test)
    test = {'sentences': tokenized_sentences_test, 'tags': tokenized_tags_test}
    evaluation = model_concepts_logic.evaluate_performance(test)

    return evaluation

