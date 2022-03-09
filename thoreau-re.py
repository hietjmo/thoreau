#!/usr/bin/python

# python thoreau-re.py --diaereses IED-utf8.txt fi20.txt thesauro-2.txt dei-2021-09-14.txt

# python thoreau-re.py IED-utf8.txt fi20.txt thesauro-2.txt
# python thoreau-re.py ~/interlingua/macovei/wikisource/dictionario-encyclopedic-2021-06-28.txt --num 100 --log

from tkinter import *
from math import *
import argparse
import sys
import time

history = []

def prt (*xs,sep=' ',end='\n'):
  text1.config (state=NORMAL)
  x = sep.join ([str (x) for x in xs])
  text1.insert ("end", x + end)
  text1.config (state=DISABLED)

def linea (char='-',length=60):
  prt (length * char)

# lines = ['line 1\n','line 2\n', 'line 3\n']

def read_args ():
  parser = argparse.ArgumentParser ()
  pad = parser.add_argument
  pad ('dictfiles', nargs='*')
  pad ("-n", "--num", type=int, default=1000)
  pad ("--nonformat", action="store_true")
  pad ("--diaereses", action="store_true")
  pad ("--incsearch", action="store_true")
  pad ("--paramlist", action="store_true")
  pad ("--log", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

if args.paramlist:
  for arg in vars (args):
    print (f"{arg}: {getattr (args, arg)}")

def read_args2 ():
  lines = []
  prt ("Files de dictionarios:")
  linea ()
  for i,e in enumerate (args.dictfiles):
      prt (f"{i+1}: {e}")
      filename = args.dictfiles[i]
      with open (filename) as f:
        lines = lines + f.readlines ()
  linea ()
  prt ("In toto",len (lines),"lineas")
  linea ()
  return lines

def try_compile (word):
  regex = None
  if len (word) > 0:
    try:
      regex = re.compile (word)
    except:
      pass
  return regex

def find_words (word):
  xs = []
  regex = try_compile (word)
  if regex:
    for s in lines:
      m = regex.search (s)
      if m: 
        xs.append ((m.start(),s))
    xs.sort ()
  ys = xs [:max_m]  
  result = [str (i+1) + " ▶ " + s for i,(b,s) in enumerate (ys)]
  d = len (xs) - len (ys)
  if d > 0: 
    result.append (f"(+ {d} alteres)")
  return result

def show_history ():
  text1.config (state=NORMAL)
  global history
  result = (["Historia:"] +
    [str (i+1) + " ▶ " + s for i,s in enumerate (history)])
  print (history)
  text1.delete ("1.0", END)
  text1.insert ("1.0", "\n".join (result))
  text1.config (state=DISABLED)

def find_all (s,sub):
  start = 0
  while True:
    start = s.find (sub,start)
    if start == -1: return
    yield start
    start = start + len (sub) 

def add_style (t):
  text1.config (state=NORMAL)
  stilo,expr = t
  txt = text1.get ("1.0", END).split("\n")
  regex = try_compile (expr)
  for i,s in enumerate (txt):
    lastpos = 0
    while True:
      m = regex.search (s,lastpos)
      if not m: 
        break
      new = m.group (1)
      a,b = m.span ()
      idx1 = f"{i+1}.{a}"
      idx2 = f"{i+1}.{b}"
      lastpos = a + len (new)
      idx3 = f"{i+1}.{lastpos}"
      text1.delete (idx1,idx2)
      text1.insert (idx1,new)
      text1.tag_add (stilo, idx1, idx3)
      s = regex.sub (new,s,count=1)
  text1.config (state=DISABLED)

def return_pressed (event,sel=True):
  global history
  text1.config (state=NORMAL)
  start = time.time()
  word = text2.get ("1.0", "end-1c")
  label1.config (text= " ● " + word)
  result = find_words (word)
  text1.delete ("1.0", END)
  text1.insert ("1.0", "".join (result))
  text1.mark_set (INSERT, "30.0")
  repl_table = [
    ("bold", r"'''(.*?)'''"),
    ("italic", r"''(.*?)''"),
    ("underline", r"<u>(.*?)</u>"),
    ("inverse", fr"({word})")]
  for t in repl_table:
    add_style (t)
  end = time.time()
  total = end - start
  decimals = abs (floor (log (total,10))) + 2
  if args.log:
    print ("\n" + word)
    print (len(word)*"=" + "\n")
    print (f"({total:.{decimals}} s)\n") 
    print ("\n".join(result) + "\n")
  text1.config (state=DISABLED)
  history.append (word)
  history = history [-max_m:]
  if sel:
    select_input ()
    return "break" # handled, do not send further!

def callback (sv,w):
  s = sv.get ()
  n = "".join ([c for c in s if c in "1234567890"])
  sv.set (n)
  set_max_m ()

def int_def (st,default=0):
  try:
    result = int (st)
  except ValueError:
    result = default
  return result

max_m = args.num

def set_max_m ():
  global max_m
  max_m = int_def (spin1.get(),default=args.num)
  return_pressed (None)

def add_backslash_Ws ():
  text2.insert ('1.0', '\W')
  text2.insert (END, '\W')
  return_pressed (None)

def select_input ():
  text2.tag_add (SEL, "1.0", "end")
  text2.mark_set (INSERT, "1.0")
  text2.see (INSERT)

def select_all ():
  text2.tag_add(SEL, "1.0", END)
  text2.mark_set(INSERT, "1.0")
  text2.see(INSERT)
  return 'break'

def scroll_up ():
  text1.config (state=NORMAL)
  index = text1.index(INSERT)
  row,col = index.split(".")
  row,col = int (row),int (col)
  text1.mark_set (INSERT, f"{row-30}.0")
  text1.see (INSERT)
  text1.config (state=DISABLED)
  select_input ()
  return 'break'

def scroll_down ():
  text1.config (state=NORMAL)
  index = text1.index(INSERT)
  row,col = index.split(".")
  row,col = int (row),int (col)
  text1.mark_set (INSERT, f"{row+30}.0")
  text1.see (INSERT)
  text1.config (state=DISABLED)
  select_input ()
  return 'break'

def on_key_press (event):
  if args.log:
    print (event.keysym)
  if args.diaereses:
    if event.keysym=="adiaeresis":
      text2.insert (INSERT, 'ä')
    if event.keysym=="Adiaeresis":
      text2.insert (INSERT, 'Ä')
    if event.keysym=="odiaeresis":
      text2.insert (INSERT, 'ö')
    if event.keysym=="Odiaeresis":
      text2.insert (INSERT, 'Ö')
  # if args.incsearch:
  #   return_pressed (event,sel=False)

def on_release (event):
  if args.incsearch:
    return_pressed (event,sel=False)

def on_control_a (event):
  select_all ()

def on_control_h (event):
  show_history ()

def on_control_w (event):
  add_backslash_Ws ()

def on_control_l (event):
  args.log = not args.log

def on_control_i (event):
  args.incsearch = not args.incsearch
  return 'break'

def on_control_d (event):
  args.diaereses = not args.diaereses

def on_prior (event):
  scroll_up ()

def on_next (event):
  scroll_down ()

def on_enter (event):
  select_input ()

def handle_focus (event):
  if event.widget == root:
    select_input ()

root = Tk ()
root.title ('Cerca in dictionarios')
root.iconphoto (False, PhotoImage (file='thoreau-re.png'))
clr = "#a6f3cc"
fnt = ("Monospace", 9)

scroll1 = Scrollbar (root)
text1 = Text (
  root, height=40, bg=clr, bd=0, font=fnt, width=100, wrap=WORD)

frame1 = Frame (root)
text2 = Text (root, height=3, bg=clr, bd=0, font=fnt, width=100)
label1 = Label (
  frame1, bg=clr, bd=0, width=96, font=fnt, anchor=W, 
  justify=LEFT)
spinvar = StringVar (value=max_m)
spin1 = Spinbox (
  frame1,from_=0,to=5000,width=4,relief=FLAT,bd=0,
  buttondownrelief=FLAT,buttonuprelief=FLAT,increment=200,
  font=fnt, textvariable=spinvar,
  command=set_max_m)
spin1.delete(0, "end"); spin1.insert(0, max_m)
label1.pack (side=LEFT,fill=X)
spin1.pack (side=RIGHT)

text2.pack (side=BOTTOM, fill=X)

frame1.pack (side=TOP, fill=X)
scroll1.pack (side=RIGHT, fill=Y)
text1.pack (side=LEFT, fill=Y)

spinvar.trace('w', lambda name, index, mode, sv=spinvar: callback 
  (spinvar,spin1))
scroll1.config (command=text1.yview)
text1.config (yscrollcommand=scroll1.set)
text1.config (state=DISABLED)
text2.bind ('<Return>', return_pressed)
text2.bind ('<Enter>', on_enter)
text2.bind ('<KeyPress>', on_key_press)
text2.bind ("<KeyRelease>", on_release)
root_binds = [
  ("<FocusIn>", handle_focus),
  ("<Control-h>", on_control_h),
  ("<Control-y>", on_control_i),
  ("<Control-w>", on_control_w),
  ("<F1>", on_control_w),
  ("<Control-l>", on_control_l),
  ("<Control-a>", on_control_a),
  ("<Control-d>", on_control_d),
  ("<Prior>", on_prior),
  ("<Next>", on_next), ]
for a,b in root_binds:
  root.bind (a,b)

text2.focus ()

text1.tag_configure (
  "inverse", background="#f3a6cd")
for st in ["bold","italic","underline"]:
  text1.tag_configure (
    st, font=f"{fnt[0]} {fnt[1]} {st}")
lines = read_args2 ()
root.mainloop ()

# Make this file executable:
# :!chmod +x %

