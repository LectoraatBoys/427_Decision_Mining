from lxml import etree
import xml.etree.ElementTree as ET
from xml.dom import minidom
from text2dm import drd_graph_construction


def generate_xml(drd_tuple):

    list_inputs = list(drd_tuple[0])
    list_decisions = list(drd_tuple[1])
    list_requirements = list(drd_tuple[2])

    # make an id from the final decision
    final_decision = " ".join(drd_graph_construction.final_dec(drd_tuple[1], drd_tuple[2]))  # final decision as string
    final_decision_id = final_decision.replace(" ", "_")

    # initialization (for Camunda implementation)
    header = """<?xml version="1.0" encoding="UTF-8"?>"""
    root = etree.Element('definitions')
    root.set("xmlns", "http://www.omg.org/spec/DMN/20151101/dmn.xsd")
    root.set("id", final_decision_id)
    root.set("name", final_decision)
    root.set("namespace", "http://camunda.org/schema/1.0/dmn")

    # input data
    i = 1
    for bc in list_inputs:
        inputdata = etree.Element('inputData')
        inputdata.set("id", "InputData" + str(i))
        inputdata.set("name", bc)
        root.append(inputdata)
        i = i + 1

    # for each decisions --> make decision component in xml
    i = 1
    for dec in list_decisions:
        decision = etree.Element('decision')
        decision.set("id", "Decision" + str(i))
        decision.set("name", dec)

        # informationRequirement (can be requiredDecision or requiredInput)
        for req in list_requirements:
            if req[2] == dec:

                if req[1] in list_inputs:
                    index = list_inputs.index(req[1]) + 1
                    informationRequirement = etree.Element('informationRequirement')
                    requiredInput = etree.Element('requiredInput')
                    requiredInput.set("href", '#InputData' + str(index))
                    informationRequirement.append(requiredInput)
                    decision.append(informationRequirement)

                if req[1] in list_decisions:
                    index = list_decisions.index(req[1]) + 1
                    informationRequirement = etree.Element('informationRequirement')
                    requiredDecision = etree.Element('requiredDecision')
                    requiredDecision.set('href', '#Decision' + str(index))
                    informationRequirement.append(requiredDecision)
                    decision.append(informationRequirement)

        root.append(decision)
        i = i + 1

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")

    return xmlstr