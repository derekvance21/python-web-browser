entitytable = {
  "nbsp": ' ',
  "lt": '<',
  "gt": '>',
  "amp": '&',
  "quot": '"',
  "apos": '\'',
  "cent": '¢',
  "pound": '£',
  "yen": '¥',
  "euro": '€',
  "copy": '©',
  "reg": '®'
}

class Text:
  def __init__(self, text):
    self.text = text

class Tag:
  def __init__(self, tag):
    self.tag = tag


def transform(html):
  return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def lex(html, viewsource=False):
  html = transform(html) if viewsource else html
  out = []
  intag = False
  inentity = False
  entity = ""
  text = ""
  for c in html:
    if c == "<":
      intag = True
      if text: out.append(Text(text))
      text = ""
    elif c == ">":
      intag = False
      out.append(Tag(text))
      text = ""
    elif c == "&":
      entity = ""
      inentity = True
    elif inentity:
      if c == ";":
        text += entitytable.get(entity) or entity
        inentity = False
      else:
        entity += c
    else:
      text += c
  if not intag and text:
    out.append(Text(text))
  return out


if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: python3 parse.py <htmlfile>"
  htmlfile = sys.argv[1]
  with open(htmlfile, 'r') as f:
    html = f.read()
    print(lex(html))
  f.close()