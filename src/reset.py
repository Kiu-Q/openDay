import shelve
with shelve.open("src/file")  as d:
    d['tScore'] = [["TL", 5], ["TL Too", 4], ["TL also", 3], ["TL Junior", 2], ["TL Junior 2", 1]]
    d.close()