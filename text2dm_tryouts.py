# TRYOUTS of text2dm python package
# other option use the graphical user interface in user_interface.py (works for single test examples)
import text2dm
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


desired_width = 100
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 5)


# DRD TUPLE EXTRACTION FROM SINGLE EXAMPLE
def tuple_single_example():
#     input = """Health evaluation criteria consider both physical health score and mental health score of a patient. The physical health score
# is determined from the physical fitness score, BMI based health risk level and
# healthiness of senses. Physical fitness score is calculated from the sex of a patient and results of various tests such as strength test, coordination test, agility
# test, stamina test and speed test. The patient’s risk level should be assessed by
# determining the level of obesity based on BMI value, also on the waist circumference. The obesity level or degree of overweight should be assessed by determining
# the BMI value. If the weight of the patient given in kgs and length of patient
# given in meters, then the BMI value is weight/(length*length). The healthiness
# of the senses is calculated from the results of eye and hearing tests. Health evaluation also depends on the score of Mental health, which is determined from the
# EQ test result and the IQ test score. An IQ of a patient is assessed from testing
# his verbal, math and abstract levels."""
    input = "Of er tennis wordt gespeeld ligt aan het weer, het weer wordt beinvloed door het seizoen, het seizoen wordt bepaald door de datum"
        
    result_tuple = text2dm.text2drd(input)
    print('DRD TUPLE EXTRACTION FROM SINGLE EXAMPLE')
    print(result_tuple)
    print()


# DRD GRAPH EXTRACTION FROM SINGLE EXAMPLE
def drd_graph():
    input = """Health evaluation criteria consider both physical health score and mental health score of a patient. The physical health score
is determined from the physical fitness score, BMI based health risk level and
healthiness of senses. Physical fitness score is calculated from the sex of a patient and results of various tests such as strength test, coordination test, agility
test, stamina test and speed test. The patient’s risk level should be assessed by
determining the level of obesity based on BMI value, also on the waist circumference. The obesity level or degree of overweight should be assessed by determining
the BMI value. If the weight of the patient given in kgs and length of patient
given in meters, then the BMI value is weight/(length*length). The healthiness
of the senses is calculated from the results of eye and hearing tests. Health evaluation also depends on the score of Mental health, which is determined from the
EQ test result and the IQ test score. An IQ of a patient is assessed from testing
his verbal, math and abstract levels."""
    result_graph, final_decision_id = text2dm.get_drd_graph(input)
    result_graph.format = 'pdf'   # png also possible
    # save to pdf in text2dm in action
    result_graph.render("results tryouts/DRD_" + final_decision_id)  # view=True if you want the visualization to pop up


# XML EXTRACTION
def xml():
    input = """1 The competent authority of an institution shall be obliged to provide students of higher education who are enrolled in a study programme for the teaching profession covered by the Higher Education and Scientific Research Act, or who are otherwise studying for a certificate of sufficient pedagogical competence, and who are training for a position in education, with the opportunity to obtain the experience required as part of their study programme at the institution.

    2 The obligation referred to in the first paragraph comprises 5% of the total vocational education and training to be provided by the institution in the relevant academic year. The competent authority may set a higher percentage provided this is in accordance with the proper course of action within the institution.

    3 The competent authority may deny a ho-student further access to the institution if the student acts contrary to the foundation and objectives of the institution. A decision to deny access to the institution will be communicated by sending or issuing a copy to the competent authority of the educational institution concerned or to the relevant state examination board, and to the inspectorate. If the governing body of a special school refuses to admit a higher education student, it will announce this decision, in writing and with reasons, by sending or issuing a copy to the higher education student, without prejudice to the provisions in the previous sentence.

    4 The competent authority of the institution shall arrange the activities related to supervision by the teachers of the higher education students in the institution in agreement with the teachers, as well as in agreement with the educational institutions involved, or, if it concerns higher education students who are preparing to take a state examination in order to obtain a certificate of competence or a certificate of adequate pedagogical and didactic preparation, in agreement with the state examination committee involved.

    5 Our Minister may grant the competent authority full or partial exemption from the obligation referred to in the first paragraph based on special circumstances. The exemption applies for one academic year.

    6 The institutions to which higher professional education students as referred to in the first paragraph are admitted, shall be accessible to the inspectorate charged with the supervision of the educational institutions, to the members of the management and the teachers of these educational institutions to be appointed by them, as well as to the members of the State Examination Boards involved, insofar as this is necessary for the exercise of supervision of the practical training or supervision of the practical training of the higher professional education students present at the institution.
    """
    xmlstr = text2dm.get_xml(input)
    #print(xmlstr)
    with open("results tryouts/xml_DRD.dmn", "w") as f:
        # write xml to dmn file
        f.write(xmlstr)
    return xmlstr


# DRD EXTRACTION FROM MULTIPLE EXAMPLES
# input: dataframe with column 'test example'
# output: dataframe with column 'test example' and 'drd tuple'
def drd_multiple():
    df_test = pd.read_csv('results tryouts/test_examples.csv')
    df_result = text2dm.get_multiple_drd_tuples(df_test)
    print('DRD TUPLE EXTRACTION FROM MULTIPLE EXAMPLES')
    print(df_result)
    print()
    # optional write to csv (see results tryouts)
    df_result.to_csv('results tryouts/test_results_drd.csv')


# LOGIC TABLE EXTRACTION
def logic_table():
    input_logic = """1 The competent authority of an institution shall be obliged to provide students of higher education who are enrolled in a study programme for the teaching profession covered by the Higher Education and Scientific Research Act, or who are otherwise studying for a certificate of sufficient pedagogical competence, and who are training for a position in education, with the opportunity to obtain the experience required as part of their study programme at the institution.

    2 The obligation referred to in the first paragraph comprises 5% of the total vocational education and training to be provided by the institution in the relevant academic year. The competent authority may set a higher percentage provided this is in accordance with the proper course of action within the institution.

    3 The competent authority may deny a ho-student further access to the institution if the student acts contrary to the foundation and objectives of the institution. A decision to deny access to the institution will be communicated by sending or issuing a copy to the competent authority of the educational institution concerned or to the relevant state examination board, and to the inspectorate. If the governing body of a special school refuses to admit a higher education student, it will announce this decision, in writing and with reasons, by sending or issuing a copy to the higher education student, without prejudice to the provisions in the previous sentence.

    4 The competent authority of the institution shall arrange the activities related to supervision by the teachers of the higher education students in the institution in agreement with the teachers, as well as in agreement with the educational institutions involved, or, if it concerns higher education students who are preparing to take a state examination in order to obtain a certificate of competence or a certificate of adequate pedagogical and didactic preparation, in agreement with the state examination committee involved.

    5 Our Minister may grant the competent authority full or partial exemption from the obligation referred to in the first paragraph based on special circumstances. The exemption applies for one academic year.

    6 The institutions to which higher professional education students as referred to in the first paragraph are admitted, shall be accessible to the inspectorate charged with the supervision of the educational institutions, to the members of the management and the teachers of these educational institutions to be appointed by them, as well as to the members of the State Examination Boards involved, insofar as this is necessary for the exercise of supervision of the practical training or supervision of the practical training of the higher professional education students present at the institution.
    """
    df_result_logic = text2dm.extract_logic_table(input_logic)
    print('LOGIC TABLE EXTRACTION')
    print(df_result_logic)
    print()
    # optional write to csv (see results tryouts)
    df_result_logic.to_csv('results tryouts/test_result_logic.csv')


if __name__ == "__main__":
    # choose here what you want to test
    # drd_graph()
    logic_table()