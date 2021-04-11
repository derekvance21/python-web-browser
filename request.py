import urlparser
import socket

def request(url):
  scheme, host, port, path = urlparser.parse(url)

  s = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM,
    proto=socket.IPPROTO_TCP,
  )

  if scheme == "https":
    import ssl
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(s, server_hostname=host)

  s.connect((host, port))

  s.send(f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n".encode())
        
  response = s.makefile("r", encoding="utf8", newline="\r\n")

  statusline = response.readline()
  version, status, explanation = statusline.split(" ", 2)
  assert status == "200", f"{status}: {explanation}"

  headers = {}
  while True:
    line = response.readline()
    if line == "\r\n": break
    header, value = line.split(":", 1)
    headers[header.lower()] = value.strip()

  body = response.read()
  s.close()
  return headers, body


if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: request.py <url>"
  url = sys.argv[1]
  headers, body = request(url)
  print(f"headers:\n{headers}\n")
  print(f"body:\n{body}")