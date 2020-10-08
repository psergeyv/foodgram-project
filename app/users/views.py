from django.core.mail import send_mail
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreationForm, UpdateProfile

class SignUp(CreateView):
    form_class = CreationForm
    success_url = '/auth/login/'
    template_name = 'signup.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        #self.send_mail_ls(email)
        return super().form_valid(form)
    '''
    def send_mail_ls(self, email):
        send_mail(
            'Регистрация',
            'Регистрация прошла успешно!',
            'foodgram.ru <admin@foodgram.ru>',
            [email],
            fail_silently=False
        )
    '''

@login_required
def EditProfile(request):
    if request.method == "POST":
        usrform = UpdateProfile(request.POST or None, instance=request.user)
        if usrform.is_valid():
            user = usrform.save()
            return render(request, "users/profile_edit_done.html", {
                'form': usrform,                
            })
        else:
            return render(request, "users/profile_edit.html", {
                'form': usrform,
            })
    else:
        usrform = UpdateProfile(instance=request.user)
        return render(request, "users/profile_edit.html", {
            'form': usrform,
        })
