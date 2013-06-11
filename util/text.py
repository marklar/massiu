# -*- coding: utf-8 -*-
import re

MAPPING = [
    (u'‘', "'"),
    (u'’', "'"),
    (u'“', '"'),
    (u'”', '"'),
    (u'…', '.'),
    ('\.\.\.', '.')
]

def fix_text(text):
    t = re.sub(u'‘', "'", text)
    t = re.sub(u'’', "'", t)
    t = re.sub(u'“', '"', t)
    t = re.sub(u'”', '"', t)
    t = re.sub(u'…', '.', t)
    t = re.sub('\.\.\.', '.', t)
    return t
