import os
import typing
from collections import Counter

import numpy as np
from flask import current_app


def calc_file_stats(file: str) -> typing.List:
    preproccessed_file_content = preprocess(file)
    words_stats = calc_words_stats(preproccessed_file_content, file)

    return words_stats


def preprocess(file: str) -> typing.List:
    with open(file, "r", encoding="utf-8", errors="ignore") as file:
        file = file.read()
        file = file.lower()
        file = clean_text(file)

        return file


def clean_text(file: str) -> typing.List:
    symbols = ["\n", "!", "\"", "#", "$", "%", "&", "(", ")", "*", "+", "-", ".", "/", ":", ";", " – ",
               "<", "=", ">", "?", "@", "[", "\\", "]", "^",  "_", "`", "{", "|", "}", "~", ",", "«", "»", "..."]

    file = str(np.char.replace(file, "-\n", ""))
    for symbol in symbols:
        file = str(np.char.replace(file, symbol, " "))
    file = [word for word in file.split(" ") if word]

    return file


def calc_words_stats(words: typing.List, file: str) -> typing.List:
    unique_words = set(words)
    cntr = Counter(words)
    file_len = len(words)

    idf_stats = calc_idf(words=unique_words,
                         filename=file)

    words_stats = []
    for word in unique_words:
        word_tf = round(cntr[word] / file_len, 6)
        words_stats.append(
            {
                "word": word,
                "tf": word_tf,
                "idf": idf_stats[word]["idf"],
            }
        )

    return sorted(words_stats, key=lambda x: x["idf"], reverse=True)


def calc_idf(words: typing.Set, filename: str) -> typing.Dict:
    docs = list(os.walk(current_app.config["UPLOAD_FOLDER"]))[0][-1]
    docs_count = len(docs)
    docs_corpus = get_docs_corpus(docs=docs, filename=filename)

    words_stats = {}
    for word in words:
        words_stats[word] = {"cnt": 1}
        for corpus in docs_corpus:
            if word in corpus:
                words_stats[word]["cnt"] += 1
        else:
            words_stats[word]["idf"] = np.log10(
                docs_count/words_stats[word]["cnt"]
            )
    else:
        return words_stats


def get_docs_corpus(docs: typing.List, filename: str) -> typing.List:
    docs_corpus = []
    for doc in docs:
        doc = os.path.join(current_app.config["UPLOAD_FOLDER"], doc)
        if doc != filename:
            docs_corpus.append(set(preprocess(doc)))

    return docs_corpus
