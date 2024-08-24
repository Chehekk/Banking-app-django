from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, AddressForm, UserForm

class UserRegistrationView(View):
    def get(self, request):
        registration_form = UserRegistrationForm()
        address_form = AddressForm()
        user_form = UserForm()
        return render(request, 'accounts/register.html', {
            'registration_form': registration_form,
            'address_form': address_form,
            'user_form': user_form
        })

    def post(self, request):
        registration_form = UserRegistrationForm(request.POST)
        address_form = AddressForm(request.POST)
        user_form = UserForm(request.POST)

        if registration_form.is_valid() and address_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            bank_account = registration_form.save(commit=False)
            bank_account.user = user
            bank_account.save()

            address = address_form.save(commit=False)
            address.user = user
            address.save()

            return redirect('home')

        return render(request, 'accounts/register.html', {
            'registration_form': registration_form,
            'address_form': address_form,
            'user_form': user_form
        })
