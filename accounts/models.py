from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .constants import GENDER_CHOICE
from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return 0

class BankAccountType(models.Model):
    name = models.CharField(max_length=128)
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='Interest rate from 0 - 100'
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text='The number of times interest will be calculated per year'
    )

    def __str__(self):
        return self.name

    def calculate_interest(self, principal):
        p = principal
        r = self.annual_interest_rate
        n = Decimal(self.interest_calculation_per_year)
        interest = (p * (1 + ((r/100) / n))) - p
        return round(interest, 2)

class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_type = models.ForeignKey(
        BankAccountType,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    interest_start_date = models.DateField(
        null=True, blank=True,
        help_text='The month number that interest calculation will start from'
    )
    initial_deposit_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.account_number)

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255, default='Unknown Address', blank=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.email

from django import forms
from .models import UserBankAccount, BankAccountType

class UserRegistrationForm(forms.ModelForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all(),
        required=True,
        empty_label="Select Account Type"
    )

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password' : forms.PasswordInput()
        }

from accounts.models import BankAccountType
BankAccountType.objects.all()

BankAccountType.objects.create(name='Fixed Deposit', maximum_withdrawal_amount=10000, annual_interest_rate=5, interest_calculation_per_year=1)
BankAccountType.objects.create(name='Savings Account', maximum_withdrawal_amount=5000, annual_interest_rate=3, interest_calculation_per_year=12)
BankAccountType.objects.create(name='Current Account', maximum_withdrawal_amount=2000, annual_interest_rate=1, interest_calculation_per_year=4)


