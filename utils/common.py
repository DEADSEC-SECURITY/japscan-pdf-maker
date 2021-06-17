from time import sleep
import random

def random_sleep():
    value = random.randrange(0, 2)
    sleep(value)