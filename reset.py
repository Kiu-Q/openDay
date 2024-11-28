import shelve
with shelve.open("src/file") as d:
    d['tScore1'] = [["TL", 5], ["TL Too", 10], ["TL also", 15], ["TL Junior", 20], ["TL Junior 2", 25]]
    d['tScore2'] = [["TL", 13], ["TL Too", 11],  ["TL also", 9], ["TL Junior", 2], ["TL Junior 4", 1]]
    d.close()