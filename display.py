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


def display(html, viewsource=False):
  html = transform(html) if viewsource else html
  intag = False
  inbody = False
  inentity = False
  entity = ""
  tag = ""
  for c in html:
    if c == "<":
      tag = ""
      intag = True
    elif c == ">":
      inbody = False if tag.lower().startswith("/body") else inbody or tag.lower().startswith("body")
      intag = False
    elif c == "&":
      entity = ""
      inentity = True
    elif inentity:
      if c == ";":
        inentity = False
        translation = entitytable.get(entity)
        print(translation, end="")
      else: 
        entity += c
    elif intag:
      tag += c
    elif inbody or viewsource:
      print(c, end="")

if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: display.py <htmlfile>"
  htmlfile = sys.argv[1]
  with open(htmlfile, 'r') as f:
    html = f.read()
    display(html, True)
  f.close()