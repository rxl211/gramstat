#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

import sys, os, subprocess, functools

from reg import registration

def walktrees(trees, process):
    def walk(root):
        stack = list()
        stack.append(root)
        while stack:
            node = stack.pop()
            process(node)
            for child in node.children:
                stack.append(child)
    for tree in trees:
        walk(tree)

def save(path, table):
    fname = path + '.csv'
    s = '\n'.join( ', '.join(str(col) for col in row) for row in table )
    f = open(fname, 'w')
    f.write(s)
    f.write('\n'*2)
    f.close()
    return table

def symbol_counter(path, oldtable, trees, callback):
    symbols = dict()
    if oldtable is not None:
        symbols.update((name, count) for name, count in oldtable)
    walktrees(trees, functools.partial(callback, symbols))

    return save(path, tuple((name,count)
        for name, count in symbols.iteritems()))

@registration.register('table')
def symbol_count(path, oldtable, conf):
    def callback(symbols, node):
        symbols[node.label] = symbols.get(node.label, 0) + 1
    return symbol_counter(path, oldtable, conf['trees'], callback)

@registration.register('table')
def non_term_count(path, oldtable, conf):
    def callback(symbols, node):
        if node.children: symbols[node.label] = symbols.get(node.label, 0) + 1
    return symbol_counter(path, oldtable, conf['trees'], callback)

@registration.register('table')
def term_count(path, oldtable, conf):
    def callback(symbols, node):
        if not node.children: symbols[node.label] = symbols.get(node.label, 0) + 1
    return symbol_counter(path, oldtable, conf['trees'], callback)
