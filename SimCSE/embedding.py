from simcse import SimCSE
def embed_text_SimSCE(contents):
    vector_list = []
    model = SimCSE("princeton-nlp/sup-simcse-bert-base-uncased")
    for content in contents:
        text = content
        vector_list.append(model.encode(text))
    return vector_list