import request
import display

def load(url : str) -> None:
  body = request.request(url)
  display.display(body, viewsource=url.startswith("view-source"))

if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: browser.py <url>"
  load(sys.argv[1])