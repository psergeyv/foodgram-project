# Generated by Django 3.1.2 on 2020-10-08 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20201008_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='image',
            field=models.ImageField(upload_to='irecipes/%d_%m_%Y/', verbose_name='Картинка'),
        ),
    ]
