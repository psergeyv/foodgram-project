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
        return super().form_valid(form)
    

@login_required
def edit_profile(request):
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
