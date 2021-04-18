import parse
import tkinter.font
from constants import MARGIN, FONT_FAMILY

class Layout:
  def __init__(self, browser, tokens):
    self.displaylist = [] 
    self.line = []
    self.cursor_x, self.cursor_y = MARGIN, MARGIN
    self.fontsize = browser.fontsize
    self.width = browser.width
    self.weight, self.style = "normal", "roman"
    for token in tokens:
      self.token(token)
    self.flush()

  def token(self, token):
    if isinstance(token, parse.Text): self.text(token.text)
    elif token.tag == "i":
      self.style = "italic"
    elif token.tag == "/i":
      self.style = "roman"
    elif token.tag == "b":
      self.weight = "bold"
    elif token.tag == "/b":
      self.weight = "normal"
    elif token.tag == "small":
      self.fontsize -= 2
    elif token.tag == "/small":
      self.fontsize += 2
    elif token.tag == "big":
      self.fontsize += 4
    elif token.tag == "/big":
      self.fontsize -= 4
    elif token.tag == "br":
      self.flush()
    elif token.tag == "/p" or token.tag.startswith("/h"):
      self.flush()
      self.cursor_y += MARGIN

  def text(self, text):
    if any([ord(c) >= 65536 for c in text]): return
    font = tkinter.font.Font(family=FONT_FAMILY, size=self.fontsize, weight=self.weight, slant=self.style)
    for word in text.split():
      w = font.measure(word)
      if self.cursor_x + w >= self.width - MARGIN:
        self.flush()
      self.line.append((self.cursor_x, word, font))
      self.cursor_x += w + font.measure(" ")

  def flush(self):
    if not self.line: return
    metrics = [font.metrics() for x, word, font in self.line]
    maxascent = max([metric["ascent"] for metric in metrics])
    baseline = self.cursor_y + 1.2 * maxascent
    for x, word, font in self.line:
      y = baseline - font.metrics("ascent")
      self.displaylist.append((x, y, word, font))
    self.cursor_x = MARGIN
    self.line = []
    maxdescent = max([metric["descent"] for metric in metrics])
    self.cursor_y = baseline + 1.2 * maxdescent
