# Generated by Django 3.1.2 on 2020-10-08 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20201008_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='image',
            field=models.ImageField(upload_to='irecipes/', verbose_name='Картинка'),
        ),
    ]
