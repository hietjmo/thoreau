
import argparse
import re
from tabulate import tabulate

def read_args ():
  parser = argparse.ArgumentParser ()
  parser.add_argument ("-i", "--infile")
  parser.add_argument (
    "-v", "--vocabulario", default="interlingua-basic-2500.txt")
  args = parser.parse_args ()
  return (args)

def x_if (b):
  if b:
    return "X"
  else:
    return " "

args = read_args ()

f = open (args.vocabulario)
parolas = [p.strip ().lower () for p in f.readlines ()]
f.close ()

g = open (args.infile)
text = g.readlines ()
g.close ()


pars = [re.findall (r'\w+',t.lower ()) for t in text]
numbered = [[(p,i+1,j+1) for j,p in enumerate(ln)] for i,ln in enumerate (pars)]
t = numbered
flat_list = [item for sublist in t for item in sublist]
table = [(i,j,n,x_if (n in parolas)) for n,i,j in flat_list]
print (tabulate (table))

