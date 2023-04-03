# Text2DM pipeline
![Text2DM framework](https://i.imgur.com/xiCiWWt.png "Text2DM framework")

This directory includes all trained models and source code used for the Text2DM pipeline. The proposed framework transforms a chunk of text into a DRD graph, along with a simplicifation of a decision table in the form of a `.csv` file. The DRD graph can also be converted into an XML format, for other usage purposes. Moreover, a user interface is created to experiment with the framework in an interactive manner. The NLP pipeline consists of 6 sequential steps:

1. Coreference resolution
2. Text classification
3. Dependency extraction (tag extraction, special cases handling, drd construction)
5. Logic extraction

## How to run code
### Packages

All packages need to be installed in a conda environment in ==python 3.7==. This can be done by running the following commands in the terminal of your working directory: 


```
 pip install spacy==2.10
 pip install neuralcoref 
 python -m spacy download en_core_web_sm 
 pip install adapted-nerda
 pip install graphviz
 pip install lxml
 
```

The graphviz package should also be installed on your system.

FOR MAC:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install graphviz

```

FOR WINDOWS: 

1. [Download Graphviz][Graphviz]
[Graphviz]: https://graphviz.org/download/#windows

2. Modify drd&#95;graph&#95;construction:

	Make the following code available, where 'D:/Program Files (x86)/Graphviz2.38/bin/' is replaced 	by the address of where your bin file is.
	
	```
	import os
	os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
	```
	
### Encountered problems for windows
If you get the error "No module named tools.nnwrap" when installing adapted-nerda:

First execute the following command, then repeat installation of adapted-nerda: 

```
conda install pytorch==1.4.0
```
If this does not work try: 

```
pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
```





## Functions in &#95;&#95;init&#95;&#95;

### Construct DRD tuples from text
`text2drd(text)`

This function invokes several functions from the other `.py` files included in the directory to output a set of concepts and drd tuples, given a textual input. A DRD tuple is of the format (D, I, R) where D is the set of decisions, I the set of input information items and R the set of requirements.

1) Coreference resolution

In the first step, a coreference resolution technique is applied to the textual input to resolve referring pronouns. We rely on the [NeuralCoref][coref] package, which is installed in `coreference_resolution.py`.

[coref]:https://github.com/huggingface/neuralcoref

2) Text classification

In the second step, all sentences of the textual input are classified into irrelevant, conditional and dependency sentences leveraging the trained `bert_classifier1.pt` and `bert_classifier2.pt` models stored in the folder *pipeline_models*. First, the irrelevant sentences are separated from the relevant sentences. Next, the relevant sentences are further labeled as dependency or conditional. This small pipeline of BERT classifiers is implemented in `text_classification.py`.

3) Dependency extraction

In this step, depencency concept tags (B-DER, B-BAS, ...) are extracted from the remaining types of sentences, that is dependency and conditional sentences, using the functions in `dependency_tag_extraction.py`. A model for each type of sentence can be found in the folder pipeline_models: `nerda_concept_from_dep.pt` and `nerda_concept_from_logic.pt`.


5) Special case handling

This is an important step to link nested dependencies within one sentence in a correct manner. As discussed in the thesis, we limit the the level of dependencies to 2 and handle this in a rule-based manner for four special cases: case1a, case1b, case2a, case2b. The code can be found in `special_cases.py`, but we refer to the thesis for futher explanation.


6) Extracting concepts and dependencies

In this step, an interaction with the user is made. First a set of concepts (B-DER, B-BAS, B-ACT) and dependencies is made using the extract_dependencies function from `drd_tuple_construction.py`. Then, the user is asked to change the text (e.g., resolve synonyms and complex referring pronouns) if the concepts are not 100% correct.

7) DRD tuple construction

If the text is correclt adjusted, in case needed, a drd tuple will be created using the construct_drd_tuple function in `drd_tuple_construction.py`.


### Get DRD graph
`get_drd_graph(text)`

This function creates a visual DRD graph our of DRD tuples. First, a set of concepts and dependencies is created using the previous `text2drd` function. Second, the DRD tuples are given back in the main function of `drd_graph_construction.py`.

### Get XML

`get_xml(text)`

This function creates an xml format of DRD tuples. First, a set of concepts and dependencies is created using the previous `text2drd` function. Second, the xml is obtained as a string and can be exported to a `.dmn` file as illustrated in the directory "text2dm in action".


### Get mutliple DRD tuples
`get_mulitple_drd_tuples(df_examples)`

This is a function to generate DRD tuples for multiple examples at once to facilitate manual evaluation of text2drd. The input should be a dataframe, where the text examples should be under the header "**test example**". Next, the DRD tuples are created for each test example and stored in a second column "**drd tuples**". Eventually, a dataframe with the test examples and their respective DRD tuples is given as output.

### Extract logic table
`extract_logic_table(text)`

This function extracts the logical structures from conditional sentences to create a more simpler version of a decision table, namely the clauses (condition, consequence, ...) are stored in diffrent columns of a dataframe.


1) Coreference resolution

Once again, the first step includes the coreference resolution technique of [NeuralCoref][coref], implemented in `coreference_resolution.py`.

2) Text classification

In the second step, all sentences of the textual input are classified into irrelevant, conditional and dependency sentences leveraging the trained `bert_classifier1.pt` and `bert_classifier2.pt` models stored in the folder *pipeline_models*. First, the irrelevant sentences are separated from the relevant sentences. Next, the relevant sentences are further labeled as dependency or conditional. This small pipeline of BERT classifiers is implemented in `text_classification.py`.

3) Logic extraction

In this final step, only the sentences that are predicted as logic are taken into account. Finally we extract the logical structures by levereaging the `nerda_logic_extraction.pt` model whish is implmented in `logic_extraction.py` and can be found in *pipeline_models*.





