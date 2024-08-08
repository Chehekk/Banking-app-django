from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, UserAddressForm, UserBankAccountForm

User = get_user_model()

class UserRegistrationView(TemplateView):
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('transactions:transaction_report'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)
        bank_account_form = UserBankAccountForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid() and bank_account_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            bank_account = bank_account_form.save(commit=False)
            bank_account.user = user
            bank_account.save()

            login(self.request, user)
            messages.success(self.request, 'Thank you for creating a bank account!')
            return redirect(reverse_lazy('transactions:deposit_money'))

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form,
                bank_account_form=bank_account_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()
        if 'bank_account_form' not in kwargs:
            kwargs['bank_account_form'] = UserBankAccountForm()

        return super().get_context_data(**kwargs)
