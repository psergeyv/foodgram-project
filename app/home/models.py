from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class Setting(models.Model):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, primary_key=True, verbose_name="Сайт")
    name = models.CharField(max_length=200, blank=True,
                            null=True, verbose_name="Название сайта", default="")
    email = models.CharField(max_length=200, blank=True,
                             null=True, verbose_name="емайл", default="")
    phone = models.CharField(max_length=300, blank=True, null=True,
                             verbose_name="Телефоны через запятую", default="")
    social_vk = models.CharField(max_length=300, blank=True, null=True,
                             verbose_name="Страничка вКонтакте", default="")                         
    social_ig = models.CharField(max_length=300, blank=True, null=True,
                             verbose_name="Страничка в Instagram", default="")                                                  

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'


class Seo(models.Model):
    slug = models.SlugField(max_length=100, unique=True, default=None,
                            verbose_name="Адрес страницы, для главной (index)")
    title = models.CharField(max_length=200, blank=True,
                             null=True, verbose_name="title", default="")
    keywords = models.CharField(
        max_length=400, blank=True, null=True, verbose_name="ключевые слова", default="")
    description = models.CharField(
        max_length=400, blank=True, null=True, verbose_name="Описание", default="")

    class Meta:
        verbose_name = 'СЕО'
        verbose_name_plural = 'СЕО'


class Textblock(models.Model):
    name = models.CharField(max_length=200, default="", verbose_name="Название блока")
    thumbnail = models.ImageField(
        upload_to='sblock/', height_field=None, width_field=None,blank=True, max_length=200, verbose_name="Изображение")
    pageblock = models.CharField(max_length=200, default="", verbose_name="Символьный код страницы/раздела")
    codeblock = models.CharField(max_length=100, default="", verbose_name="Код блока")
    description = RichTextUploadingField(blank=True,verbose_name="Содержимое блока")
    
    class Meta:
        verbose_name = 'Текстовый блок сайта'
        verbose_name_plural = 'Текстовые блоки сайта'
    
    def save(self, *args, **kwargs):
        if self.thumbnail:
            '''
            img = Image.open(self.thumbnail)
            img_height = 490
            img_width = 497
            if img.height > img_height or img.width > img_width:
                img = img.resize((img_width, img_height), Image.ANTIALIAS)
                img = img.convert('RGB')

                output = BytesIO()
                img.save(output, format='JPEG', quality=72)
                output.seek(0)
                self.thumbnail = InMemoryUploadedFile(output, 'ImageField',
                                                          f'{self.thumbnail.name.split(".")[0]}.jpg',
                                                          'image/jpeg', sys.getsizeof(
                                                              output),
                                                          None)
            '''                                              
            try:
                this = Textblock.objects.get(id=self.id)
                if this.thumbnail != self.thumbnail:
                    this.thumbnail.delete(save=False)
            except:
                pass
            super().save(*args, **kwargs)
        else:
            super(Textblock, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.thumbnail.storage, self.thumbnail.path
        super(Textblock, self).delete(*args, **kwargs)
        storage.delete(path)