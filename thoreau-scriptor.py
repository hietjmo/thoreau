
# python thoreau-scriptor.py --log +BCDEFGHW
# python thoreau-scriptor.py -f arbores.txt thoreau-initio.txt

from collections import defaultdict
from tkinter.ttk import Progressbar
from math import sqrt,sin,cos
from tabulate import tabulate
from random import randint
from tkinter import *
import argparse
import pickle
import pprint
import time
import csv
import re

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
tgs,wds,rowlist,tabs = [],[],[],[]
termw,termh = 110,30
yratio = 2.1690 
hc,wc = None,None
logwin,note,after_id = None,None,None
logs = defaultdict (lambda: '')
search_wd,logging = "",""

tagcolors = [
  ("white",  "#fafafa"),
  ("yellow", "#fdfdbd"),
  ("red",    "#f8a3a8"),
  ("green",  "#b6f3ae"),
  ("blue",   "#b3ddfc"),
  ("violet", "#bfb2f3"),
]

def create_emptys ():
  global sc,rowlist
  rowlist = []
  md = termh // 2
  sc = defaultdict (lambda: ' ')
  r = randint (0,9999)

  for y in range (1,termh+1):
    a = termw // 2 + 1
    b = termw
    a += round (1.5 + 3 * sin ((y+r)/2)) + 5
    rowlist.append ((y,a,b,True))

  for y in range (termh,0,-1):
    a = 0
    b = termw // 2 - 1
    b += round (1.5 + 3 * sin ((y+r)/2)) - 5
    rowlist.append ((y,a,b,False))

  rllen = sum ([(b-a) for (i,a,b,right) in rowlist])
  return rllen

def filename (i):
  return f"ngrams/gram-{i}-total.csv"

def read_seque1 (): # 15.7 s
  seque = defaultdict (list)

  for i in range (1,7):
    with open (filename (i)) as f:
      print (f"Lege {filename (i)}")
      reader = csv.reader (f,delimiter='\t')
      for row in reader:
        k = " ".join (row [:-2])
        v = (row [-2],int (row [-1]),i-1)
        seque [k].append (v)
  return seque

def read_seque2 (): # 7.7 s
  print (f"Lege {dumpfile}")
  try:
    seque = pickle.load (open (dumpfile,"rb"))
  except FileNotFoundError:
    print ("Non trovate. Lege n-grammas.")
    seque = read_seque1 ()
    pickle.dump (seque, open (dumpfile,"wb"))
    print (f"\nScribeva {dumpfile}")
  return seque

def add_to (s0,b,c):
  s0 [c] = s0 [c] + b
  return s0

def seque_plus2 (s,maxm):
  parolas = p.findall (s)
  s1 = defaultdict (lambda: [0,0,0,0,0,0]) 

  for i in range (0,len(parolas)+1):
    si = " ".join (parolas [i:])
    for a,b,c in seque [si][:maxm]:
      s1 [a] = add_to (s1[a],b,c)
    maxm -= len (" ".join (s1.keys ()))
    if maxm <= 0:
      break
  return [
    [k,v[5],v[4],v[3],v[2],v[1],v[0]] for k,v in s1.items ()]

def seque_plus (s,n):
  return seque_plus2 (s, n)

def log_me (c, s):
  if c in logging:
    if logwin:
      current_tab = note.tab (note.select (),"text")
      if current_tab == c:
        text3.delete ("1.0", END)
        text3.insert (END, s)
    else:
      print (f"{c} · {s}")
    logs[c] = s

def prt (*xs,sep=' ',end='\n'):
  log_me ("S", f"{sep.join ([str (x) for x in xs])}")

def read_args ():
  global logging
  parser = argparse.ArgumentParser (
    description='Lege regulas, dictionarios e documentos.')
  t1 = [
   ('-g','--ngrammas'),
   ('-r','--regulas'),
   ('-f','--files'),
   ('-d','--dicts'),
  ]
  for a,b in t1:
    parser.add_argument (a,b,nargs='+',action='extend',
    default=[])
  parser.add_argument ('-l','--log',default=logging)
  args = parser.parse_args ()
  if args.log[0:1] == "+":
    logging += args.log[1:]
  else:
    logging = args.log
  ngrammas,dicts,regulas,lines = [],[],[],[]
  dic_wds = {}
  start = time.time ()
  seque = read_seque2 ()
  end = time.time ()
  print (f"{end - start:.3f} secundas")

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

aie = "aeiounlsrtcdmpvbghfqjkxyzw"
abc = "abcdefghijklmnopqrstuvwxyz"

def aein (c):
  return aie.find (c)
  
def aeiou (ste):
  [w,t5,t4,t3,t2,t1,t0] = ste
  return "".join (
    [abc [aie.index (c)] if c in aie else c for c in w])

def remove_all_tags ():
  global tgs  
  tgs = []
  for tag in text1.tag_names ():
    text1.tag_remove (tag,"1.0","end")

def table6 (dic):
  table = []
  for k,v in dic.items():
    table.append ((k,str(v)))
  return table

def table4 (wds):
  tb5h = ['i','parola','5','4','3','2','1','0','score']
  newtab = []
  for j,w in enumerate (wds):
    [a,t5,t4,t3,t2,t1,t0] = w
    newtab.append ([j,a,t5,t4,t3,t2,t1,t0,ranked_score(w)])
  return tabulate (newtab, headers=tb5h)

def add_seques (s):
  global wds
  remove_all_tags ()
  rllen = create_emptys () # // 5
  text1.delete ("1.0", END)
  
  sg = seque_plus (s,rllen)
  log_me ("C", f"sg: \n" + table4 (sg) + 
    f"\n\nrllen = {rllen}")
  wds = sorted (sg,key=aeiou)
  log_me ("D", f"wds: \n" + table4 (wds))
  distr_wds = distribute (wds,rowlist)
  logtabu = pprint.pformat (table6 (distr_wds))
  log_me ("F", f"distr_wds:\n{logtabu}") 
  log_me ("G", f"rowlist:\n{tabulate(rowlist)}") 
  new_sc (distr_wds,rowlist)
  txt = []

  for y in range (1,termh+1):
    ln = ""
    for x in range (0,termw):
      ln += sc [(x,y)]
    txt.append (ln)
    f = distr_wds [y-1] + distr_wds [2*termh - y]
    for w in f:
      [word,t5,t4,t3,t2,t1,t0] = w
      tg = aein (word [0]) % 6
      h = re.search (
        r"(?<= )" + re.escape (word) + 
        r"(?= )"," " + ln + " ")
      if h:
        tgs.append (
         (tagcolors[tg][0],(h.start()-1,y),(h.end()-1,y)))
  text1.insert ("end", "\n".join (txt))
  log_me ("H", f'\n'.join (txt))
  for tg in tgs:
    tagname,(x1,y1),(x2,y2) = tg
    text1.tag_add (tagname, f"{y1}.{x1}", f"{y2}.{x2}")

def add_lines (lines):
  text2.delete ("1.0", END)
  text2.insert (END, "".join (lines))

def itd (r,c):
  return str (r) + "." + str (c)

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
  row,col = index.split (".")
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
  return wd.strip ()

def add_selected ():
  global sel
  sel = None
  idx = text2.index (INSERT)
  text2.insert (INSERT, f" {search_wd}")
  idx = text2.index (INSERT)
  last_five = five_words (idx)
  log_me ("E", f"last_five: '{last_five}'")
  add_seques (last_five)

def init_seq ():
  global sel
  sel = None
  idx = text2.index (INSERT)
  last_five = five_words (idx)
  log_me ("E", f"last_five: '{last_five}'")
  add_seques (last_five)

def distrlen2 (d,lst):
  s = " ".join ([x[0] for x in lst])
  log_me ("B", f's = "{s}"\n')
  k,ks = 0,[]

  for x in lst:
    k += len (x[0]) + 1
    ks.append (k / len (s))
  t,ts = [],[]

  for t1 in d:
    t.append (t1)
    ts.append (sum (t) / sum (d))
  e = []

  for a in ts:
    c = []
    for b in ks:
      c.append (abs (a-b))
    e.append (c.index (min (c)))
  vs = {i:z for i,z in enumerate (
    [lst [a+1:b+1] for a,b in zip ([-1]+e,e)])}
  return vs 

def ranked_score (wd):
  result = 0
  for i,t in enumerate (wd [6:0:-1]):
    result += (10 ** i) * t
  return result  

def distribute (wds,rowlist):
  d = []
  for (y,x1,x2,right) in rowlist:
    d.append (x2-x1)
  newlist  = sorted (wds,key=ranked_score,reverse=True)
  newlist2 = sorted (wds,key=aeiou)
  dl2 = distrlen2 (d,newlist2)
  return dl2

def new_sc (distr_wds,rowlist):
  global sc
  b = 0
  sc = defaultdict (lambda: ' ')

  for (y,x1,x2,right) in rowlist:
    assert distr_wds[b], f"distr_wds[{b}] does not exist"
    ns = [s[0] for s in sorted (
      distr_wds[b],key=ranked_score,reverse=True)]
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
  w = text1.winfo_width ()
  h = text1.winfo_height ()

  if hc:
    termw = w // wc
    termh = h // hc
  else:
    wc = w // termw
    hc = h // termh

def on_leave (event):
  global sel
  sel = None

def on_mouse_move (event):
  global search_wd,start,sel
  index = text1.index (f"@{event.x},{event.y}")
  ch = text1.get (index)
  wd_under_cursor = txt_word_at (index).lower ()
  sel = wd_under_cursor

  if search_wd != wd_under_cursor and wd_under_cursor:
    start = time.time ()
    search_wd = wd_under_cursor
    label1.config (text= " ● " + search_wd)

def update_clock_mov ():
  global start_mov,mov
  end = time.time ()
  root.after (45, update_clock_mov)

  if mov:
    proginit = 100 * (end - start_mov)
  else:
    proginit = 0 
    start_mov = time.time ()

  if proginit >= 100:
    get_screen_size ()
    init_seq ()
    mov = False

def update_clock_sel ():
  global start_sel,sel
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

def on_tab_selected (event):
  selected_tab = event.widget.select ()
  tab_text = event.widget.tab (selected_tab,"text")

  if logs [tab_text]:
    text3.delete ("1.0", END)
    text3.insert (END, logs [tab_text])

def on_close ():
  global logwin,logging
  logwin.destroy ()
  logging = ""
  logwin = None

def logWindow ():
  global logwin
  logwin = Toplevel (root)
  logwin.title ("Log Window")
  note = ttk.Notebook (logwin)
  tabs = []

  for c in logging:
    tabs.append (Frame (logwin))
    note.add (tabs[-1],text=f"{c}")
  note.bind ("<<NotebookTabChanged>>", on_tab_selected)
  scroll3 = Scrollbar (logwin)
  text3 = Text (
    logwin, height=50, bg=clr, bd=0, font=fnt, width=100,
    wrap=WORD)
  note.pack (side=TOP, fill=X)
  text3.pack (side=LEFT, fill=BOTH, expand=True)
  scroll3.config (command=text3.yview)
  text3.config (yscrollcommand=scroll3.set)
  scroll3.pack (side=RIGHT, fill=Y)
  logwin.protocol ("WM_DELETE_WINDOW", on_close)
  return text3,note,tabs

root = Tk ()
root.title ('Thoreau scriptor')
root.iconphoto (False, PhotoImage (file='thoreau-scriptor.png'))
clr = "#f7c29c"
fnt = ("Monospace", 9)

frame1,frame2,frame3 = Frame(root),Frame(root),Frame(root)
scroll1,scroll2 = Scrollbar(frame1),Scrollbar(frame2)
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
  frame3, orient=HORIZONTAL, length=250, 
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
text1.bind ("<Configure>", movect)
text2.focus ()

create_tag_names ()
seque,dic_wds,regulas,lines = read_args ()
add_lines (lines)
start_sel = time.time ()
start_mov = time.time ()
sel,mov = False,False

update_clock_sel ()
update_clock_mov ()

if "W" in logging:
  logging = logging.replace ("W","")
  text3,note,tabs = logWindow ()

root.mainloop ()

