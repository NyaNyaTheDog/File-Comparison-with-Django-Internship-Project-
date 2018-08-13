from django import forms

class FileForm(forms.Form):
    file1_path = forms.CharField(label='File1', max_length=100)
    file2_path = forms.CharField(label='File2', max_length=100)


class UploadFileForm(forms.Form):
    file1 = forms.FileField(required=False)
    file2 = forms.FileField(required=False)