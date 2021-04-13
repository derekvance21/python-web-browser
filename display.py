def display(html):
  intag = False
  inbody = False
  tag = ""
  for c in html:
    if c == "<":
      tag = ""
      intag = True
    elif c == ">":
      inbody = False if tag.lower().startswith("/body") else inbody or tag.lower().startswith("body")
      intag = False
    elif intag:
      tag += c
    elif not intag and inbody:
      print(c, end="")

if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: display.py <htmlfile>"
  htmlfile = sys.argv[1]
  with open(htmlfile, 'r') as f:
    html = f.read()
    display(html)
  f.close()