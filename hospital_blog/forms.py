from django import forms
from django.utils.translation import gettext_lazy as _
from .models import BlogCommentModel
from hospital_extentions.validations import name_val, phone_val
from hospital_extentions.customs import CustomizedModelForm


class BlogCommentForm(CustomizedModelForm):
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


class BlogReplyForm(CustomizedModelForm):
    comment_id = forms.CharField(widget=forms.HiddenInput())
    blog_slug = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = BlogCommentModel
        fields = ['message']


class BlogCommentEditForm(CustomizedModelForm):
    comment_id = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = BlogCommentModel
        fields = ['message']