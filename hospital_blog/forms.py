from django import forms
from django.utils.translation import gettext_lazy as _
from .models import BlogCommentModel
from extentions.validations import name_val, phone_val


class BlogCommentForm(forms.ModelForm):
    comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = BlogCommentModel
        fields = ['message', 'first_name', 'last_name', 'phone', 'comment_id']

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        output = name_val(name=data, required=True)
        return output
    
    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')
        output = name_val(name=data, required=True)
        return output
    
    def clean_phone(self):
        data = self.cleaned_data.get('phone')
        output = phone_val(phone=data, required=True)
        return output


class BlogReplyForm(forms.ModelForm):
    comment_id = forms.CharField(widget=forms.HiddenInput())
    blog_slug = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = BlogCommentModel
        fields = ['message']


class BlogCommentEditForm(forms.ModelForm):
    comment_id = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = BlogCommentModel
        fields = ['message']