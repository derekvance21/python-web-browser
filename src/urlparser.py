def parse(url):
  scheme, url = url.split("://", 1)
  assert scheme in ["http", "https"], f"Unknown scheme {scheme}"
  host, path = url.split("/", 1)
  path = "/" + path
  port = 80 if scheme == "http" else 443
  if ":" in host:
    host, port = host.split(":", 1)
    port = int(port)
  return scheme, host, port, path

if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, "Usage: python3 urlparser.py <url>"
  url = sys.argv[1]
  scheme, host, port, path = parse(url)
  print(f"scheme: {scheme}")
  print(f"host: {host}")
  print(f"port: {port}")
  print(f"path: {path}")
