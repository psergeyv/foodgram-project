# Generated by Django 3.1.2 on 2020-10-07 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201007_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='Номер телефона'),
        ),
    ]
