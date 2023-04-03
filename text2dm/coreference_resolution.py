import spacy
import neuralcoref
nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)


def resolve_coref(text):
    
    """
    function to resolve coreferences of a textual description
    :param text: string
    :return: string
    """
    doc = nlp(text)
    resolved_text = text
    if doc._.has_coref:
        resolved_text = doc._.coref_resolved
        doc = nlp(resolved_text)

    if doc._.has_coref:  # double check
        resolved_text = doc._.coref_resolved
        doc = nlp(resolved_text)
    return resolved_text
