# Python Web Browser

This is a simple web browser written in Python that follows the [Web Browser Engineering](https://browser.engineering/) ebook.

## Instructions

Run `python3 src/browser.py <url>` from the command line, where `<url>` is a complete `<scheme>://<host>/<path>` URL, i.e. `https://example.org/index.html`. Currently, browser.py will request the specified URL and open a window which will display the contents of the webpage. Also, try using the data URI scheme with a local HTML file as the `<url>`, i.e. `` "data:text/html,`cat tests/test.html`" ``

## Features

The browser supports the following features:

- HTTP and HTTPS protocols
- Data URI scheme (i.e. `data:text/html,<body><h1>Hello</h1></body>`)
- Transfer-Encoding: chunked
- Content-Encoding: gzip
- Cache-Control: max-age=`<seconds>`
- Content-Type: text/\*
- Scrolling, using the mouse wheel, or the up/down keys
- Zooming in/out, using Ctrl+plus/minus
- Window resizing
- `<b>`, `<i>`, `<big>`, `<small>`, `<p>`, and `<br>` tags

## Bug Report

| Date Reported | Date Fixed | Summary | Steps to Reproduce |
| ------------- | ---------- | ------- | ------------------ |
