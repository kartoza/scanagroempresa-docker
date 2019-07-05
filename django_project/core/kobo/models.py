from django.db import models


class KoboForm(models.Model):
    form_id = models.CharField(max_length=200)
    form_title = models.CharField(
        max_length=200,
        blank=True,
        null=True)
    style_attributes = models.TextField(
        null=True)

    def __str__(self):
        return '{0.form_id}: {0.form_title}'.format(
            self)
