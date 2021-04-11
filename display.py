def display(html):
  in_tag = False
  for c in html:
    if c == "<":
      in_tag = True
    elif c == ">":
      in_tag = False
    elif not in_tag:
      print(c, end="")

if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: display.py <html>"
  html = sys.argv[1]
  display(html)