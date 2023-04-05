from text2dm import dependency_tag_extraction
from text2dm import text_classification


# helper functions
def get_first_indices(sentence):
    # find the start index of the derived concepts, base concepts and action verbs
    start_indices = {"derived": [], "base": [], "action": []}
    for i, (token, tag) in enumerate(sentence):
        if "B-" in tag:
            if "DER" in tag:
                start_indices["derived"].append(i)  # add the start index
            elif "BAS" in tag:
                start_indices["base"].append(i)  # add the start index
            elif "ACT" in tag:
                start_indices["action"].append(i)  # add the start index
    return start_indices


def get_all_indices(sentence):
    # find all the indices of the derived concepts, base concepts and action verbs
    start_indices = get_first_indices(sentence)
    all_indices = {"derived": [], "base": [], "action": []}
    for type_, indices in start_indices.items():  # loop over the key-value pairs in the start_indices dictionary
        for start_index in indices:
            i = start_index + 1
            if i == len(sentence):
                continue
            index_list = [start_index]  # create a list of all the indices
            while "I-" in sentence[i][1]:
                index_list.append(i)
                i += 1
            all_indices[type_].append(index_list)
    return all_indices


def indices_between(first_index, second_index, indices):
    for i in indices:
        if first_index < i < second_index:
            return True
    return False


def case1a(sentence):
    sentence1, sentence2 = None, None

    # find the start index of the derived concepts, base concepts and action verbs
    start_indices = get_first_indices(sentence)
    # print(start_indices)

    # find all the indices of the derived concepts, base concepts and action verbs
    all_indices = get_all_indices(sentence)
    # print(all_indices)

    # check if DER-ACT-DER
    if len(start_indices["derived"]) >= 2:  # at least two derived concepts
        first_derived_index, second_derived_index = start_indices["derived"][:2]
        for action_index in start_indices["action"]:
            if first_derived_index < action_index < second_derived_index and not indices_between(first_derived_index,
                                                                                                 second_derived_index,
                                                                                                 start_indices["base"]):
                end_index = all_indices["derived"][0][-1]  # last index of the first derived concept
                sentence1 = sentence[:end_index + 1]
                sentence2 = sentence[first_derived_index:]

                # making a new predictino for sentence 2print(sentence2)
                sentence2_string = ''
                for token in sentence2:
                    sentence2_string = sentence2_string + (' ') + token[0]

                df_label = text_classification.extract_labels(sentence2_string)
                text, tags = dependency_tag_extraction.extract_concept_tags(df_label)

                sentence2 = [list(zip(sentence[0], sentence[1])) for sentence in zip(text, tags)]
                sentence2 = sentence2[0]

                # return sentence1, sentence2

    return sentence1, sentence2


def case1b(sentence):
    sentence1, sentence2 = None, None

    # find the start index of the derived concepts, base concepts and action verbs
    start_indices = get_first_indices(sentence)
    # print(start_indices)

    # find all the indices of the derived concepts, base concepts and action verbs
    all_indices = get_all_indices(sentence)
    # print(all_indices)

    # check if BAS-ACT-BAS
    if len(start_indices["base"]) >= 2:  # at least two derived concepts
        first_base_index, second_base_index = start_indices["base"][:2]
        for action_index in start_indices["action"]:
            if first_base_index < action_index < second_base_index and not indices_between(first_base_index,
                                                                                           second_base_index,
                                                                                           start_indices["derived"]):
                end_index = all_indices["base"][0][-1]  # last index of the first base concept
                sentence1 = sentence[:end_index + 1]
                sentence2 = sentence[first_base_index:]

                # making a new predictino for sentence 2print(sentence2)
                sentence2_string = ''
                for token in sentence2:
                    sentence2_string = sentence2_string + (' ') + token[0]

                df_label = text_classification.extract_labels(sentence2_string)
                text, tags = dependency_tag_extraction.extract_concept_tags(df_label)

                sentence2 = [list(zip(sentence[0], sentence[1])) for sentence in zip(text, tags)]
                sentence2 = sentence2[0]

        # return sentence1, sentence2

    return sentence1, sentence2


def case2a(sentence):
    sentence1, sentence2 = None, None

    # find the start index of the derived concepts, base concepts and action verbs
    start_indices = get_first_indices(sentence)
    # print(start_indices)

    # find all the indices of the derived concepts, base concepts and action verbs
    all_indices = get_all_indices(sentence)
    # print(all_indices)

    # check if DER-BAS-DER-BAS
    if len(start_indices["derived"]) >= 2 and len(
            start_indices["base"]) >= 2:  # at least two derived concepts and two base concepts
        first_derived_index, second_derived_index = start_indices["derived"][:2]
        first_base_index, second_base_index = start_indices["base"][:2]
        if first_derived_index < first_base_index < second_derived_index < second_base_index:
            end_index1 = all_indices["base"][0][-1]  # final index of the first base concept
            sentence1 = sentence[:end_index1 + 1]
            sentence2 = sentence[second_derived_index:]

    return sentence1, sentence2


def case2b(sentence):
    sentence1, sentence2 = None, None

    # find the start index of the derived concepts, base concepts and action verbs
    start_indices = get_first_indices(sentence)

    # find all the indices of the derived concepts, base concepts and action verbs
    all_indices = get_all_indices(sentence)

    # check if BAS-DER-BAS-DER
    if len(start_indices["derived"]) >= 2 and len(
            start_indices["base"]) >= 2:  # at least two derived concepts and two base concepts
        first_derived_index, second_derived_index = start_indices["derived"][:2]
        first_base_index, second_base_index = start_indices["base"][:2]
        if first_base_index < first_derived_index < second_base_index < second_derived_index:
            end_index1 = all_indices["derived"][0][-1]  # final index of the first derived concept
            sentence1 = sentence[:end_index1 + 1]
            sentence2 = sentence[second_base_index:]

    return sentence1, sentence2


# main function
# we limit ourselves to be able to handle 2 dependencies in one sentence not more
def resolve_2_dep(d_texts, d_tags):
    # from one list of text and one list of tags to one list of tuples (text, tag)
    pred = [list(zip(sentence[0], sentence[1])) for sentence in zip(d_texts, d_tags)]
    resolved_pred = []

    not_true = (None, None)
    for sentence in pred:
        if case1a(sentence) != not_true:
            print("case1a")
            sentence_1, sentence_2 = case1a(sentence)
            resolved_pred.append(sentence_1)
            resolved_pred.append(sentence_2)

        elif case1b(sentence) != not_true:
            print("case1b")
            sentence_1, sentence_2 = case1b(sentence)
            resolved_pred.append(sentence_1)
            resolved_pred.append(sentence_2)

        elif case2a(sentence) != not_true:
            print("case2a")
            sentence_1, sentence_2 = case2a(sentence)
            resolved_pred.append(sentence_1)
            resolved_pred.append(sentence_2)

        elif case2b(sentence) != not_true:
            print("case2b")
            sentence_1, sentence_2 = case2b(sentence)
            resolved_pred.append(sentence_1)
            resolved_pred.append(sentence_2)

        else:
            resolved_pred.append(sentence)

        i = + 1

    return resolved_pred
