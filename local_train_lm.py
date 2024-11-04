#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys
import math
import nwordseg

g_ngram_dict = {}

def seg_ngram(query) :
    term_list = []
    ngram_list = []

    term_list = nwordseg.segment(query)
    sg_str = ''
    seg_len = len(term_list)
    for i in range(seg_len) :
        #unigram
        word = term_list[i]
        ngram_list.append(word)
        #bigram
        if i + 1 < seg_len :
            bigram = ''.join([word, term_list[i + 1]])
            ngram_list.append(bigram)
        ##trigram
        if i + 2 < seg_len :
            trigram = ''.join([word, term_list[i + 1], term_list[i + 2]])
            ngram_list.append(trigram)
    return ngram_list

def mapper() :
    global g_ngram_dict
    for line in sys.stdin :
        cols = line.strip().split('\t')
        if len(cols) < 2 :
            continue
        query = cols[0]
        query_ngram_list = seg_ngram(query)
        for qngram in query_ngram_list :
            if qngram not in g_ngram_dict:
                g_ngram_dict[qngram] = 1
            else:
                g_ngram_dict[qngram] += 1
        if query not in g_ngram_dict:
            g_ngram_dict[query] = 1

def lm_ngram():
    global g_ngram_dict
    for ngram in g_ngram_dict:
        freq = g_ngram_dict[ngram]
        print('\t'.join([ngram, str(freq)]))

if __name__ == "__main__" :
    nwordseg.init("./nseg_model/nseg.model")
    mapper()
    lm_ngram()
    nwordseg.destroy()
