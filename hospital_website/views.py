from django.utils import timezone
from django.shortcuts import render, redirect
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from hospital_setting.models import (
    NewsLetterEmailsModel, FAQModel, SettingModel, HomeGalleryModel, CertificateModel, 
    HospitalImageGalleryModel, HospitalVideoGalleryModel, HospitalPoliticModel, ResultModel, CostModel, AncientsModel
)
from hospital_units.models import UnitModel
from hospital_blog.models import CreditEduModel
from hospital_contact.models import FamousPatientModel, WorkshopModel
from extentions.utils import is_email, write_action


# url: /
def home_page(request):
    return render(request, 'web/home.html', {
        'faqs': FAQModel.objects.all(),
        'galleries': HomeGalleryModel.objects.all(),
    })


# url: /search/?query=
def search_page(request):
    return render(request, 'web/search.html')


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

            write_action(f'register an email to newsletter. email: {email_field}', 'ANONYMOUS')

            messages.success(request, _('ایمیل شما با موفقیت در سیستم ثبت شد.'))
            return redirect(redirect_field)
            
        return redirect(f'/{get_language()}/404')
    return redirect(f'/{get_language()}/404')


# url: /about-us/
def aboutus_page(request):

    return render(request, 'web/aboutus.html', {
        'setting': SettingModel.objects.first() if SettingModel.objects.exists() else None
    })


# url: /history/
def history_page(request):

    return render(request, 'web/history.html', {
        'history': SettingModel.objects.first().history if SettingModel.objects.exists() else None
    })


# url: /workshops/
def workshops_page(request):

    return render(request, 'web/workshops.html', {
        'active_workshops': WorkshopModel.objects.filter(start_date__gt=timezone.now()).all(),
        'prevs_workshops': WorkshopModel.objects.filter(start_date__lt=timezone.now()).all(),
    })


# url: /certificates/
def certificates_page(request):

    return render(request, 'web/certificates.html', {
        'certificates': CertificateModel.objects.all(),
    })


# url: /gallery/images/
def gallery_imgs_page(request):

    return render(request, 'web/gallery-imgs.html', {
        'images': HospitalImageGalleryModel.objects.all(),
    })


# >>>>  2 model before  <<<<
# HospitalGalleryModel
# HospitalGalleryItemModel


# url: /gallery/videos/
def gallery_vids_page(request):

    return render(request, 'web/gallery-vids.html', {
        'videos': HospitalVideoGalleryModel.objects.all(),
    })


# url: /policies/
def policies_page(request):

    return render(request, 'web/policies.html', {
        'policies': HospitalPoliticModel.objects.all()
    })


# url: /management/
def management_page(request):
    #TODO
    return render(request, 'web/management.html')


# url: /chart/
def chart_page(request):
    #TODO
    return render(request, 'web/chart.html')


# url: /results/
def results_page(request):

    return render(request, 'web/results.html', {
        'results': ResultModel.objects.all()
    })


# url: /perspective/
def perspective_page(request):

    return render(request, 'web/perspective.html', {
        'costs': CostModel.objects.all()
    })


# url: /visiting-famous-faces/
def visiting_famous_page(request):

    return render(request, 'web/visiting-famous-faces.html', {
        'faces': FamousPatientModel.objects.all()
    })


# url: /patient-chart/
def patient_chart_page(request):
    #TODO
    return render(request, 'web/patient-chart.html')


# url: /committees/
def committees_page(request):

    committees = UnitModel.objects.filter(
        subunit__title_fa='کمیته', 
        subunit__category='official'
    ).all()

    return render(request, 'web/committees.html', {
        'committees': committees
    })


# url: /credit/
def credit_page(request):
    
    return render(request, 'web/credit.html', {
        'credits': CreditEduModel.objects.all()
    })


# url: /quality-improvement/
def quality_improvement_page(request):
    # TODO
    return render(request, 'web/quality-improvement.html', {})


# url: /deceaseds/
def deceaseds_page(request):

    return render(request, 'web/deceaseds.html', {
        'ancients': AncientsModel.objects.all()
    })

