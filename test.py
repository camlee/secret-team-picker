import sys
import time
import random

while True:
    time.sleep(random.random())
    print(".", end="")
    sys.stdout.flush()
