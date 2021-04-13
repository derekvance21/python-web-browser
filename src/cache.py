import uuid
import csv
import datetime

cachepath = "../cache/"
fieldnames = ("url", "filename", "expiration")

def getcache() -> list:
  with open(f"{cachepath}cache.csv", newline="") as f:
    return [row for row in csv.DictReader(f)]


def writecache(cache: list) -> None:
  with open(f"{cachepath}cache.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()
    writer.writerows(cache)


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
    responsepath = f"{cachepath}{filename}"
    if datetime.datetime.now(tz=datetime.timezone.utc) < expiration:
      f = open(responsepath, "rb")
      return f
    else:
      # cache entry was outdated, so remove it and update cache csv
      import os
      if os.path.exists(responsepath):
        os.remove(responsepath)
      cache.pop(match)
      writecache(cache)
  return None
    

def cache(url: str, response: bytes, seconds: int) -> None:
  cache = getcache()
  match = getentry(url, cache)
  filename = match.get("filename") if match else uuid.uuid4()
  with open(f"{cachepath}{filename}", "wb") as f:
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