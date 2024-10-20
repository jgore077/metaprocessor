# a file used for housing all the mutation functions
import spacy
from spacy.cli import download
from VisualContextualClassifier import VisualContextualClassifier

def splitMetaData(metadata):
    # Downloads spacy model if not already downloaded
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading 'en_core_web_sm' model...")
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    for entry in metadata.values():
        if entry['description']:
            desc = nlp(entry['description'])
            temp_dict = {}
            for idx, sentence in enumerate(desc.sents):
                temp_dict[idx] = str(sentence)
            entry['sentences'] = temp_dict
        else:
            entry['sentences'] = None

def visualContextualBins(metadata):
    for entry in metadata.values():
        for idx, sentence in entry['sentences'].items():
            vis_con = VisualContextualClassifier.predict(sentence)
            abs(vis_con['visual'] - vis_con['contextual'])<.10