# helper function to concatenate IOB-tags
def concatenate(concepts):
    concatenated_concepts = []

    for row in concepts:
        temp = []
        w = None
        for i in range(len(row)):
            word, tag = row[i]
            assert tag != "O"

            if "B-" in tag:
                if w is not None:  # no w to append for the first concept
                    temp.append(w)
                w = word
            elif "I-" in tag:
                w = str(w)
                w += " " + word
            else:
                print("error")

            if i == len(row) - 1:  # for the last concept we need to add w here (because there is no new B-)
                temp.append(w)
        concatenated_concepts.append(temp)
    return concatenated_concepts


def extract_dependencies(predictions):
    """
    function to extract set of concepts and set of dependencies
    :param predictions: list of sets (token, tag)
    :return: set of concepts and set of dependency tuples (action verb, base concept, derived concept)
    """
    derived_concepts = [[t for t in row if "DER" in t[1]] for row in predictions]
    base_concepts = [[t for t in row if "BAS" in t[1]] for row in predictions]
    action_verbs = [[t for t in row if "ACT" in t[1]] for row in predictions]

    # concatenate tokens to concept, action verb chunks
    conc_derived_concepts = concatenate(derived_concepts)
    conc_base_concepts = concatenate(base_concepts)
    conc_action_verbs = concatenate(action_verbs)

    # if no action verb put "None"
    conc_action_verbs = [["None"] if verb == [] else verb for verb in conc_action_verbs]

    # set of concepts: all base and derived concepts
    def extract_concept_set(conc_base_concepts, conc_derived_concepts):
        set_concepts = set()
        for sentence in conc_base_concepts:
            for concept in sentence:
                set_concepts.add(concept)

        for sentence in conc_derived_concepts:
            for concept in sentence:
                set_concepts.add(concept)
        return set_concepts

    # extract dependencies per sentence (one level dependencies can be extracted from a sentence)
    # special cases converted two level dependencies in two sentences, so that this can be captured here
    def concatenated_to_dependencies(d_concepts, b_concepts, a_verbs):
        result = set()
        # get all derived concepts, base concepts and action verbs in a sentence
        for i in range(len(d_concepts)):  # number of sentences
            derived = d_concepts[i]
            base = b_concepts[i]
            action = a_verbs[i]

            # for each derived concept construct a dependency
            for d in derived:
                for b in base:
                    for a in action:
                        result.add((a, b, d))
        return result

    def remove_duplicates(intermediate_result):
        end_result = set()
        for item in intermediate_result:
            boolean = False
            # check if the base and derived concept do not occur in another tuple, if not: add dependency
            # if end_result empty add item
            if len(end_result) == 0:
                end_result.add(item)

            else:
                for dep in end_result:
                    if item[1] == dep[1] and item[2] == dep[2]:
                        boolean = True
                        break

                if boolean:
                    continue

                else:
                    end_result.add(item)

        return end_result

    set_concepts = extract_concept_set(conc_base_concepts, conc_derived_concepts)
    intermediate_result = concatenated_to_dependencies(conc_derived_concepts, conc_base_concepts, conc_action_verbs)
    set_dependencies = remove_duplicates(intermediate_result)

    return set_concepts, set_dependencies


def construct_drd_tuple(dependency_set):
    """
    function to construct DRD tuple from dependency set
    :param dependency_set: set of dependency tuples
    :return: drd_tuple: (I, D, R)
    """
    decisions = set([])
    inputs = set([])

    # decision set equals all derived concepts
    for i in dependency_set:
        decisions.add(i[2])

    # inputs set equals all base concepts that do not occur as derived concept
    for i in dependency_set:
        count = 0
        for j in dependency_set:
            if i[1] == j[2]:
                count = +1

        if count == 0:
            inputs.add(i[1])

    # requirements set equals all dependencies (derived in extract_dependencies)
    requirements = dependency_set
    drd_tuple = (inputs, decisions, requirements)
    return drd_tuple
