# REPRODUCE RESULTS THESIS BEST PERFORMING MODELS (PIPELINE MODELS)
from text2dm import text_classification
from text2dm import dependency_tag_extraction
from text2dm import logic_extraction


# TEXT CLASSIFICATION
results = text_classification.evaluate_text_classification('../data/problem specific datasets/1. text classification/testset_1.csv')
print('Evaluation report for pipeline BERT sequence classifiers')
print(results)
print()


# DEPENDENCY TAG EXTRACTION
# from explicit dependency sentences
results = dependency_tag_extraction.evaluate_dep_tag_extraction_from_dep('../data/problem specific datasets/2. dependency extraction/from dependency sentences/testset_2d_tags.csv')
print('Evaluation report for NERDA (bert-base-uncased) to extract dependency tags from dependency sentences')
print(results)
print()
# from conditional sentences
results = dependency_tag_extraction.evaluate_dep_tag_extraction_from_log('../data/problem specific datasets/2. dependency extraction/from conditional sentences/testset_2l_tags.csv')
print('Evaluation report for NERDA (bert-base-uncased) to extract dependency tags from conditional sentences')
print(results)
print()


# LOGIC TAG EXTRACTION
results = logic_extraction.evaluate_logic_tag_extraction('../data/problem specific datasets/3. logic extraction/testset_3_tags.csv')
print('Evaluation report for NERDA (bert-base-uncased including stop word removal) to extract logical structure tags')
print(results)
print()
