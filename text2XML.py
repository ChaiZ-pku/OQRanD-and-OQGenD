#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ChaiZi (chaizi [at] pku.edu.cn)'

import xml.dom.minidom


def read_text(file_name):
    texts = []
    with open(file_name) as f_in:
        for line in f_in:
            line = line.strip().split()
            texts.append(line)
    return texts


def form_data(source_text, target_text):
    corpus = {}
    for (x, y) in zip(source_text, target_text):
        news = ''.join(x)
        questions = ''.join(y).split('#?#')[:-1]
        if news not in corpus:
            corpus[news] = questions
        else:
            print('alert! duplicated news')
            corpus[news] += questions
    return corpus


def create_XML(corpus):
    doc = xml.dom.minidom.Document()
    root = doc.createElement('Data')
    doc.appendChild(root)
    for id, news in enumerate(corpus):
        node_ID = doc.createElement('NQ-pair')
        node_ID.setAttribute('ID', '{}'.format(str(id)))
        root.appendChild(node_ID)

        node_news = doc.createElement("news")
        node_news.appendChild(doc.createTextNode(news))
        node_ID.appendChild(node_news)

        questions = corpus[news]
        for question in questions:
            node_question = doc.createElement("question")
            node_question.appendChild(doc.createTextNode(question))
            node_ID.appendChild(node_question)
    return doc


if __name__ == "__main__":
    source_text = read_text("./texts/source.txt")
    target_text = read_text("./texts/target.txt")
    print('{} source, {} target'.format(len(source_text), len(target_text)))

    XML_obj = create_XML(form_data(source_text, target_text))
    with open('OQGenD.xml', 'w') as f_out:
        XML_obj.writexml(
            f_out, indent='\t', addindent='\t', newl='\n', encoding="utf-8"
        )