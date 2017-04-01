from django import forms
from .models import HostList

class HostsListForm(forms.ModelForm):

    class Meta:
        model = HostList
        fields = ('ip', 'hostname', 'product', 'application', 'idc_jp', 'status', 'remark')
        widgets = {
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'application': forms.TextInput(attrs={'class': 'form-control'}),
            'idc_jp': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'from-control'}),
            'remark': forms.TextInput(attrs={'class': 'from-control'}),
        }