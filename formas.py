
# python formas.py > formas.txt
# sort formas.txt > formas-sorted.txt
# uniq formas-sorted.txt > formas-uniq.txt

import subprocess

command = "tools/wordforms"
aff = "ia-ia.aff" 
dic = "ia-ia.dic"

f = open (dic)
xs = f.readlines ()
xs = [x.strip () for x in xs]
bases = [x.split ("/")[0] for x in xs]

for b0 in bases:
  b1 = b0.replace ("(","")
  b2 = b1.replace (")","")
  print (b2)
  result = subprocess.run (
    [command, aff, dic, b2], stdout=subprocess.PIPE)
  result = result.stdout.decode ('utf-8')
  for s in result.split ("\n"):
    x = s.strip ()
    if len (x) > 0:
      print (x)

