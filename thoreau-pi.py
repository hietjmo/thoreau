
# python thoreau-pi.py --log +BCDEFGHW
# python thoreau-scriptor.py -f arbores.txt thoreau-initio.txt

from collections import defaultdict
from tkinter.ttk import Progressbar
from math import sqrt,sin,cos,tau
from tabulate import tabulate
from tkinter import *
import argparse
import pickle
import time
import csv
import re

p = re.compile (r"""
  [a-zA-ZÀ-ÖØ-öø-ÿ]+|
  [0-9.]+|
  [.,!?:;/¶·\-]|
  \n\n|
  --|
  \.\.\.""",re.VERBOSE )

dumpfile = "seque.dump"
seque = defaultdict (list)
sc = defaultdict (lambda: ' ')
tgs,wds,rowlist,tabs = [],[],[],[]
termw,termh = 110,30
hc,wc = None,None
logwin,note,after_id = None,None,None
logs = defaultdict (lambda: '')
search_wd,logging = "",""
selx,sely = 0,0
phase = 0.0

tagcolors = [
  ("white",  "#fafafa"),
  ("yellow", "#fdfdbd"),
  ("red",    "#f8a3a8"),
  ("green",  "#b6f3ae"),
  ("blue",   "#b3ddfc"),
  ("violet", "#bfb2f3"),
]

with open ("pi1000000.txt") as f:
  content = f.read()
  pi = [int (c) for c in content if c in "0123456789"]

pi_man = "".join([str (c) for c in pi [:10000]])
pin = 0

def create_emptys ():
  global sc,rowlist,phase
  rowlist = []
  md = termh // 2
  sc = defaultdict (lambda: ' ')
  # r = randint (0,9999)
  phase = (phase + tau / 60) % tau


  for y in range (1,termh+1):
    a = termw // 2 + 1
    b = termw
    a += round (1.5 + 3 * sin ((y+phase)/2)) + 5
    rowlist.append ((y,a,b,True))

  for y in range (termh,0,-1):
    a = 0
    b = termw // 2 - 1
    b += round (1.5 + 3 * sin ((y+phase)/2)) - 5
    rowlist.append ((y,a,b,False))

  rllen = sum ([(b-a) for (i,a,b,right) in rowlist])
  return rllen

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

def seque_plus (s,maxm):
  log = []
  log.append (f"function seque_plus2")
  log.append (f"parameter s = {s}")
  log.append (f"parameter maxm = {maxm}")

  parolas = p.findall (s)
  log.append (f"\nparolas = {str(parolas)}")
  s1 = defaultdict (lambda: [0,0,0,0,0,0]) 

  for i in range (0,len(parolas)+1):
    log.append (f"\nfor loop: i = {i}")
    si = " ".join (parolas [i:])
    # maxm is in characters, now we count words (c. 4 chars):
    # for a,b,c in seque [si][:maxm // 4]:
    for a,b,c in seque [si][:50000]: # pi day 
      if (len (a) < 11 and len (a) % 10 == pi [pin] and 
        (all ([c in aie for c in a]))): 
        s1 [a] = add_to (s1[a],b,c)
    log.append (f"s1:\n{table5(s1)}")
    stkeys = " ".join (s1.keys ())
    maxm -= len (stkeys)
    log.append (f"\"{stkeys}\" ({len(stkeys)})")
    if maxm <= 0:
      break
  log_me ("A","\n".join(log))
  return [
    [k,v[5],v[4],v[3],v[2],v[1],v[0]] for k,v in s1.items ()]

def prt (*xs,sep=' ',end='\n'):
  log_me ("S", f"{sep.join ([str (x) for x in xs])}")

def read_args ():
  global logging,text3,note,tabs
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

  if "W" in logging:
    logging = logging.replace ("W","")
    text3,note,tabs = logWindow ()

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
  text2.delete ("1.0", END)
  text2.insert (END, "".join (lines))

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
    table.append (f"Rowlist row {k}:\n{table4(v)}")
  return "\n\n".join (table)

def table4 (wds):
  tb5h = ['i','parola','5','4','3','2','1','0','score']
  newtab = []
  for j,w in enumerate (wds):
    [a,t5,t4,t3,t2,t1,t0] = w
    newtab.append ([j,a,t5,t4,t3,t2,t1,t0,ranked_score(w)])
  return tabulate (newtab, headers=tb5h)

def table5 (dic):
  tb5h = ['i','parola','5','4','3','2','1','0']
  newtab = []
  i = 0
  for w in dic:
    [t0,t1,t2,t3,t4,t5] = dic [w]
    newtab.append ([i, w,t5,t4,t3,t2,t1,t0])
    i += 1
  return (
    tabulate (newtab, headers=tb5h) + 
    ("" if dic else "\ntable is empty"))

def add_seques (s):
  global wds
  log_me ("I", pi_man)
  remove_all_tags ()
  rllen = create_emptys () # // 5
  text1.delete ("1.0", END)
  
  sg = seque_plus (s,rllen)
  log_me ("B", f"sg = seque_plus (s,rllen): \n" + table4 (sg) + 
    f"\n\nrllen = {rllen}")
  wds = sorted (sg,key=aeiou)
  log_me ("C", f"wds = sorted (sg,key=aeiou):\n" + table4 (wds))
  distr_wds = distribute (wds,rowlist)
  log_me ("E", f"distr_wds = distribute (wds,rowlist):\n" + 
    "{table6 (distr_wds)}") 
  tbh = ['y','x1','x2','right']
  log_me ("F", f"Rowlist:\n{tabulate(rowlist,headers=tbh)}") 
  new_sc (distr_wds,rowlist)
  log_me ("J", f"sc:\n{sc}") 
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
  return wd,start,row

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
  global sel,pin
  if pin < len (pi):
    pin += 1
    label2.config (text=pi_man [pin:pin+20])
  else:
    pin = len (pi) - 1
    label2.config (text= "Out of decimals. Restart!")
    print ("Out of decimals. Restart!")
  sel = None
  idx = text2.index (INSERT)
  text2.insert (INSERT, f" {search_wd}")
  idx = text2.index (INSERT)
  last_five = five_words (idx)
  log_me ("G", f"last_five: '{last_five}'")
  add_seques (last_five)

def init_seq ():
  global sel
  sel = None
  idx = text2.index (INSERT)
  last_five = five_words (idx)
  log_me ("G", f"last_five: '{last_five}'")
  add_seques (last_five)

def distrlen2 (d,lst):
  s = " ".join ([x[0] for x in lst]) + " "
  log_me ("D", f'distrlen2 (d,lst), s = "{s}"\n')
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
  newlist2 = sorted (wds,key=aeiou)
  dl2 = distrlen2 (d,newlist2)
  return dl2

def divide_spatio (spatio):
  global sc
  letters = aie + "·¶"
  gone = set ()
  j = 0
  while len (letters) > 0 and j < 99:
    j += 1 
    i = 0
    while len (letters) > 0 and i in spatio:
      x,y,vacue,right,initials = spatio [i]
      c = letters [0]
      if (c in initials or c in gone) and vacue > 1:
        if right:
          sc[x+1,y] = c.upper()
          spatio [i] = x+2,y,vacue-2,right,initials.replace(c,"")
          letters = letters.replace(c,"")
        else:
          sc[x+vacue-2,y] = c.upper()
          spatio [i] = x-2,y,vacue-2,right,initials.replace(c,"")
          letters = letters.replace(c,"")
      gone.update ([c for c in initials])
      i += 1
    gone.update (letters)

def new_sc (distr_wds,rowlist):
  global sc
  b = 0
  sc = defaultdict (lambda: ' ')
  spatio = [] # spatio que remane
  for (y,x1,x2,right) in rowlist:
    dstr =  distr_wds [b] if distr_wds [b] else []
    ns = [s [0] for s in sorted (
      dstr,key=ranked_score,reverse=True)]
    a,k = 1,""
    # initials = set ()
    while a <= len (ns) and len (" ".join (ns[:a])) <= x2 - x1:
      if right:
        k = " ".join (ns[:a])
      else:
        k = " ".join (reversed (ns[:a]))
      # initials = "".join ({w[0] for w in ns[:a]})
      a += 1
    kl = len (k)
    sp = (x2-x1)-kl
    if not right:
      k = k.rjust (x2-x1)
      # spatio.append ((x1,y,sp,right,initials))
    else:
      pass
      # spatio.append ((x2-sp,y,sp,right,initials))
    for i,c in enumerate (k):
      if x1+i < x2:
        sc [x1+i,y] = c
    b += 1

  """
  tbh = ['x','y','vacue','right','initials']
  log_me ("I", 
    f"Spatio que remane:\n{tabulate(spatio,headers=tbh)}")
  spatio = dict (enumerate (spatio))
  divide_spatio (spatio)
  """

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
  global search_wd,start_sel,sel,selx,sely
  index = text1.index (f"@{event.x},{event.y}")
  ch = text1.get (index)
  wd1,selx,sely = txt_word_at (index)
  wd_under_cursor = wd1.lower ()
  sel = wd_under_cursor

  if search_wd != wd_under_cursor and wd_under_cursor:
    start_sel = time.time ()
    search_wd = wd_under_cursor
    label1.config (text= " ● " + search_wd)

def update_clock_conf ():
  global start_conf,conf
  end = time.time ()
  root.after (45, update_clock_conf)

  if conf:
    proginit = 100 * (end - start_conf)
  else:
    proginit = 0 
    start_conf = time.time ()

  if proginit >= 100:
    get_screen_size ()
    init_seq ()
    conf = False

def clear_and_highlight (search_wd,sely,selx):
  text1.delete ("1.0", END)
  for y in range (0,termh):
    text1.insert (END, termw * " " + "\n")
  text1.insert (f"{sely}.{selx}", search_wd )
  for i in range (0,len (search_wd)):
    tg = aein (search_wd [i]) % 6
    text1.tag_add (tagcolors[tg][0], f"{sely}.{selx+i}", f"{sely}.{selx+i+1}")
  # print (f"{sely}.{selx} {search_wd}")
  text1.update ()

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
    clear_and_highlight (search_wd,sely,selx)
    add_selected ()

def create_tag_names ():
  for (a,b) in tagcolors:
    text1.tag_configure (a, background=b)

def on_conf (event):
  global start_conf,conf
  start_conf = time.time ()
  conf = True

def on_tab_selected (event):
  selected_tab = event.widget.select ()
  tab_text = event.widget.tab (selected_tab,"text")

  if logs [tab_text]:
    text3.delete ("1.0", END)
    text3.insert (END, logs [tab_text])

def on_log_close ():
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
    logwin, height=50, bg=clr, bd=0, font=fnt, width=110,
    wrap=WORD)
  note.pack (side=TOP, fill=X)
  text3.pack (side=LEFT, fill=BOTH, expand=True)
  scroll3.config (command=text3.yview)
  text3.config (yscrollcommand=scroll3.set)
  scroll3.pack (side=RIGHT, fill=Y)
  logwin.protocol ("WM_DELETE_WINDOW", on_log_close)
  return text3,note,tabs

def on_close ():
  fileout = "le-ultime-texto.txt"
  written = text2.get("1.0",END)
  with open (fileout,"w") as f:
    f.write (written)
  print ("Scribeva", fileout)
  root.destroy()

root = Tk ()
root.title ('Thoreau Pi')
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
  frame3, bg=clr, bd=0, width=47, font=fnt, anchor=W, 
  justify=LEFT)
label2 = Label (
  frame3, bg=clr, bd=0, width=20, font=fnt, anchor=W, 
  justify=LEFT, text=pi_man [pin:pin+20])
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
label2.pack (side=LEFT, fill=X, expand=True)
progress.pack (side=RIGHT, fill=X)

scroll1.config (command=text1.yview)
scroll2.config (command=text2.yview)
text1.config (yscrollcommand=scroll1.set)
text2.config (yscrollcommand=scroll2.set)
text1.bind ("<Any-Motion>", on_mouse_move)
text1.bind ("<Leave>", on_leave)
text1.bind ("<Configure>", on_conf)
root.protocol ("WM_DELETE_WINDOW", on_close)
text2.focus ()

create_tag_names ()
seque,dic_wds,regulas,lines = read_args ()
start_sel = time.time ()
start_conf = time.time ()
sel,conf = False,False

update_clock_sel ()
update_clock_conf ()

root.mainloop ()

