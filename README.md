# Python Web Browser

This is a simple web browser written in Python that follows the [Web Browser Engineering](https://browser.engineering/) ebook.

## Instructions

Run `python3 src/browser.py <url>` from the command line, where `<url>` is a complete `<scheme>://<host>/<path>` URL, i.e. `https://example.org/index.html`. Currently, browser.py will request the specified URL and open a window which will display the contents of the webpage.

## Features

The browser supports the following features:

- HTTP and HTTPS protocols
- Transfer-Encoding: chunked
- Content-Encoding: gzip
- Cache-Control: max-age=`<seconds>`
- Content-Type: text/\*
- Zooming in/out, using Ctrl+plus/minus
- Scrolling, using the mouse wheel, or the up/down keys
- Window resizing

## Bug Report

| Date Reported | Date Fixed | Summary | Steps to Reproduce |
| ------------- | ---------- | ------- | ------------------ |
