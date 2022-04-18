import os

from matplotlib import lines
from numbrix import main
import cProfile
import pstats

cProfile.run("main()", "output.dat")

with open("time.txt", "w") as f:
    p = pstats.Stats("output.dat", stream=f)
    p.sort_stats("time").print_stats()

os.remove("output.dat")