#!/usr/bin/env python

from __future__ import absolute_import
from xml import etree
import sys

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
            pass
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
                pass
        if not e.tail or not e.tail.strip():
            e.tail = i
            pass
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            pass
        pass

if len(sys.argv) > 1:
    src = sys.argv[1]
    pass
else:
    src = sys.stdin
    pass

tree = etree.parse(src)
indent(tree.getroot())
tree.write(sys.stdout, "utf-8")
