
# python thoreau-ortho.py -i Vespertilio.txt

from tkinter import *
import argparse

search_wd = ""

def read_args ():
  parser = argparse.ArgumentParser ()
  parser.add_argument ("-i", "--infile")
  parser.add_argument (
    "-v", "--vocabulario", default="ia-ia-dic.txt")
  args = parser.parse_args ()
  return (args)

args = read_args ()

def add_lines (lines):
  text1.delete ("1.0", END)
  text1.insert ("1.0", "".join (lines))

wdrex = r'[a-zA-ZÀ-ÖØ-öø-ÿ]+'

def itd (r,c):
  return str(r) + "." + str(c)

def txt_word_at (index):
  row,col = index.split(".")
  start = int (col)
  while start >= 0 and re.match (wdrex,text1.get (itd (row,start))):
    start -= 1
  start += 1
  end = int (col)
  while re.match (wdrex, text1.get (itd (row,end))):
    end += 1
  wd = text1.get (itd (row,start), itd (row,end))
  return wd

def on_mouse_move (event):
  global search_wd
  index = text1.index (f"@{event.x},{event.y}")
  ch = text1.get (index)
  wd_under_cursor = txt_word_at (index).lower ()
  if search_wd != wd_under_cursor and wd_under_cursor:
    search_wd = wd_under_cursor
    if search_wd.lower () in parolas_dic:
      info = f"'{search_wd}' es un parola in {args.vocabulario}."
    else:
      info = f"'{search_wd}' NON es un parola in {args.vocabulario}."
    label1.config (text= " ● " + info)
    print (f"'{search_wd}'")

root = Tk ()
root.title ('Controlo orthographic')
root.iconphoto (False, PhotoImage (file='thoreau-ortho.png'))
clr = "#f99597"
fnt = ("Monospace", 9)

frame1 = Frame (root)
scroll1 = Scrollbar (frame1)
text1 = Text (
  frame1, height=25, bg=clr, bd=0, font=fnt, width=100, 
  wrap=WORD, cursor="cross")
label1 = Label (
  root, bg=clr, bd=0, width=96, font=fnt, anchor=W, 
  justify=LEFT)

scroll1.pack (side=RIGHT, fill=Y)
text1.pack (side=TOP, fill=BOTH, expand=True)
frame1.pack (side=TOP, fill=BOTH, expand=True)
label1.pack (side=BOTTOM,fill=X)

scroll1.config (command=text1.yview)
text1.config (yscrollcommand=scroll1.set)
text1.bind("<Any-Motion>", on_mouse_move)
text1.focus ()

text1.tag_configure (
  "triadic1", background="#97f995")

text1.tag_configure (
  "triadic2", background="#9597f9")

f = open (args.vocabulario)
parolas = [p.strip ().lower () for p in f.readlines ()]
f.close ()

parolas_dic = {p:"" for p in parolas}

g = open (args.infile)
text = g.read ()
g.close ()

w_re    =  r'[a-zA-ZÀ-ÖØ-öø-ÿ]*'
nonw_re = r'[^a-zA-ZÀ-ÖØ-öø-ÿ]*'
# r'(\w*)(\W*)'
# convert text to (word,non-word) -pairs:
pars = re.findall (f'({w_re})({nonw_re})',text)
for w,nonw in pars:
  if w.lower () in parolas_dic:
    text1.insert ("end",w)
  else:
    text1.insert ("end",w,"triadic1")
  text1.insert ("end",nonw)

text1.config (state=DISABLED) # read-only
# text1.configure (state=NORMAL)
root.mainloop ()

