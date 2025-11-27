import shelve
with shelve.open("src/file") as d:
    d['tScore'] = [["TL", 30], ["TL", 20],  ["TL", 10], ["TL", 1], ["TL", 0]]
    d.close()