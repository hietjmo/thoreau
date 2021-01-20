
# python thoreau-scriptor.py -f arbores.txt thoreau-initio.txt

from collections import defaultdict
from tkinter.ttk import Progressbar
from random import randint
import tkinter.font as tkfont
import numpy as np
from math import sqrt
from tkinter import *
import argparse
import re
import csv
import time
import pickle

# p = re.compile (r'[a-zA-ZÀ-ÖØ-öø-ÿ]+')
p = re.compile (r"""
  [a-zA-ZÀ-ÖØ-öø-ÿ]+|
  [0-9.]+|
  [.,!?:;/¶-]|
  \n\n|
  --|
  \.\.\.""",re.VERBOSE )

dumpfile = "seque.dump"
seque = defaultdict (list)
sc = defaultdict (lambda: ' ')
tgs = []
wds = []
rowlist = []
termw,termh = 100,20
yratio = 2.1690 
hc,wc = None,None
after_id = None

tagcolors = [
  ("white", "#fafafa"),
  ("yellow", "#fdfdbd"),
  ("red", "#f8a3a8"),
  ("green", "#b6f3ae"),
  ("blue", "#b3ddfc"),
  ("violet", "#bfb2f3"),
]

def dist_ell (p):
  ratio2 = 2
  mx = termw/2
  my = termh/2
  x,y = p
  dy = y-my
  dx = ratio2 * (x-mx)
  return sqrt (dx**2 + dy**2)

def dist (p):
  mx = termw/2
  my = termh/2
  x,y = p
  dy = yratio * (y-my)
  dx = x-mx
  return sqrt (dx**2 + dy**2)

def manh_dist (p):
  mx = termw/2
  my = termh/2
  x,y = p
  dy = yratio * (y-my)
  dx = x-mx
  return abs (dx) + abs (dy)

def create_emptys ():
  global sc,rowlist
  rowlist = []
  md = termh//2
  sc = defaultdict (lambda: ' ')
  for y in range (1,termh+1):
    a = termw//2+1
    b = termw
    while dist_ell ((a,y)) <= termh//2-1:
      a += 1
    rowlist.append ((y,a,b,True))
  for y in range (termh,0,-1):
    a = 0
    b = termw//2-1
    while dist_ell ((b,y)) <= termh//2-1:
      b -= 1
    rowlist.append ((y,a,b,False))
  # print ("rowlist =",rowlist)
  rllen = sum ([(b-a) for (i,a,b,right) in rowlist])
  return rllen

def filename (i):
  return f"ngrams/gram-{i}-total.csv"

def read_seque1 (): # 15.7 s
  seque = defaultdict (list)
  for i in range (1,7):
    with open (filename (i)) as f:
      print ("Lege", filename (i))
      reader = csv.reader (f,delimiter='\t')
      for row in reader:
        k = " ".join (row [:-2])
        v = (row [-2],int (row [-1]),i)
        seque [k].append (v)
  return seque

def read_seque2 (): # 7.7 s
  print ("Lege", dumpfile)
  try:
    seque = pickle.load (open (dumpfile, "rb"))
  except FileNotFoundError:
    print ("Non trovate.")
    seque = read_seque1 ()
    pickle.dump (seque, open (dumpfile, "wb"))
    print ("Scribeva", dumpfile)
  return seque

def seque_plus2 (s,maxm):
  n = maxm
  parolas = p.findall (s)
  s1 = []
  for i in range (0,len(parolas)+1):
    si = " ".join (parolas [i:])
    # s1.extend (seque [si][:n])
    s1.extend (
      [a for a in seque [si][:n] if a[0] not in [s[0] for s in s1]])
    n = maxm - len (" ".join ([s[0] for s in s1]))
    if n <= 0:
      break
  return s1

def seque_plus (s,n):
  return seque_plus2 (s, n)

search_wd = ""

def prt (*xs,sep=' ',end='\n'):
  x = sep.join ([str (x) for x in xs])
  text2.insert ("end", x + end)

# lines = ['line 1\n','line 2\n', 'line 3\n']
def read_args ():
  parser = argparse.ArgumentParser (description=
    'Lege regulas, dictionarios e documentos.')
  parser.add_argument ('-g', '--ngrammas', nargs='+', 
    action='extend')
  parser.add_argument ('-r', '--regulas', nargs='+', 
    action='extend')
  parser.add_argument ('-f', '--files', nargs='+', 
    action='extend')
  parser.add_argument ('-d', '--dicts', nargs='+', 
    action='extend')
  args = parser.parse_args ()

  ngrammas,dicts,regulas,lines = [],[],[],[]
  dic_wds = {}
  if not args.ngrammas:
    args.ngrammas = []
  if not args.regulas:
    args.regulas = []
  if not args.files:
    args.files = []
  if not args.dicts:
    args.dicts = []

  start = time.time ()
  seque = read_seque2 ()
  end = time.time ()
  print (end - start, "secundas")

  prt ("Files:")
  lines = (["¶"])
  for i,e in enumerate (args.files):
    prt (f"  {i+1}: {e}")
    filename = args.files [i]
    with open (filename) as f:
      lines = lines + f.readlines ()
  prt ()
  for rgl in regulas:
    prt (rgl)
  return seque,dic_wds,regulas,lines

def aeiou (ste):
  if len (ste) == 2:
    st,k = ste
  if len (ste) == 3:
    st,k,i = ste
  a = "abcdefghijklmnopqrstuvwxyz"
  b = "aeiounlsrtcdmpvbghfqjkxyzw"
  result = ""
  for c in st:
    d = c
    if c in b:
      d = a [b.index(c)]
    result += d
  return result

def inner_length (lst):
  result = 0
  for w in lst:
    result += len (w)
  return result

def strs1 (lst):
  return [a for (a,b,c) in lst]

def strs2 (lst):
  return [a for (a,b) in lst]

def str3 (lst):
  result = []
  for i,(a,b,c) in enumerate (lst):
    # result.append ((f"{a} ({b}) ",c))
    result.append ((f"{a} ",c))
  return result

def len_fsts2 (wds):
  result = []
  for a,b in wds:
    result.append (a)
  return len (" ".join (result))

def len_fsts3 (wds):
  result = []
  for a,b,c in wds:
    result.append (a)
  return len (" ".join (result))

def remove_all_tags ():
  global tgs  
  tgs = []
  for tag in text1.tag_names ():
    # print ("deleting", tag)
    text1.tag_remove (tag,"1.0","end")

def add_seques (s):
  global wds
  print ("add_seques (s)")
  # generate () # ?
  remove_all_tags ()
  rllen = create_emptys ()
  text1.delete ("1.0", END)
  # print ("nearest", rowlist_nearest())
  
  sg = seque_plus (s,rllen)
  result = str3 (sg)
  print ("len (result) = ",len (result))
  print (str(result)[:80])
  wds = sorted (sg,key=aeiou)
  print ("wds = ")
  print (str(wds)[:80])

  # print (s)
  # print ("inner_length ()",inner_length (s))
  distr_wds = distribute (wds,rowlist)
  new_sc (distr_wds,rowlist)
  txt = []
  for y in range (1,termh+1):
    ln = ""
    for x in range (0,termw):
      ln += sc [(x,y)]
    txt.append (ln)
    # print ("ln =\n" + str(ln)[:80])
    # print (str(ln)[:80])
    f = distr_wds [y-1] + distr_wds [2*termh - y]
    # print (" ".join (strs2(f))[:80])
    # print ("f =\n" + str(f)[:80])
    for (word,score,tg) in f:
      h = re.search(r"(?<= )" + re.escape (word) + r"(?= )"," " + ln + " ")
      if h:
        tgs.append ((tagcolors[tg-1][0],(h.start()-1,y),(h.end()-1,y)))
  text1.insert ("end", "\n".join (txt))

  for tg in tgs:
    tagname,(x1,y1),(x2,y2) = tg
    text1.tag_add (tagname, f"{y1}.{x1}", f"{y2}.{x2}")

def add_lines (lines):
  text2.delete ("1.0", END)
  text2.insert ("1.0", "".join (lines))

def itd (r,c):
  return str(r) + "." + str(c)

def txt_word_at (index):
  row,col = index.split (".")
  start = int (col)
  while start >= 0 and p.match (text1.get (itd (row,start))):
    start -= 1
  start += 1
  end = int (col)
  while p.match (text1.get (itd (row,end))):
    end += 1
  wd = text1.get (itd (row,start), itd (row,end))
  return wd

def five_words (index):
  row,col = index.split(".")
  start = int (col)
  five = 5
  while start >= 0 and five >= 0:
    while start >= 0 and p.match (text2.get (itd (row,start))):
      start -= 1
    start -= 1
    five -= 1
  start += 1
  end = int (col)
  wd = text2.get (itd (row,start), itd (row,end))
  return wd.strip()

def add_selected ():
  global sel
  sel = None
  idx = text2.index (INSERT)
  # print (f"ADD '{search_wd}' at {idx}")
  text2.insert (INSERT, f" {search_wd}")
  idx = text2.index (INSERT)
  new_seques = five_words (idx)
  print (f"new_seques: '{new_seques}'")
  add_seques (new_seques)

def distrlen2 (d,lst):
  s = " ".join ([x[0] for x in lst])
  k,ks = 0,[]
  for x in lst:
    k += len (x[0])+1
    ks.append (k/len(s))
  t,ts = [],[]
  for t1 in d:
    t.append (t1)
    ts.append (sum (t)/ sum (d))
  e = []
  for a in ts:
    c = []
    for b in ks:
      c.append (abs (a-b))
    # print ([f"{x:.2f}" for x in c])
    e.append (c.index (min (c)))
  print (str(e)[:80])
  print ("len e =",len (e))
  print (" ".join ([x[0] for x in lst])[:80])
  print (" ".join ([str(i).rjust (len (x [0]),"z")[-len (x [0]):] for i,x in enumerate (lst)])[:80])
  print (" ".join ([(x-1)*"x" for x in d])[:80])
  vs = {i:z for i,z in enumerate ([lst[a+1:b+1] for a,b in zip ([-1]+e,e)])}
  
  print ("vs =")
  print (str(vs)[:80])
  return vs 

def ranked_score (x):
  wd,score,tg = x
  return (10 ** tg) * score  

def distribute (wds,rowlist):
  print ("distribute (wds,rowlist)")
  d = []
  for (y,x1,x2,right) in rowlist:
    d.append (x2-x1)
  print ("d =")
  print (str(d)[:80])
  print ("sum d =", sum (d))
  newlist = sorted (wds,key=ranked_score,reverse=True)
  print ("sort1 =")
  print (str(newlist)[:80])
  newlist2 = sorted (wds,key=aeiou)
  print ("sort2 =")
  print (str(newlist2)[:80])
  print ("len sort2 =", len (newlist2))
  dl2 = distrlen2 (d,newlist2)
  return dl2
  # return dl

def new_sc (distr_wds,rowlist):
  global sc
  b = 0
  sc = defaultdict (lambda: ' ')
  for (y,x1,x2,right) in rowlist:
    assert distr_wds[b], f"distr_wds[{b}] does not exist"
    # print (str(distr_wds[b])[:80])
    #ns = [s[0] for s in sorted (distr_wds[b],key=lambda x:x[1],reverse=True)]
    ns = [s[0] for s in sorted (distr_wds[b],key=ranked_score,reverse=True)]
    a,k = 1,""
    while a <= len (ns) and len (" ".join (ns[:a])) <= x2 - x1:
      if right:
        k = " ".join (ns[:a])
      else:
        k = " ".join (reversed (ns[:a]))
      a += 1
    if not right:
      k = k.rjust (x2-x1)
    for i,c in enumerate (k):
      if x1+i < x2:
        sc [x1+i,y] = c
    b += 1

def get_screen_size ():
  global hc,wc,termw,termh
  w = text1.winfo_width()
  h = text1.winfo_height()
  print(f"w × h = {w} × {h}")
  if hc:
    termw = w // wc
    termh = h // hc
  else:
    wc = w // termw
    hc = h // termh
  print(f"wc × hc = {wc} × {hc}")
  print(f"termw × termh = {termw} × {termh}")

def on_leave (event):
  global sel
  sel = None

def on_mouse_move (event):
  global search_wd, start, sel
  index = text1.index (f"@{event.x},{event.y}")
  ch = text1.get (index)
  wd_under_cursor = txt_word_at (index).lower ()
  sel = wd_under_cursor
  if search_wd != wd_under_cursor and wd_under_cursor:
    start = time.time ()
    search_wd = wd_under_cursor
    label1.config (text= " ● " + search_wd)
    # print (f"'{search_wd}'")

def update_clock_mov ():
  global start_mov, mov
  end = time.time ()
  root.after (45, update_clock_mov)
  if mov:
    proginit = 100 * (end - start_mov)
  else:
    proginit = 0 
    start_mov = time.time ()
  if proginit >= 100:
    print ("proginit > 100")
    get_screen_size ()
    add_selected () # dont! Only when inited?
    mov = False

def update_clock_sel ():
  global start_sel, sel
  end = time.time ()
  root.after (45, update_clock_sel)
  if sel:
    progval = 100 * (end - start_sel)
  else:
    progval = 0 
    start_sel = time.time ()
    label1.config (text= "")
  progress ['value'] = progval
  if progval >= 100:
    add_selected ()

def create_tag_names ():
  for (a,b) in tagcolors:
    text1.tag_configure (a, background=b)

def movect (event):
  global start,mov
  start = time.time ()
  mov = True

root = Tk ()
root.title ('Thoreau scriptor')
root.iconphoto (False, PhotoImage (file='thoreau-scriptor.png'))
clr = "#f7c29c"
fnt = ("Monospace", 9)

frame1 = Frame (root)
frame3 = Frame (root)
frame2 = Frame (root)
scroll1 = Scrollbar (frame1)
scroll2 = Scrollbar (frame2)
text1 = Text (
  frame1, width=termw, height=termh, bg=clr, bd=0, font=fnt,
  wrap=NONE, cursor="cross")
text2 = Text (
  frame2, height=10, bg=clr, bd=0, font=fnt, width=100,
  wrap=WORD)
label1 = Label (
  frame3, bg=clr, bd=0, width=67, font=fnt, anchor=W, 
  justify=LEFT)
progress = Progressbar (
  frame3, orient = HORIZONTAL, length = 250, 
  mode = 'determinate') 

scroll1.pack (side=RIGHT, fill=Y)
text1.pack (side=LEFT, fill=BOTH, expand=True)
scroll2.pack (side=RIGHT, fill=Y)
text2.pack (side=LEFT, fill=X, expand=True)
frame1.pack (side=TOP, fill=BOTH, expand=True)
frame3.pack (side=TOP, fill=X)
frame2.pack (side=BOTTOM, fill=X)
label1.pack (side=LEFT, fill=X, expand=True)
progress.pack (side=RIGHT, fill=X)

scroll1.config (command=text1.yview)
scroll2.config (command=text2.yview)
text1.config (yscrollcommand=scroll1.set)
text2.config (yscrollcommand=scroll2.set)
text1.bind ("<Any-Motion>", on_mouse_move)
text1.bind ("<Leave>", on_leave)
text1.bind("<Configure>", movect)
text2.focus ()

create_tag_names ()
seque,dic_wds,regulas,lines = read_args ()
add_lines (lines)
start_sel = time.time ()
start_mov = time.time ()
sel = False
mov = False

update_clock_sel ()
update_clock_mov ()
root.mainloop ()


