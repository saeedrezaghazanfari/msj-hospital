from django.shortcuts import render, redirect
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from hospital_setting.models import NewsLetterEmailsModel, FAQModel
from extentions.utils import is_email


# url: /
def home_page(request):
    return render(request, 'web/home.html', {
        'faqs': FAQModel.objects.all(),
    })


# url: /newsletter/register/
def newsletter_page(request):
    
    if request.method == 'POST':
        email_field = request.POST.get('email_field')
        redirect_field = request.GET.get('route')

        if email_field and redirect_field:

            if not is_email(email_field):
                messages.error(request, _('الگوی ایمیل شما صحیح نیست.'))
                return redirect(redirect_field)

            if NewsLetterEmailsModel.objects.filter(email=email_field).exists():
                messages.error(request, _('قبلا این آدرس ایمیل در خبرنامه ثبت شده است.'))
                return redirect(redirect_field)
            
            NewsLetterEmailsModel.objects.create(
                email=email_field
            )
            messages.success(request, _('ایمیل شما با موفقیت در سیستم ثبت شد.'))
            return redirect(redirect_field)
            
        return redirect(f'/{get_language()}/404')
    return redirect(f'/{get_language()}/404')

