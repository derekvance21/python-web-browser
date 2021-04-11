import request
import display

def load(url):
  headers, body = request.request(url)
  display.display(body)

if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: browser.py <url>"
  load(sys.argv[1])