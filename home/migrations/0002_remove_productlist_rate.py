# Generated by Django 3.1.1 on 2021-06-27 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productlist',
            name='rate',
        ),
    ]
