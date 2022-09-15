def choose_stimulus(stimulus_type):
    if stimulus_type == "Latin":
        import string
        stimulus = {"type": "text", "stimulus_list": list(string.ascii_uppercase)}
    else:
        raise Exception("Unknown stimulus type")
    return stimulus["type"], stimulus["stimulus_list"]