from django import forms
from django.forms import ModelForm
from .models import Book, DNDPage, SRDPage


class BookCreateForm(ModelForm):
    class Meta:
        model = Book
        fields = ('title', )


class DNDPageCreateForm(ModelForm):
    class Meta:
        model = DNDPage
        fields = ('title', 'sub_title', 'casting_time', 'casting_range', 'components', 'duration', 'description')


class SRDSelectForm(forms.Form):
    srd_spells = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['srd_spells'].queryset = SRDPage.objects.all().order_by('title')
