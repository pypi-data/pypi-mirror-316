# Not used anymore in dashboard

from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import editor

class ckeditor(forms.ModelForm):
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 12}))
    class Meta:
        model = editor
        fields = "__all__"
        labels = {'content':"JSON Data"}
        widgets = {            
            'content': forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 12}))
        }