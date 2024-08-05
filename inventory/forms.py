from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem, Department

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), initial=0)
    
    class Meta:
        model = InventoryItem
        fields = [
            'no',     # Corresponds to 'no'
            'name',              # Corresponds to 'name'
            'specifications',  # Corresponds to 'specifications'
            'department',        # Newly added based on model
            'category', # Corresponds to 'location'
            'location',              # Corresponds to 'pic'
            'pic',           # Corresponds to 'condition'
            'condition',        # Corresponds to 'history'
            'history',
            'tipe_unit',            # Newly added based on model
            'digit_1',        # Newly added based on model
            'kode_asset',         # Newly added based on model
            'digit_23',     # Newly added based on model
            'kode_golongan',         # Newly added based on model
            'digit_45',   # Newly added based on model
            'kode_jenisunit',            # Newly added based on model
            'urutan',             # Newly added based on model
            'bulan',             # Newly added based on model
            'tahun',          # Newly added based on model
            'bpb_ppat',                # Newly added based on model
            'po',          # Newly added based on model
            'photo',                # Newly added based on model
        ]
