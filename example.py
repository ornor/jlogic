from jlogic.battleships import Battleships


bs = Battleships("""

  1133102414
3 ..x.....x.    --x----xx-
1 ..........    --x-------
1 ..........    --x-------
2 .......x..    ----x--x--
1 ..........    -------x--
2 ..........    -x-------x
2 ..........    -------x-x
3 x..x......    x--x-----x
3 ......x...    ---x--x--x
2 ..........    ---x--x---

""")

print()
print(bs.row_values)

