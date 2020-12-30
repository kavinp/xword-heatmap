# Helpers for Crossword Heatmap

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield [None] + lst[i:i + n]

def init_grid(lst, n):
    """Yields successive n-sized chunks from lst.
       Pads list with a row and col of None @ 0,
       so that the output grid is 1-indexed."""
    return [None] + list(chunks(lst, n))

def normalize_diff(d):
    if d > 5:
        return 5
    elif d < -5:
        return -5
    return d

def to_str_with_sign(num):
    """Convert integer to string with pos sign if positive."""
    if num >= 0:
        return '+' + str(num)
    return str(num)
