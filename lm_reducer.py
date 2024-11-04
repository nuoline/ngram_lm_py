#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys

def emit(last_ngram, count_sum) :
    if last_ngram == '' : return
    if count_sum <= 3.0 : return
    print '\t'.join([last_ngram, str(round(count_sum, 2))])

def reduce() :
    last_ngram = ''
    count_sum = 0.0
    for line in sys.stdin :
        cols = line.strip().split('\t')
        if len(cols) < 2 :
            continue
        ngram, count = cols[0:2]
        if ngram == last_ngram :
            count_sum += float(count)
        else :
            emit(last_ngram, count_sum)
            count_sum = float(count)
            last_ngram = ngram
    emit(last_ngram, count_sum)

if __name__ == "__main__" :
    reduce()
