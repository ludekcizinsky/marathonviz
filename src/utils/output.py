"""
Credit goes to Jonas-Mika Senghaas for writing this utility code.
"""

from termcolor import colored
from timeit import default_timer as timer

def output(task):
  task = colored(task, "blue", attrs=["bold"])
  print(task + '\n')

def working_on(task, time=True):
  st = colored("Working:", "yellow", attrs=["bold", "blink"])
  task = colored(task, "white", attrs=[])
  print(st, task)
  if time:
    return timer()

def finished(task, time=None):
  st = colored("Finished:", "green", attrs=["bold"])
  task = colored(task, "white", attrs=[])
  if time:
    time = colored(f"({round(time, 2)}s)", "white", attrs=['dark'])
    print(st, task, time)
  else:
    print(st, task)
  print()

def error(task):
  st = colored("Error:", "grey", "on_red", attrs=[])
  task = colored(task, "white", attrs=[])
  print(st, task)

