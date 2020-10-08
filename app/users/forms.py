from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',  'phone', 'vk')
    def save(self, commit=True):
        user = super(CreationForm, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user    


class UpdateProfile(forms.ModelForm):
    #username = forms.CharField(required=True,label="Логин")
    email = forms.EmailField(required=True,label="E-mail")
    phone = forms.CharField(required=False,label="Номер телефона")
    vk = forms.URLField(required=False,label="Старничка вКонтакте")
    first_name = forms.CharField(required=False,label="Имя")
    last_name = forms.CharField(required=False,label="Фамилия")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'vk')

    def clean_email(self):
        username = self.cleaned_data.get('email')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('Ошибка, уже занято.')
        return email