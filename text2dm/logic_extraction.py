from NERDA.models import NERDA
import pandas as pd
import nltk
import os

import warnings
warnings.simplefilter(action='ignore', category= UserWarning)
warnings.simplefilter(action='ignore', category= FutureWarning)

# LOAD IN LOGIC EXTRACTION MODEL
tag_scheme = ['B-CONS', 'I-CONS', 'B-COND', 'I-COND', 'B-ELSE', 'I-ELSE', 'B-EXCE', 'I-EXCE']
transformer = 'bert-base-uncased'
target_path_1 = os.path.join(os.path.dirname(__file__), 'pipeline_models/nerda_logic_extraction.pt')
model_logic_extraction = NERDA(dataset_training=None, dataset_validation=None, tag_scheme=tag_scheme, tag_outside='O',
                               transformer=transformer)
model_logic_extraction.load_network_from_file(model_path=target_path_1)


def preprocess(dataframe):
    # lower case
    lower = dataframe['sentence'].apply(str.lower)

    # removing the words: "an", "a", "the"
    stopwords = ["the", "a", "an"]

    # Exclude stopwords with Python's list comprehension and pandas.DataFrame.apply.
    rem_stopwords = lower.apply(lambda x: ' '.join([word for word in x.split() if word not in (stopwords)]))

    result = pd.concat([rem_stopwords, dataframe['prediction']], axis=1)

    return result


def extract_logic(df_logic_sentences):
    l_tags = []
    l_texts = []

    df_logic_prep = preprocess(df_logic_sentences)

    # get IOB-tags
    for index, row in df_logic_prep.iterrows():
        prediction = model_logic_extraction.predict_text(row['sentence'])
        l_text, l_tag = prediction[0][0], prediction[1][0]
        l_tags.append(l_tag)
        l_texts.append(l_text)

    # from one list of text and one list of tags to one list of tuples (text, tag)
    l_pred = [list(zip(sentence[0], sentence[1])) for sentence in zip(l_texts, l_tags)]

    conditions = [[t for t in row if "COND" in t[1]] for row in l_pred]
    then_consequences = [[t for t in row if "CONS" in t[1]] for row in l_pred]
    else_consequences = [[t for t in row if "ELSE" in t[1]] for row in l_pred]
    exceptions = [[t for t in row if "EXCE" in t[1]] for row in l_pred]

    def concatenate_logic(logic_tags):
        concatenated_chunks = []
        # list of chunks per sentence
        for item in logic_tags:
            chunk = []
            w = None
            for i in range(len(item)):
                word, tag = item[i]
                assert tag != "O"

                if "B-" in tag:
                    if w is not None:  # no w to append for the first concept
                        chunk.append(w)
                    w = word
                elif "I-" in tag:
                    w = str(w) + " " + str(word)
                else:
                    print("error")

                if i == len(item) - 1:  # for the last concept we need to add w here (because there is no new B-)
                    chunk.append(w)
            concatenated_chunks.append(chunk)

        return concatenated_chunks

    conc_conditions = concatenate_logic(conditions)
    conc_consequences = concatenate_logic(then_consequences)
    conc_exceptions = concatenate_logic(exceptions)
    conc_else_consequences = concatenate_logic(else_consequences)

    final_conditions = []
    final_consequences = []
    final_exceptions = []
    final_else_consequences = []
    i = 0
    for condition in conc_conditions:

        if len(condition) == 2 and len(conc_consequences[i]) == 2:  # to handle if-then and if-then in one sentences
            final_conditions.append(condition[0])
            final_conditions.append(condition[1])

            final_consequences.append(conc_consequences[i][0])
            final_consequences.append(conc_consequences[i][1])

            final_exceptions.append(conc_exceptions[i])
            final_exceptions.append(conc_exceptions[i])  # assumption that this will be the same for both rules

            final_else_consequences.append([])  # assumption first if-then has no else
            final_else_consequences.append(conc_else_consequences[i])

        else:
            final_conditions.append(condition)
            final_consequences.append(conc_consequences[i])
            final_exceptions.append(conc_exceptions[i])
            final_else_consequences.append(conc_else_consequences[i])

        i += 1

        # to undo the lists in the dataframe

    def remove_lists_in_list(list):
        new_list = []
        for statement in list:
            string = ''
            for item in statement:
                string = string + item
            new_list.append(string)
        return new_list

    str_conditions = remove_lists_in_list(final_conditions)
    str_exceptions = remove_lists_in_list(final_exceptions)
    str_consequences = remove_lists_in_list(final_consequences)
    str_else_consequences = remove_lists_in_list(final_else_consequences)

    # replace empty values with /
    str_conditions = [word if word != '' else '/' for word in str_conditions]
    str_exceptions = [word if word != '' else '/' for word in str_exceptions]
    str_consequences = [word if word != '' else '/' for word in str_consequences]
    str_else_consequences = [word if word != '' else '/' for word in str_else_consequences]

    data = {'Condition': str_conditions, 'Exception': str_exceptions, 'Then-consequence': str_consequences,
            'Else-consequence': str_else_consequences}
    result = pd.DataFrame(data)
    return result


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


def remove_stopwords(tokenized_sentences, tokenized_tags):
    words = {"A", "a", "an", "An", "the", "The"}
    combined_sentences = [[(s, t) for s, t in zip(tokenized_sentence, tokenized_tag)] for tokenized_sentence, tokenized_tag in zip(tokenized_sentences, tokenized_tags)]
    filtered_combined_sentences = [list(filter(lambda t: t[0] not in words, combined_sentence)) for combined_sentence in combined_sentences]
    filtered_tokenized_sentences, filtered_tokenized_tags = [[t[0] for t in sentence] for sentence in filtered_combined_sentences], [[t[1] for t in sentence] for sentence in filtered_combined_sentences]

    return filtered_tokenized_sentences, filtered_tokenized_tags


def evaluate_logic_tag_extraction(testset_csv):
    """
    function to evaluate logic IOB-tag extraction
    (to reproduce results thesis use '../data/problem specific datasets/3. logic extraction/testset_3_tags.csv'
    :param testset_csv: csv file with columns 'sentence' and 'tags
    :return: classification report (precision recall and f1 score per tag)
    """
    df_test = pd.read_csv(testset_csv)
    tokenized_sentences_test, tokenized_tags_test = tokenized_list(df_test)
    errors_in_data(tokenized_sentences_test, tokenized_tags_test)
    tokenized_sentence_test_prep, tokenized_tags_test_prep = remove_stopwords(tokenized_sentences_test, tokenized_tags_test)
    test = {'sentences': tokenized_sentence_test_prep, 'tags': tokenized_tags_test_prep}
    evaluation = model_logic_extraction.evaluate_performance(test)

    return evaluation
