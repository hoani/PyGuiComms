# Attempts to convert a string into an integer or float
# Returns the string if it can't

def str2num(s):
    try:
        n = int(s)
        return n
    except ValueError:
        pass
    try:
        n = float(s)
        return n
    except ValueError:
        pass
    return s
