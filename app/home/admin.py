from django.contrib import admin
from django.db.utils import ProgrammingError
from django.conf import settings

from .models import Seo, Setting, Textblock
from users.models import Profile
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django import forms


class ProfileUserAdmin(admin.ModelAdmin):
    model = Profile
    search_fields = ("username",)


admin.site.register(Profile, ProfileUserAdmin)


class SeoAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = ("slug", "title",)
    search_fields = ("slug",)
    list_filter = ("slug",)


admin.site.register(Seo, SeoAdmin)


class SettingAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'

    def has_add_permission(self, request, obj=None):
        return False if self.model.objects.filter(site=settings.SITE_ID).count() > 0 else super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


admin.site.register(Setting, SettingAdmin)


class TextBlockAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    list_display = ("name", "pageblock", "codeblock")
    search_fields = ("name", "codeblock")
    list_filter = ("pageblock",)


admin.site.register(Textblock, TextBlockAdmin)


class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'


class PageAdmin(FlatPageAdmin):
    """
    Page Admin
    """
    form = FlatPageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, PageAdmin)
