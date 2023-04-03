from graphviz import Digraph

# FOR WINDOWS
#import os
#os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'

# internal function: get final decision to make graph_id
def final_dec(decisions, requirements):
    final_decision = decisions.copy()
    for i in decisions:
        for req in requirements:
            if req[1] == i:
                if i in final_decision:
                    final_decision.remove(i)
    return final_decision


# internal functions: creation of graphical objects
def initialise_graph(final_decision, final_decision_id):
    dot = Digraph(final_decision, comment=final_decision, filename='DRD_' + final_decision_id)
    return dot


def create_dec(dec, dot):
    dot.node(dec, shape='box')
    return dot


def create_input(input, dot):
    dot.node(input)
    return dot


def create_edge(d_concept, b_concept, dot):
    dot.edge(d_concept, b_concept, dir='back')
    return dot


def tuple2graph(drd_tuple):

    """
    function to generate a visualisation of a drd tuple
    :param drd_tuple: (D, I, R) with D a set of decision, I set of input information items, R set of requirements
    :return: Digraph object (dot) and string (final_decision_id), graph is exportable with dot.render()
    """
    final_decision = " ".join(final_dec(drd_tuple[1], drd_tuple[2]))  # final decision as string
    final_decision_id = final_decision.replace(" ", "_")
    dot = initialise_graph(final_decision, final_decision_id)

    for ip in drd_tuple[0]:
        dot = create_input(ip, dot)

    for i in drd_tuple[1]:
        dot = create_dec(i, dot)

    for ir in drd_tuple[2]:
        dot = create_edge(ir[2], ir[1], dot)
    return dot, final_decision_id



