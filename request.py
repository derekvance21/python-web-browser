import urlparser
import socket
import cache

default_redirects = 4

# where header is a dictionary of HTTP field name: value pairs
def httpheader(header: dict) -> str:
  return "\r\n".join(map(lambda x: f"{x[0]}: {x[1]}", header.items())) + "\r\n"

def request(url: str, redirects: int = default_redirects):
  assert redirects >= 0, f"Error: request exceeded {default_redirects} redirects"

  scheme, host, port, path = urlparser.parse(url)

  response = cache.fetch(url)
  if not response:
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

    header = httpheader({
      "Host": host,
      "Connection": "close",
      "User-Agent": "Juzang",
      "Accept-Encoding": "gzip",
      "Accept": "text/*"
    })

    s.send(f"GET {path} HTTP/1.1\r\n{header}\r\n".encode())
    response = s.makefile("rb", newline="\r\n")
    s.close()

  statusline = response.readline().decode()
  version, status, explanation = statusline.split(" ", 2)

  header = {}
  while True:
    line = response.readline().decode()
    if line == "\r\n": break
    field, value = line.split(":", 1)
    header[field.lower()] = value.strip()
  cacheheader = header.copy()

  body = response.read()
  response.close()

  contentlength = header.get("content-length")
  contentlength = int(contentlength) if contentlength else contentlength
  assert not contentlength or len(body) == contentlength, f"Error: length of body: {len(body)} != content-length: {contentlength}"

  transferencoding = header.get("transfer-encoding")
  if transferencoding == "chunked":
    newbody, body = bytearray(), bytearray(body)
    while body:
      chunkstart = body.find(b"\r\n")
      chunksize = int(body[:chunkstart], 16)
      body = body[chunkstart+2:]
      newbody += body[:chunksize]
      body = body[chunksize+2:]
    body = newbody
    cacheheader.pop("transfer-encoding")
  else:
    assert not transferencoding, f"Error: Transfer-Encoding: {transferencoding} is unsupported"

  contentencoding = header.get("content-encoding")
  if contentencoding == "gzip":
    import gzip
    body = gzip.decompress(body)
    cacheheader.pop("content-encoding")
  else:
    assert not contentencoding, f"Error: Content-Encoding: {contentencoding} is unsupported"

  cachecontrol = header.get("cache-control")
  if cachecontrol:
    directives = [directive.strip() for directive in cachecontrol.split(",")]
    for directive in directives:
      if directive.startswith("max-age="):
        seconds = int(directive.split("=")[1].strip())
        if seconds > 0:
          cacheheader.pop("cache-control")
          cacheheader["content-length"] = len(body)
          cachedresponse = f"{statusline}{httpheader(cacheheader)}\r\n".encode() + body
          cache.cache(url, cachedresponse, seconds)

  contenttype = header.get("content-type")
  if isinstance(contenttype, str):
    if contenttype.startswith("text"):
      body = body.decode(encoding="utf8", errors="replace")
    else:
      assert False, f"Error: Content-Type: {contenttype} is unsupported"


  if status.startswith("3"): # redirect
    redirect = header.get("location")
    if not redirect.find("://"): # redirect location doesn't include scheme, so use whatever prior scheme was
      if not redirect.find("."): # redirect location doesn't include host, so use whatever prior host was
        if not redirect.startswith("/"): # redirect location is a relative uri, so append to whatever prior path was
          redirect = f"{path}{redirect}"
        redirect = f"{host}{redirect}"
      redirect = f"{scheme}://{redirect}"
    return request(redirect, redirects=redirects-1)

  return body



if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: request.py <url>"
  url = sys.argv[1]
  body = request(url)
  print(f"body:\n{body}")