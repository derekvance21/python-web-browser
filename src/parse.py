ENTITY_TABLE = {
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

SELF_CLOSING_TAGS = [
  "area", "base", "br", "col", "embed", "hr", "img", "input",
  "link", "meta", "param", "source", "track", "wbr",
]

HEAD_TAGS = [
  "base", "basefont", "bgsound", "noscript",
  "link", "meta", "title", "style", "script",
]

class Text:
  def __init__(self, text, parent):
    self.text = text
    self.children = []
    self.parent = parent

  def __repr__(self):
    return repr(self.text)

class Element:
  def __init__(self, tag, attributes, parent):
    self.tag = tag
    self.attributes = attributes
    self.parent = parent
    self.children = []

  def __repr__(self):
    return f"<{self.tag}>"

class HTMLParser:
  def __init__(self, body):
    self.body = body
    self.unfinished = []

  def implicit_tags(self, tag):
    while True:
      open_tags = [node.tag for node in self.unfinished]
      if open_tags == [] and tag != "html":
        self.add_element("html")
      elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
        if tag in HEAD_TAGS:
          self.add_element("head")
        else:
          self.add_element("body")
      elif open_tags == ["html", "head"] and tag not in ["/head"] + HEAD_TAGS:
        self.add_element("/head")
      else: break

  def finish(self):
    while len(self.unfinished) > 1:
      node = self.unfinished.pop()
      parent = self.unfinished[-1]
      parent.children.append(node)
    return self.unfinished.pop()

  def add_text(self, text):
    if text.isspace(): return
    self.implicit_tags(None)
    parent = self.unfinished[-1]
    node = Text(text, parent)
    parent.children.append(node)

  def add_element(self, element):
    if not element: return
    tag, attributes = self.get_attributes(element)
    if tag.startswith("!"): return
    self.implicit_tags(tag)
    if tag.startswith("/"):
      if len(self.unfinished) == 1: return
      node = self.unfinished.pop()
      parent = self.unfinished[-1]
      parent.children.append(node)
    elif tag in SELF_CLOSING_TAGS:
      parent = self.unfinished[-1]
      node = Element(tag, attributes, parent)
      parent.children.append(node)
    else:
      parent = self.unfinished[-1] if self.unfinished else None
      node = Element(tag, attributes, parent)
      self.unfinished.append(node)

  def get_attributes(self, element):
    parts = element.split()
    tag = parts[0].lower()
    attributes = {}
    for attrpair in parts[1:]:
      if "=" in attrpair:
        key, value = attrpair.split("=", 1)
        if len(value) > 2 and value[0] in ["'", "\""]:
          value = value[1:-1]
        attributes[key.lower()] = value
      else:
        attributes[attrpair.lower()] = ""
    return tag, attributes

  def parse(self, viewsource=False):
    html = self.body
    html = transform(html) if viewsource else html
    intag = False
    inentity = False
    entity = ""
    text = ""
    for c in html:
      if c == "<":
        intag = True
        if text: self.add_text(text)
        text = ""
      elif c == ">":
        intag = False
        self.add_element(text)
        text = ""
      elif c == "&":
        entity = ""
        inentity = True
      elif inentity:
        if c == ";":
          text += ENTITY_TABLE.get(entity) or entity
          inentity = False
        else:
          entity += c
      else:
        text += c
    if not intag and text:
      self.add_text(text)
    return self.finish()


def transform(html):
  return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def print_tree(node, indent=0):
  print(" " * indent, node)
  for child in node.children:
    print_tree(child, indent + 2)


if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: python3 parse.py <htmlfile>"
  htmlfile = sys.argv[1]
  with open(htmlfile, 'r') as f:
    html = f.read()
    tree = HTMLParser(html).parse()
    print_tree(tree)
  f.close()