# Generated by Django 4.1 on 2022-09-01 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0018_myorders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myorders',
            name='wishlist',
        ),
        migrations.AddField(
            model_name='myorders',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
