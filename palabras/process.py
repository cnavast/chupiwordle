# -*- coding: iso-8859-1 -*-

f = open("listado-general.txt", "r")
wu = open("list-unique-chars.txt", "w")
w = open("list.txt", "w")

replacements = (
    ("á", "a"),
    ("é", "e"),
    ("í", "i"),
    ("ó", "o"),
    ("ú", "u"),
    ("ñ", "$")
)

def normalize(s):
    s = s.lower()
    for a, b in replacements:
        s = s.replace(a, b)
    return s

for word in f:
    word = normalize(word)

    if len(word) != 6:
        continue

    # Filter out words that repeats characters
    if len(set(word)) != 6:
        w.write(word.replace("$", "ñ"))
    else:
        w.write(word.replace("$", "ñ"))
        wu.write(word.replace("$", "ñ"))


f.close()
w.close()
wu.close()
