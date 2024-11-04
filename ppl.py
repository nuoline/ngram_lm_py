#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import math
import nwordseg

g_lm_dict = {}
gDebug = False

kBackoff = [0, 0, math.log10(0.02), math.log10(0.5), math.log10(0.8), math.log10(0.8)]

def safe_div(a, b, s=1e-6) : return float(a)/max(float(b), s)

def load_lm_dict(ngram_file):
    global g_lm_dict
    for line in open(ngram_file, 'r'):
        cols = line.strip().split('\t')
        if(len(cols) != 2):continue
        ngram = cols[0]
        freq = int(cols[1])
        g_lm_dict[ngram] = freq
ef get_ngram_freq(ngram):
    global g_lm_dict
    freq = 0
    if ngram in g_lm_dict:
        freq = g_lm_dict[ngram]
    return freq

def get_ngram_lm(words, n=5) :
    sum = 0.0
    for i in range(len(words)) :
       ngram = [words[j] for j in range(max(0, i-n+1), i+1)]
       sum += get_lm_score(ngram)
    return sum
def get_lm_score(w) :
    num = len(w)
    res = 0.0

    if num > 1:
        c1 = get_ngram_freq("".join(w))
        if c1 > 0 :
            c2 = get_ngram_freq("".join(w[:-1]))
            res = math.log10(safe_div(c1, c2))
            if gDebug : print num, c1, c2, "".join(w), "".join(w[:-1]), res
        else :
            res = kBackoff[num] + get_lm_score(w[1:])
    else:
        c1 = max(get_ngram_freq(w[0]), 1)
        c2 = 2e10
        res = math.log10(safe_div(c1, c2))
        if gDebug : print num, c1, c2, w[0], res

    return res

def compute_lm_score(qfile):
    global g_ngram_dict
    for line in open(qfile, 'r'):
        query = line.strip()
        query = cols[0:2]
        if int(freq) <= 0 :
            continue
        terms = nwordseg.segment(query)
        ppl = get_ngram_lm(terms)
        print '\t'.join([query, str(ppl)])

if __name__ == "__main__" :
    qfile = sys.argv[1]
    nwordseg.init("./nseg_model/nseg.model")
    load_lm_dict("./qngram.dict")

    compute_lm_score(qfile)
    lm_ngram()
    mapper()

    nwordseg.destroy()
