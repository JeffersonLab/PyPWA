def lowercase_dict(dictionary):
    return dict((key.lower().strip(" "), value) for key, value in zip(
                 dictionary.keys(), dictionary.values()))
