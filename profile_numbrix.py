import os
import signal

from numbrix import main
import cProfile
import pstats

def handler(signum, frame):
    print ("Aborting ...")
    filter_output()
    exit()

def filter_output():
    with open("time.txt", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("time").print_stats()

    os.remove("output.dat")
 
 
signal.signal(signal.SIGINT, handler)


cProfile.run("main()", "output.dat")
filter_output()
