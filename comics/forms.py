from django import forms


class SearchForm(forms.Form):
    title = forms.CharField(max_length=200, label='Введите название комикса', help_text='Название комикса')
