# Generated by Django 3.1.2 on 2020-10-07 21:49

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default=None, max_length=100, unique=True, verbose_name='Адрес страницы, для главной (index)')),
                ('title', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='title')),
                ('keywords', models.CharField(blank=True, default='', max_length=400, null=True, verbose_name='ключевые слова')),
                ('description', models.CharField(blank=True, default='', max_length=400, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'СЕО',
                'verbose_name_plural': 'СЕО',
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sites.site', verbose_name='Сайт')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Название сайта')),
                ('email', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='емайл')),
                ('phone', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Телефоны через запятую')),
                ('social_vk', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Страничка вКонтакте')),
                ('social_ig', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Страничка в Instagram')),
            ],
            options={
                'verbose_name': 'Настройки сайта',
                'verbose_name_plural': 'Настройки сайта',
            },
        ),
        migrations.CreateModel(
            name='Textblock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200, verbose_name='Название блока')),
                ('thumbnail', models.ImageField(blank=True, max_length=200, upload_to='sblock/', verbose_name='Изображение')),
                ('pageblock', models.CharField(default='', max_length=200, verbose_name='Символьный код страницы/раздела')),
                ('codeblock', models.CharField(default='', max_length=100, verbose_name='Код блока')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='Содержимое блока')),
            ],
            options={
                'verbose_name': 'Текстовый блок сайта',
                'verbose_name_plural': 'Текстовые блоки сайта',
            },
        ),
    ]