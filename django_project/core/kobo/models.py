from django.db import models

class KoboForm(models.Model):
    form_id = models.CharField(max_length=200)

    def __str__(self):
        return self.form_id
