# Generated by Django 4.1 on 2022-08-05 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('dd', models.IntegerField()),
                ('telephone', models.IntegerField()),
                ('birthday', models.DateField(blank=True)),
                ('favorite', models.BooleanField(default=False)),
                ('note', models.TextField(blank=True)),
                ('create', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
