from django.shortcuts import render
from sklearn.feature_extraction.text import TfidfVectorizer

from .models import Word


def text_process(file):
    """Обработка текста."""
    text = file.read().decode('utf-8')

    vectorizer = TfidfVectorizer()
    words = vectorizer.get_feature_names()
    ftidf_matrix = vectorizer.fit_transform([text])
    tfidf_values = ftidf_matrix.toarray()[0]

    data = [
        (
            word, tfidf_values[i], vectorizer.idf_[i]
        ) for i, word in enumerate(words)
    ]

    return data


def file_upload(request):
    """Загрузка файла."""
    if request.method == 'POST' and request.FILES['file']:
        data = text_process(request.FILES['file'])

        for word, tf, idf in data:
            Word.objects.create(word=word, tf=tf, idf=idf)

        return render(
            request,
            'results.html',
            {'data': Word.objects.order_by('-idf')[:50]}
        )
    return render(request, 'upload.html')
