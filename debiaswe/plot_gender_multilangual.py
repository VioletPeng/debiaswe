#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs as cs
from numpy.random import normal
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{lmodern}']

def parse_results(infile):
    lang_gender_dict = dict()
    with cs.open(infile, encoding='utf-8') as inf:
        header = inf.readline()
        helems = header.split('\t')
        assert(len(helems) == 22), len(helems)
        inf.readline()
        for i, el in enumerate(helems):
            if el != '' and el != '\r\n':
                assert (el not in lang_gender_dict), (el, lang_gender_dict)
                lang_gender_dict[el] = [[],[]]
            else:
                helems[i] = helems[i-1]
        print(helems)
        count = 0
        for line in inf:
            elems = line.strip().split('\t')
            for i, el in enumerate(elems):
                if count < 20:
                    if i < 2:
                        lang_gender_dict[helems[i]][i].append(el)
                    elif len(lang_gender_dict[helems[i]][(i-2)%4/2]) == count:
                        lang_gender_dict[helems[i]][(i-2)%4/2].append(el)
                    else: 
                        assert (len(lang_gender_dict[helems[i]][(i-2)%4/2]) > count), (i, el, helems[i], len(lang_gender_dict[helems[i]][i%2]), count)
                        lang_gender_dict[helems[i]][(i-2)%4/2][count] += '('+el+')'
                else:
                    if i < 2:
                        lang_gender_dict[helems[i]][i][count%20] += ':'+el
                    else:
                        lang_gender_dict[helems[i]][(i-2)%4/2][count%20] += ':'+el
            count += 1
    return lang_gender_dict

def parse_data_point(values):
    assert len(values) == 2
    annotations, associations = [], []
    for elems in values:
        for el in elems:
            an, val = el[:-1].split(':')
            val = float(val)
            if abs(val) < 0.15:
                continue
            annotations.append(an)
            associations.append((val-0.1)*2 if val > 0 else (val+0.1)*2)
    return annotations, associations

def plot_gender_multilingual_emb(lang_gender_dict):
    fig, ax = plt.subplots()
    plt.ylim(-7,7)
    plt.xlim(-0.42,0.5)
    #ax.annotate("She", xy=(0.0, 0.0), xytext=(0.35, 0),
    #        arrowprops=dict(arrowstyle="->"))
    #ax.arrow(0, -7.8, 0.35, 0, head_width=0.05, head_length=0.1, fc='k', ec='k')
    #ax.arrow(0, -7.8, -0.3, 0, head_width=0.05, head_length=0.1, fc='k', ec='k')
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    count = 0
    for k, v in lang_gender_dict.items():
        gender_annotations, gender_values = parse_data_point(v)
        assert len(gender_annotations) == len(gender_values)
        mean = (count%2-0.5)*(count/2+1)*2
        print(mean)
        y = normal(loc=mean, scale=3, size=len(gender_annotations))
        count += 1
        ax.scatter(gender_values, y, c=colors[count], s=80)
        for i, ann in enumerate(gender_annotations):
            ax.annotate(ann, (gender_values[i],y[i]), fontsize=20)
    plt.show()
    fig.savefig("test.pdf", bbox_inches='tight')

if __name__ == '__main__':
    lang_gender_dict = parse_results(sys.argv[1])
    print (len(lang_gender_dict))
    plot_gender_multilingual_emb(lang_gender_dict)
