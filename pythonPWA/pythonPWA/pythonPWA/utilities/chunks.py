def chunks(l, n):
    """
    Simple list splitting algorithm obtained from stackOverflow from:
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    """
    if n<1:
        n=1
    return [l[i:i+n] for i in range(0, len(l), n)]