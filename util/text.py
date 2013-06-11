# -*- coding: utf-8 -*-
import re

MAPPING = [
    (u'‘', "'"),
    (u'’', "'"),
    (u'“', '"'),
    (u'”', '"'),
    (u'…', '.'),
    (u'–', '-'),
    ('\.\.\.', '.')
]

def fix_text(text):
    for k,v in MAPPING:
        text = re.sub(k, v, text)
    return text
