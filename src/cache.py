import uuid
import csv
import datetime
import os

cachedir = "../cache/"
fieldnames = ("url", "filename", "expiration")
cachepath = f"{cachedir}cache.csv"

def getcache() -> list:
  if os.path.isfile(cachepath):
    with open(cachepath, newline="") as f:
      reader = csv.DictReader(f)
      return [row for row in reader]
  else:
    return writecache([])
    

def writecache(cache: list) -> list:
  with open(cachepath, "w") as f:
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    writer.writerows(cache)
  return cache


def getentry(url: str, cache: list = None) -> dict:
  cache = cache or getcache()
  match = next(filter(lambda row: row.get("url") == url, cache), None)
  return match


def fetch(url: str):
  cache = getcache()
  match = getentry(url, cache)
  if match:
    expiration = datetime.datetime.fromisoformat(match.get("expiration"))
    filename = match.get("filename")
    responsepath = f"{cachedir}{filename}"
    if datetime.datetime.now(tz=datetime.timezone.utc) < expiration:
      f = open(responsepath, "rb")
      return f
    else:
      # cache entry was outdated, so remove it and update cache csv
      import os
      if os.path.exists(responsepath):
        os.remove(responsepath)
      cache.remove(match)
      writecache(cache)
  return None
    

def cache(url: str, response: bytes, seconds: int) -> None:
  cache = getcache()
  match = getentry(url, cache)
  filename = match.get("filename") if match else uuid.uuid4()
  with open(f"{cachedir}{filename}", "wb") as f:
    f.write(response)
  expiration = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
  cache.append({"url": url, "filename": filename, "expiration": expiration})
  if not match:
    writecache(cache)


if __name__ == "__main__":
  import sys
  assert len(sys.argv) == 2, f"Usage: python3 cache.py <url>"
  url = sys.argv[1]
  entry = getentry(url)
  print(entry)