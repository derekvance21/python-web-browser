import tkinter as tk
import tkinter.font
import request
import parse
from layout import Layout
from constants import WIDTH, HEIGHT, SCROLL_STEP, FONT_SIZE, MARGIN

class Browser:
  
  def __init__(self):
    self.window = tk.Tk()
    self.window.bind("<Down>", self.scrolldown)
    self.window.bind("<Up>", self.scrollup)
    self.window.bind("<MouseWheel>", self.scrollwheel)
    self.window.bind("<Configure>", self.resize)
    self.window.bind("<Control-+>", self.zoomin)
    self.window.bind("<Control-minus>", self.zoomout)
    self.canvas = tk.Canvas(self.window, width=WIDTH, height=HEIGHT)
    self.canvas.pack(expand=1, fill="both")
    self.scroll = 0
    self.width, self.height = WIDTH, HEIGHT
    self.fontsize = FONT_SIZE

  def zoomin(self, e):
    self.fontsize = int(self.fontsize * 1.25)
    self.update()

  def zoomout(self, e):
    self.fontsize = max(4, int(self.fontsize * 0.8))
    self.update()

  def resize(self, e):
    self.width, self.height = e.width, e.height
    self.update()

  def scrolldown(self, e):
    self.scroll += SCROLL_STEP
    self.update(layout=False)

  def scrollup(self, e):
    self.scroll = max(0, self.scroll - SCROLL_STEP)
    self.update(layout=False)

  def scrollwheel(self, e):
    self.scroll = max(0, self.scroll - e.delta)
    self.update(layout=False)
    
  def render(self):
    self.canvas.delete("all")
    for x, y, word, font in self.displaylist:
      if y > self.scroll + self.height: continue
      if y + MARGIN < self.scroll: continue
      self.canvas.create_text(x, y - self.scroll, text=word, anchor='nw', font=font)

  def update(self, layout=True):
    if layout:
      self.displaylist = Layout(self, self.tokens).displaylist
    self.render()

  def load(self, url):
    header, body = request.request(url)
    self.tokens = parse.lex(body) if header.get("content-type").startswith("text/html") else body
    self.update()


if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: src/window.py <url>"
  url = sys.argv[1]
  Browser().load(url)
  tk.mainloop()