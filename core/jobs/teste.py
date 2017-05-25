# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd().replace("/core",""))
from nltk.tokenize import sent_tokenize, word_tokenize
def sentences(text):
    return sent_tokenize(text)
def tokenizer(text):
    return word_tokenize(text)
def concordance(word, sentences, context=100):
    out=[]
    for sent in sentences:
        if word in sent:
            context = len(sent)
            pos = sent.index(word)
            left = ''.join(sent[:pos])
            right = ''.join(sent[pos + len(word):])
            s = str('%*s %s %-*s' % (context, left[-context:], str(word).strip(), context, right[:context])).strip()
            out.append(s)
    return out
text = '''
A Secretaria de Estado de Saúde do Pará (Sespa) coletou nesta terça-feira (16) amostras de sangue de uma criança de dois anos que teria morrido vítima da febre maculosa. O material será analisado pelo Instituto Evandro Chagas, em Belém. De acordo com a Sespa, a doença não tem registro no Pará há 17 anos. A paciente, que era de Parauapebas, no sudeste do estado, apresentou sintomas de febre e inflamação na garganta após ser picada por um carrapato. O exame no Instituto Evandro Chagas vai identificar se essa foi a causa da morte. Uma equipe da Vigilância em Saúde da Sespa esteve em Parauapebas para acompanhar o caso.
'''
s=sentences(text)
outs = concordance('febre',s)
for o in outs:
    print(o)
