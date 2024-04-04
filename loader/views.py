import re
from collections import Counter
from math import log

from django.shortcuts import render

from .consts import LIMIT_WORDS
from .models import Word


def process_file(text):
    """Обработка документа с подсчетом TF и IDF."""
    words_table = []
    words = re.split(r'\W+', text)
    word_counter = Counter(words)
    for word, tf in word_counter.items():
        words_table.append(
            Word(
                word=word.capitalize(),
                tf=tf,
                idf=log(len(words) / (1 + word_counter[word]))
            )
        )
    return Word.objects.bulk_create(words_table)


def render_results(request):
    """Рендер страницы с результатами подсчета TF и IDF."""
    return render(
        request,
        'results.html',
        {'words': Word.objects.order_by('-idf')[:LIMIT_WORDS]}
    )


def file_upload(request):
    """Загрузка документа с последующим подсчетом TF и IDF."""
    Word.objects.all().delete()
    if not (request.method == 'POST' and request.FILES.get('file')):
        return render(request, 'upload.html')
    text = request.FILES['file'].read().decode('utf-8')
    process_file(text)
    return render_results(request)
