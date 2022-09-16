def choose_stimulus(stimulus_type):
    if stimulus_type == "Latin":
        import string
        alphabet = list(string.ascii_uppercase)
        to_remove = "IQMERW"
        [alphabet.remove(elem) for elem in to_remove]
        stimulus = {"type": "text", "stimulus_list": alphabet}
    else:
        raise Exception("Unknown stimulus type")
    return stimulus["type"], stimulus["stimulus_list"]