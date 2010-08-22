import datetime

def fuzzy_time_diff(begin, end=None):
    """
    Returns a humanized string representing time difference
    between now() and the input timestamp.
    
    The output rounds up to days, hours, minutes, or seconds.
    4 days 5 hours returns "4 days"
    0 days 4 hours 3 minutes returns "4 hours", etc...
    """
    if end is None:
        end = datetime.datetime.now()
    timeDiff = end - begin
    days = timeDiff.days
    hours = timeDiff.seconds/3600
    minutes = timeDiff.seconds%3600/60
    seconds = timeDiff.seconds%3600%60
    
    str = u''
    tStr = u''
    if days > 365:
        years = int(days / 365)
        if years == 1:
            str = str + u'over 1 year'
        else:
            str = str + u'over %s years' % years
        return str
    if days > 61:
        months = int(days / 30)
        assert(months > 1)
        str = str + u'%s months' % months
        return str
    elif days > 0:
        if days == 1:   tStr = u'day'
        else:           tStr = u'days'
        str = str + u'%s %s' %(days, tStr)
        return str
    elif hours > 0:
        if hours == 1:  tStr = u'hour'
        else:           tStr = u'hours'
        str = str + u'%s %s' %(hours, tStr)
        return str
    elif minutes > 0:
        if minutes == 1:tStr = u'minutes'
        else:           tStr = u'minutes'           
        str = str + u'%s %s' %(minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:tStr = u'second'
        else:           tStr = u'seconds'
        str = str + u'%s %s' %(seconds, tStr)
        return str
    else:
        return '0 seconds'

