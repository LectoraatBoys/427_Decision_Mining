# import library
from text2dm import coreference_resolution
from text2dm import text_classification
from text2dm import dependency_tag_extraction
from text2dm import special_cases
from text2dm import drd_tuple_construction
from text2dm import drd_graph_construction
from text2dm import logic_extraction
from text2dm import xml_extraction
from googletrans import Translator
import pandas as pd
import warnings
import os
import time


# settings
pd.options.display.max_columns = 5
os.environ["TOKENIZERS_PARALLELISM"] = "false"
# undo printing of warnings
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

def classification(text):
    start = int(round(time.time() * 1000))
    print("Time for classification resolution in ms:")
    # step 1: coreference resolution
    coref_resolved = coreference_resolution.resolve_coref(text)
    print('STEP 1/6 DONE: coreference resolution')
    print()
    # step 2: text classification
    df_classified = text_classification.extract_labels(coref_resolved)
    end = int(round(time.time() * 1000))
    print(end - start)
    return df_classified


def text2drd(text):
    start = int(round(time.time() * 1000))
    print("Time for DRD tuple construction in ms:")
    """
    function to extract drd tuple from a textual description
    :param text: string
    :return: drd_tuple: (D, I, R) with D set of decision, I set of input information items and R set of requirements
    """

    translator = Translator()
    translation = translator.translate(text, src='nl', dest='en')
    print(f"translation: {translation}")
    text = translation.text

    # step 1: coreference resolution
    coref_resolved = coreference_resolution.resolve_coref(text)
    print('STEP 1/6 DONE: coreference resolution')
    print()
    # step 2: text classification
    df_classified = text_classification.extract_labels(coref_resolved)
    df_relevant = text_classification.remove_irrelevant_sentences(df_classified)
    print('STEP 2/6 DONE: text classification')
    print(df_relevant)
    print()
    # step 3: dependency tag extraction
    text, tags = dependency_tag_extraction.extract_concept_tags(df_relevant)
    print('STEP 3/6 DONE: dependency tag extraction')
    print()
    # step 4: resolving special cases
    output = special_cases.resolve_2_dep(text, tags)
    print('STEP 4/6 is DONE: resolving special cases')
    print()
    # step 5: extracting concepts and dependencies
    set_concepts, dependencies = drd_tuple_construction.extract_dependencies(output)
    print('INTERVENTION USER: adjust input text and iterate if list of concepts and dependencies not correct')
    print('Set of concepts = ', set_concepts)
    print('Set of dependencies = ', dependencies)
    print('STEP 5/6 is DONE: extracting concepts and dependencies')
    print()
    # step 6: drd tuple construction
    drd_tuple = drd_tuple_construction.construct_drd_tuple(dependencies)
    print('STEP 6/6 is DONE: construction of drd tuple')
    print(drd_tuple)
    print()
    end = int(round(time.time() * 1000))
    print(end - start)
    return drd_tuple, set_concepts, dependencies


def get_drd_graph(text):
    start = int(round(time.time() * 1000))
    print("Time for DRD graph construction in ms:")
    # construct the drd tuple
    drd_tuple, set_concepts, dep = text2drd(text)
    # get graph
    dot = drd_graph_construction.tuple2graph(drd_tuple)
    end = int(round(time.time() * 1000))
    print(end - start)
    return dot


def get_xml(text):
    # construct the drd tuple
    drd_tuple, set_concepts, dep = text2drd(text)
    # get xml
    xml = xml_extraction.generate_xml(drd_tuple)

    return xml


def get_multiple_drd_tuples(df_examples):
    """ function to get drd_tuples of multiple examples at once to facilitate manual evaluation of text2drd
    :param df_examples: dataframe with column 'test example' and one test example per row
    :return: dataframe with 'columns sentence' and 'drd tuple' (can be exported to csv with pandas)
    """
    examples = df_examples['test example']
    drd_tuples = []
    for example in examples:
        drd_tuple, set_concept, dep = text2drd(example)
        drd_tuples.append(drd_tuple)

    df_examples['drd tuple'] = drd_tuples
    df_result = df_examples

    return df_result


def extract_logic_table(text):
    coref_resolved = coreference_resolution.resolve_coref(text)
    # step 1: coreference resolution
    print('STEP 1/3 DONE: coreference resolution')
    print()
    # step 2: text classification
    df_classified = text_classification.extract_labels(coref_resolved)
    df_relevant = text_classification.remove_irrelevant_sentences(df_classified)
    print('STEP 2/3 DONE: text classification')
    print()
    # step 3: logic table extraction
    df_logic = df_relevant[df_relevant['prediction'] == 'logic']
    result = logic_extraction.extract_logic(df_logic)
    print('STEP 3/3 DONE: logic table extraction')

    return result