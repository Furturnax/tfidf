from django.db import models

from loader.consts import MAX_LENGHT_WORDS


class Word(models.Model):
    """Модель для хранения слов, их количества и частоты вхождения в файле."""

    word = models.CharField(
        'Слово',
        max_length=MAX_LENGHT_WORDS,
    )
    tf = models.IntegerField(
        'Количество вхождений',
    )
    idf = models.FloatField(
        'Частота вхождений в тексты',
    )

    class Meta:
        verbose_name = 'слово'
        verbose_name_plural = 'Слова'
        ordering = ('-idf',)

    def __str__(self):
        return f'{self.word} - {self.tf} - {self.idf}'
