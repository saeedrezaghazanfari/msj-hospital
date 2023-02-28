from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from hospital_setting.models import (
    NewsLetterEmailsModel, FAQModel, SettingModel, HomeGalleryModel, 
    CertificateModel, HospitalImageGalleryModel, HospitalVideoGalleryModel,
    HospitalPoliticModel, ResultModel, CostModel, AncientsModel, 
    PriceBedModel, PriceServiceModel, PriceSurgrayModel,
    InsuranceModel, ContactInfoModel, HospitalFacilityModel, ReportModel
)
from hospital_doctor.models import DoctorWorkTimeModel, DoctorModel, TitleSkillModel
from hospital_units.models import UnitModel, ManagersModel
from hospital_blog.models import CreditEduModel, PampheletModel
from hospital_contact.models import FamousPatientModel, WorkshopModel, BenefactorModel
from extentions.utils import is_email, write_action


# url: /
def home_page(request):
    return render(request, 'web/home.html', {
        'faqs': FAQModel.objects.all(),
        'galleries': HomeGalleryModel.objects.all()[:6],
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


# ### about us ### #


# url: /about-us/
def aboutus_page(request):

    return render(request, 'web/aboutus/aboutus.html', {
        'setting': SettingModel.objects.first() if SettingModel.objects.exists() else None
    })


# url: /history/
def history_page(request):

    return render(request, 'web/aboutus/history.html', {
        'history': SettingModel.objects.first().history if SettingModel.objects.exists() else None
    })


# url: /workshops/
def workshops_page(request):

    return render(request, 'web/aboutus/workshops.html', {
        'active_workshops': WorkshopModel.objects.filter(start_date__gt=timezone.now()).all(),
        'prevs_workshops': WorkshopModel.objects.filter(start_date__lt=timezone.now()).all(),
    })


# url: /certificates/
def certificates_page(request):

    return render(request, 'web/aboutus/certificates.html', {
        'certificates': CertificateModel.objects.all(),
    })


# url: /gallery/images/
def gallery_imgs_page(request):

    return render(request, 'web/aboutus/gallery-imgs.html', {
        'images': HospitalImageGalleryModel.objects.all(),
    })


# >>>>  2 model before  <<<<
# HospitalGalleryModel
# HospitalGalleryItemModel


# url: /gallery/videos/
def gallery_vids_page(request):

    return render(request, 'web/aboutus/gallery-vids.html', {
        'videos': HospitalVideoGalleryModel.objects.all(),
    })


# url: /policies/
def policies_page(request):

    return render(request, 'web/aboutus/policies.html', {
        'policies': HospitalPoliticModel.objects.all()
    })


# url: /board-of-directors/
def board_of_directors_page(request):

    return render(request, 'web/aboutus/board-of-directors.html', {
        'managers': ManagersModel.objects.filter(label='hm').all(),
    })


# url: /ceo-management/
def ceo_management_page(request):

    return render(request, 'web/aboutus/ceo-management.html', {
        'managers': ManagersModel.objects.filter(label='magm').all(),
    })


# url: /chart/
def chart_page(request):
    #TODO STATIC
    return render(request, 'web/aboutus/chart.html')


# url: /results/
def results_page(request):

    return render(request, 'web/aboutus/results.html', {
        'results': ResultModel.objects.all()
    })


# url: /perspective/
def perspective_page(request):

    return render(request, 'web/aboutus/perspective.html', {
        'costs': CostModel.objects.all()
    })


# url: /visiting-famous-faces/
def visiting_famous_page(request):

    return render(request, 'web/aboutus/visiting-famous-faces.html', {
        'faces': FamousPatientModel.objects.all()
    })


# url: /patient/chart/
def patient_chart_page(request):
    #TODO STATIC
    return render(request, 'web/aboutus/patient-chart.html')


# url: /patient/edu/
def patient_edu_page(request):

    return render(request, 'web/aboutus/patient-edu.html', {
        'pamphlets': PampheletModel.objects.all(),
    })


# url: /committees/
def committees_page(request):

    committees = UnitModel.objects.filter(
        subunit__title_fa='کمیته', 
        subunit__category='official'
    ).all()

    return render(request, 'web/aboutus/committees.html', {
        'committees': committees,
    })


# url: /credit/
def credit_page(request):
    
    return render(request, 'web/aboutus/credit.html', {
        'credits': CreditEduModel.objects.all()
    })


# url: /quality-improvement/
def quality_improvement_page(request):
    
    return render(request, 'web/aboutus/quality-improvement.html', {
        'quality': SettingModel.objects.first().quality_improvement,
    })


# url: /deceaseds/
def deceaseds_page(request):

    return render(request, 'web/aboutus/deceaseds.html', {
        'ancients': AncientsModel.objects.all()
    })


# url: /benefactors/
def benefactors_page(request):

    return render(request, 'web/aboutus/benefactors.html', {
        'benefactors': BenefactorModel.objects.all(),
    })


# url: /facility/
def facility_page(request):

    return render(request, 'web/aboutus/facility.html', {
        'facilities': HospitalFacilityModel.objects.all(),
    })


# url: /reports/
def reports_page(request):

    return render(request, 'web/aboutus/reports.html', {
        'reports': ReportModel.objects.all(),
    })


# ### patient guides ### #


# url: /clinic/program/
def clinic_program_page(request):

    plan_generated = []

    for doctor in DoctorModel.objects.iterator():
        if doctor.doctorworktimemodel_set.exists():

            days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']

            for doc_time in doctor.doctorworktimemodel_set.iterator():
                
                if doc_time.day_from == doc_time.day_to:
                    plan_generated.append({
                        'doctor': doctor.get_full_name(),
                        'gender': doctor.user.gender,
                        'skill': doctor.skill_title.title,
                        'degree': doctor.degree.title,
                        'day': doc_time.day_from,
                        'from': doc_time.time_from,
                        'to': doc_time.time_to,
                    })
                else:
                    dayfrom_index = days.index(doc_time.day_from)
                    dayto_index = days.index(doc_time.day_to)

                    if dayfrom_index < dayto_index:
                      
                        for i in range(dayfrom_index, (dayto_index + 1)):
                            plan_generated.append({
                                'doctor': doctor.get_full_name(),
                                'gender': doctor.user.gender,
                                'skill': doctor.skill_title.title,
                                'degree': doctor.degree.title,
                                'day': days[i],
                                'from': doc_time.time_from,
                                'to': doc_time.time_to,
                            })

    return render(request, 'web/guides/clinic-program.html', {
        'plans': plan_generated,
        'doctors': DoctorModel.objects.filter(is_active=True).all(),
        'skills': TitleSkillModel.objects.all(),
    })


# url: /prices/
def prices_page(request):
    return render(request, 'web/guides/prices.html')


# url: /prices/bed/
def prices_bed_page(request):
        
    return render(request, 'web/guides/prices-bed.html', {
        'prices': PriceBedModel.objects.all(),
    })


# url: /prices/services/
def prices_services_page(request):
        
    return render(request, 'web/guides/prices-services.html', {
        'prices': PriceServiceModel.objects.all(),
    })


# url: /prices/surgray/
def prices_surgray_page(request):
        
    return render(request, 'web/guides/prices-surgray.html', {
        'prices': PriceSurgrayModel.objects.all(),
    })


# url: /insurances/
def insurances_page(request):

    return render(request, 'web/guides/insurances.html', {
        'insurances': InsuranceModel.objects.all(),
    })


# url: /phones/
def phones_page(request):

    return render(request, 'web/guides/phones.html', {
        'phones': ContactInfoModel.objects.all(),
    })


# url: /visitors-guide/
def visitors_guide_page(request):
    #TODO STATIC
    return render(request, 'web/guides/visitors-guide.html', {})


# ### services ### #


# url: /clinic/list/
def clinic_list_page(request):

    return render(request, 'web/service-list/clinic-list.html', {
        'clinics': UnitModel.objects.filter(subunit__title_fa='درمانگاه', subunit__category='medical').all()
    })


# url: /unit/<unitId>/
def unit_page(request, unitId):

    unit = get_object_or_404(UnitModel, id=unitId)
    members = unit.unitmembermodel_set.all()

    return render(request, 'web/service-list/unit-info.html', {
        'clinic': unit,
        'members': members,
    })
