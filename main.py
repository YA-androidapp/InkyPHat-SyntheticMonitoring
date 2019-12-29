#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

import csv
import requests
import urllib.parse


def check(item):
    # print(item)
    # print(item['url'])
    r = requests.get(item['url'], allow_redirects=False)
    if requests.codes.ok == r.status_code:
        # print(r.text)
        if r.text.find(item['content']) > -1:
            return True
        else:
            return False
    else:
        return False


def is_url(target_string):
    url_parts = urllib.parse.urlparse(target_string)
    # print(
    #     url_parts.scheme, url_parts.hostname, url_parts.path,  # required
    #     url_parts.query, url_parts.fragment  # optional
    # )
    if len(url_parts.scheme) > 0 and len(url_parts.hostname) > 0 and len(url_parts.path) > 0:
        return True
    else:
        return False


def load_tsv():
    with open('data.tsv', encoding='utf_8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        items = [row for row in reader]
        # for item in items:
        #     print(item)
        return items


def main():
    items = load_tsv()
    # print(items)
    for item in items:
        if None != item:
            if 'url' in item:  # and 'content' in item:
                if 2 >= len(item) and len(item) >= 1:
                    if is_url(item['url']):
                        result = check(item)
                        print(item['url'], result)


if __name__ == "__main__":
    main()
