#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

# Required:
#  $ pip install pillow qrcode requests
#  $ pip install inky

import csv
import qrcode
import requests
import urllib.parse

# 実機上でないとinkyの依存パッケージのRPi.GPIOがインストールできないので、開発中はinkyを使用する部分はスキップする
ON_RASPPI = False

if ON_RASPPI:
    from inky import InkyPHAT


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


def generate_qrcode(contents):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=2,
        border=8
    )

    qr.add_data(contents)
    qr.make()
    img = qr.make_image(fill_color="#000000", back_color="#ffffff")
    print(img.size)
    img.save('qrcode.png')

    return img


def init_inky():
    if ON_RASPPI:
        inkyphat = InkyPHAT('black')


def is_url(target_string):
    url_parts = urllib.parse.urlparse(target_string)
    # print(
    #     url_parts.scheme, url_parts.hostname, url_parts.path,  # required
    #     url_parts.query, url_parts.fragment  # optional
    # )
    if len(url_parts.scheme) > 0 and len(url_parts.hostname) > 0:
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
    init_inky()
    items = load_tsv()
    # print(items)
    results = []
    for item in items:
        if None != item:
            if 'url' in item:  # and 'content' in item:
                if 2 >= len(item) and len(item) >= 1:
                    if is_url(item['url']):
                        result = check(item)
                        # print(item['url'], result)
                        results.append({'url': item['url'], 'result': result})
    show_results(results)


def show_results(items):
    for item in items:
        print(item['url'], item['result'])

    message = '成功: {}件\n{}\n失敗: {}件\n{}'.format(
        len([i for i in items if i['result'] == True]),
        '\t' + '\n\t'.join([i['url'] for i in items if i['result'] == True]),
        len([i for i in items if i['result'] == False]),
        '\t' + '\n\t'.join([i['url']
                            for i in items if i['result'] == False]),
    )

    qrimg = generate_qrcode(message)
    if ON_RASPPI:
        pass  # 表示処理


if __name__ == "__main__":
    main()
