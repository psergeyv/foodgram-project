# Generated by Django 3.1.2 on 2020-10-17 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20201009_1120'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipes',
            options={'ordering': ('-pub_date', 'name'), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.RenameField(
            model_name='recipes',
            old_name='title',
            new_name='name',
        ),
    ]