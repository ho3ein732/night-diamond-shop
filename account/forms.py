from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import NightDimondUser


class UserCreatedForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = NightDimondUser
        fields = ['phone']

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password2 != password1:
            raise forms.ValidationError('پسورد ها مانند هم نیستد!')
        return password2

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError("شماره تلفن حتما باید از عداد باشد!")

        if not phone.startswith('09'):
            raise forms.ValidationError('شماره تلفن باید به 09 شروع شود!')

        if len(phone) != 11:
            raise forms.ValidationError('شماره تلفن کمتر از 11 رقم است!')

        if NightDimondUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError('این شماره تلفن وجود دارد!')
        return phone


class VerifyCodeForm(forms.Form):
    token = forms.CharField(max_length=6,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد تایید'}))


class NightDimondUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = NightDimondUser
        fields = ('phone', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError('form must be a number!')

        if not phone.startswith('09'):
            raise forms.ValidationError('form must start with 09')

        if len(phone) != 11:
            raise forms.ValidationError('form must have 11 numbers')

        if self.instance.pk:
            if NightDimondUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('phone already exists!')
        else:
            if NightDimondUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('phone already exists!')

        return phone


class NightDimondUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = NightDimondUser
        fields = ('phone', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError('form must be a number!')

        if not phone.startswith('09'):
            raise forms.ValidationError('form must start with 09')

        if len(phone) != 11:
            raise forms.ValidationError('form must have 11 numbers')

        if self.instance.pk:
            if NightDimondUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('phone already exists!')
        else:
            if NightDimondUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('phone already exists!')
        return phone


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))


class NewPhoneForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = NightDimondUser
        fields = ['phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not phone.isdigit():
            raise forms.ValidationError('شماره تلفن باید فقط شامل اعداد باشد!')

        if not phone.startswith('09'):
            raise forms.ValidationError('شماره تلفن باید با 09 شروع شود!')

        if len(phone) != 11:
            raise forms.ValidationError('شماره تلفن باید 11 رقم داشته باشد!')

        if self.instance.pk:
            if NightDimondUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('این شماره تلفن قبلاً ثبت شده است!')
        else:
            if NightDimondUser.objects.filter(phone=phone).exists():
                raise forms.ValidationError('این شماره تلفن قبلاً ثبت شده است!')
        return phone




