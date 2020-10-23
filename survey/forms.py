from django import forms

class SearchBar(forms.Form):
    search = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'placeholder': 'Search surveys'})
