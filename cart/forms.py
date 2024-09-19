from django import forms
from .models import Province, City, Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'province', 'city', 'detailed_address', 'postal_code',
                  'plaque', 'recipient_phone']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['province'].queryset = Province.objects.all()
        self.fields['city'].queryset = City.objects.none()

        if 'province' in self.data:
            try:
                province_id = int(self.data.get('province'))
                self.fields['city'].queryset = City.objects.filter(province_id=province_id).order_by('name')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.province.city_set.order_by('name')

        if user:
            self.fields['recipient_phone'].initial = user.phone

        self.fields['province'].required = True
        self.fields['city'].required = True
        self.fields['detailed_address'].required = True
        self.fields['postal_code'].required = True
        self.fields['plaque'].required = True
