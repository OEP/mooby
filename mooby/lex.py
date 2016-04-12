import re

stop_rx = re.compile(r'([?.!]+) *')


def tokenize(blob):
    return blob.split()


def phrasify(blob):
    result = stop_rx.split(blob)
    out = []
    i = 0
    while i < len(result):
        piece = result[i:i+2]
        piece = ''.join(piece)
        if piece:
            out.append(piece)
        i += 2
    return out
