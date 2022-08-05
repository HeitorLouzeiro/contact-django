from django.db import models


# Create your models here.
class Contacts(models.Model):
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    telephone = models.IntegerField()
    birthday = models.DateField()
    favorite = models.BooleanField(default=False)
    note = models.TextField(null=False, blank=True)
    create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name+" "+self.last_name

    class Meta:
        verbose_name_plural = 'Contacts'
        verbose_name = 'Contact'
