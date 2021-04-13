# Python Web Browser

This is a simple web browser written in Python that follows the [Web Browser Engineering](https://browser.engineering/) ebook.

## Instructions

Run `python3 src/browser.py <url>` from the command line, where `<url>` is a complete `<scheme>://<host>/<path>` URL, i.e. `https://example.org/index.html`. Currently, browser.py will request the specified URL and print the contents of the response HTML that is within the body tag.

## Features

The browser supports the following features:
- HTTP and HTTPS protocols
- Transfer-Encoding: chunked
- Content-Encoding: gzip
- Cache-Control: max-age=`<seconds>`
- Content-Type: text/*

## Bug Report

| Date Reported | Date Fixed | Summary | Steps to Reproduce
| --- | --- | --- | --- |