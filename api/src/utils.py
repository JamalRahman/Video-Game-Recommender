def search_list(term, target_list):
    return (term.lower() in target_list)

def get_superstrings(term, target_list):
    term = term.lower()
    superstrings = []
    for string in target_list:
        if string.lower().startswith(term):
            superstrings.append(string)
    return superstrings