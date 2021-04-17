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

def transform(html):
  return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def lex(html, viewsource=False):
  html = transform(html) if viewsource else html
  intag = False
  inhead = False
  inentity = False
  entity = ""
  tag = ""
  text = ""
  for c in html:
    if c == "<":
      tag = ""
      intag = True
    elif c == ">":
      if tag.lower().startswith("/head"):
        inhead = False 
      elif tag.lower().startswith("head"):
        inhead = True
      intag = False
    elif c == "&":
      entity = ""
      inentity = True
    elif inentity:
      if c == ";":
        inentity = False
        translation = entitytable.get(entity)
        text += translation or c
      else:
        entity += c
    elif intag:
      tag += c
    elif not inhead or viewsource:
      text += c
  return text


if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: python3 parse.py <htmlfile>"
  htmlfile = sys.argv[1]
  with open(htmlfile, 'r') as f:
    html = f.read()
    print(lex(html))
  f.close()