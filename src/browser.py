import tkinter as tk
import request
import parse

FONT_SIZE = 8
SCROLL_STEP = 100
WIDTH, HEIGHT = 800, 600

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
    self.fontsize, self.vstep = FONT_SIZE, FONT_SIZE * 1.5

  def zoomin(self, e):
    self.fontsize += 1
    self.vstep = self.fontsize * 1.5
    self.layout()
    self.render()

  def zoomout(self, e):
    self.fontsize = max(2, self.fontsize - 1)
    self.vstep = self.fontsize * 1.5
    self.layout()
    self.render()

  def resize(self, e):
    self.width, self.height = e.width, e.height
    self.layout()
    self.render()

  def scrolldown(self, e):
    self.scroll += SCROLL_STEP
    self.render()

  def scrollup(self, e):
    self.scroll = max(0, self.scroll - SCROLL_STEP)
    self.render()

  def scrollwheel(self, e):
    self.scroll = max(0, self.scroll - e.delta)
    self.render()

  def layout(self):
    displaylist = []
    cursor_x, cursor_y = self.fontsize, self.vstep
    for c in self.text:
      if c == "\n":
        cursor_x = self.fontsize
        cursor_y += self.vstep * 2
      else:
        cursor_x += self.fontsize
        if cursor_x >= self.width - self.fontsize:
          cursor_x = self.fontsize
          cursor_y += self.vstep
        displaylist.append((cursor_x, cursor_y, c))
    self.displaylist = displaylist
    
  def render(self):
    self.canvas.delete("all")
    for x, y, c in self.displaylist:
      if y > self.scroll + self.height: continue
      if y + self.vstep < self.scroll: continue
      if ord(c) in range(65536):
        self.canvas.create_text(x, y - self.scroll, text=c, font=("", self.fontsize))

  def load(self, url):
    header, body = request.request(url)
    self.text = parse.lex(body) if header.get("content-type").startswith("text/html") else body
    self.layout()
    self.render()


if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: src/window.py <url>"
  url = sys.argv[1]
  Browser().load(url)
  tk.mainloop()