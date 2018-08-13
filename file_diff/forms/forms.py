from django import forms

class FileForm(forms.Form):
    file1_path = forms.CharField(label='Enter path of File1', max_length=100)
    file2_path = forms.CharField(label='\nEnter path of File2', max_length=100)