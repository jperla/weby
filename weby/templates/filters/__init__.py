def truncate(s, amount, buffer=5):
    if len(s) < (amount - buffer):
        return s
    else:
        return '%s...' % s[:amount]

def truncate_words(s, amount, buffer=5):
    #TODO: jperla: same but split
    raise NotImplementedError
    
