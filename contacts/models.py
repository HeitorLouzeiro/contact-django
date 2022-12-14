from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Contacts(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    telephone = models.CharField(max_length=25)
    favorite = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    create = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name+" "+self.last_name

    class Meta:
        verbose_name_plural = 'Contacts'
        verbose_name = 'Contact'


class ExcelFile(models.Model):
    file = models.FileField(upload_to="excel")

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
