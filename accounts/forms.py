from django import forms
from .models import User, UserBankAccount, UserAddress, BankAccountType

class UserRegistrationForm(forms.ModelForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all(),
        required=True,
        empty_label="Select Account Type"
    )

    class Meta:
        model = UserBankAccount
        fields = ['account_type', 'account_number', 'balance', 'gender', 'birth_date']

class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['address_line1', 'address_line2', 'city', 'state', 'postal_code']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
