from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from hospital_setting.models import (
    NewsLetterEmailsModel, SettingModel, HomeGalleryModel, 
    CertificateModel, HospitalImageGalleryModel, HospitalVideoGalleryModel,
    HospitalPoliticModel, ResultModel, CostModel, AncientsModel, 
    PriceBedModel, PriceServiceModel, PriceSurgrayModel,
    InsuranceModel, ContactInfoModel, HospitalFacilityModel, ReportModel
)
from hospital_doctor.models import DoctorModel, TitleSkillModel
from hospital_units.models import UnitModel, ManagersModel
from hospital_blog.models import BlogModel, CreditEduModel, PampheletModel
from hospital_news.models import NewsModel
from hospital_contact.models import FamousPatientModel, WorkshopModel, BenefactorModel
from hospital_extentions.utils import is_email, write_action


# url: /
def home_page(request):
    return render(request, 'web/home.html', {
        'galleries': HomeGalleryModel.objects.all()[:6],
        'links': SettingModel.objects.first(),
        'services': UnitModel.objects.all()[:20],
        'blogs': BlogModel.objects.filter(is_publish=True).all()[:7],
        'news': NewsModel.objects.filter(is_publish=True).all()[:7],
        'insurances': InsuranceModel.objects.all()[:30],
    })


# url: /home/doctors/data/
@csrf_exempt
def home_doctors_info_api(request):

    if request.method == 'POST':

        list_doctors = DoctorModel.objects.filter(is_active=True).all()[:50]

        gallery = []
        for doctor in list_doctors:
            if doctor.user.profile:
                gallery.append({
                    'name': doctor.get_full_name(),
                    'img': doctor.user.profile.url,
                    'skill': doctor.skill_title.title,
                    'uid': doctor.id,
                })
            if len(gallery) == 9:
                break
            
        selectbox = []
        for doctor in list_doctors:
            selectbox.append({
                'name': doctor.get_full_name(),
                'uid': doctor.id,
            })

        return JsonResponse({
            'doctors': selectbox,
            'skills': list(TitleSkillModel.objects.all()[:50].values('id', 'title_en', 'title_fa', 'title_ar', 'title_ru')),
            'clinics': list(UnitModel.objects.filter(subunit__title_fa='درمانگاه', subunit__category='medical').all()[:30].values(
                'id', 'subunit__title_en', 'subunit__title_fa', 'subunit__title_ar', 'subunit__title_ru', 
                'title_ar', 'title_en', 'title_fa', 'title_ru'
            )),
            'doctors_gallery': gallery,
            'status': 200,
        })
    return JsonResponse({'status': 400}) 


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
        'prevs_workshops': WorkshopModel.objects.filter(start_date__lt=timezone.now()).all()[:20],
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
    # چارت بیمارستان
    # چارت سازمانی
    # خط مشی کیفیت بیمارستان
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
    # منشور حقوق بیمار
    # منشور ایمنی بیمار
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
    return render(request, 'web/guides/clinic-program.html')


# url: /clinic/program/get-data/
@csrf_exempt
def clinic_program_getdata(request):

    if request.method == 'POST':

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

        counter = int(request.POST.get('counter'))
        if not counter:
            counter = 1000
        plan_generated = plan_generated[:counter]

        if get_language() == 'fa':
            get_skills = list(TitleSkillModel.objects.values('title_fa'))
        elif get_language() == 'en':
            get_skills = list(TitleSkillModel.objects.values('title_en'))
        elif get_language() == 'ar':
            get_skills = list(TitleSkillModel.objects.values('title_ar'))
        elif get_language() == 'ru':
            get_skills = list(TitleSkillModel.objects.values('title_ru'))


        get_doctor_list = list()
        for doctor_item in DoctorModel.objects.filter(is_active=True).iterator():
            if not doctor_item.get_full_name() in get_doctor_list: 
                get_doctor_list.append(doctor_item.get_full_name())

        return JsonResponse({
            'status': 200,
            'plans': plan_generated,
            'doctors': get_doctor_list,
            'skills': get_skills,
        })
    
    return JsonResponse({'status': 400})



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
    # راهنمای پذیرش تا ترخیص بیمار 
    # مدارک مورد نیاز پذیرش بیمار 
    # راهنمای پوشش کارکنان
    # راهنمای ملاقات در بخش‌های ویژه
    # راهنمای طبقات بیمارستان
    # مسیرهای دسترسی به بیمارستان
    # منشور حقوق پرسنل
    return render(request, 'web/guides/visitors-guide.html', {})


# ### services ### #


# url: /unit/clinic/list/
def clinic_list_page(request):

    return render(request, 'web/service-list/unit-list.html', {
        'units': UnitModel.objects.filter(subunit__title_fa='درمانگاه', subunit__category='medical').all()
    })


# url: /unit/operating-room/list/
def operating_room_list_page(request):

    return render(request, 'web/service-list/unit-list.html', {
        'units': UnitModel.objects.filter(subunit__title_fa='اتاق عمل', subunit__category='medical').all()
    })


# url: /unit/official/list/
def official_list_page(request):

    return render(request, 'web/service-list/unit-list.html', {
        'units': UnitModel.objects.filter(subunit__category='official').all()
    })
    

# url: /unit/paraclinic/list/
def paraclinic_list_page(request):

    return render(request, 'web/service-list/unit-list.html', {
        'units': UnitModel.objects.filter(subunit__category='paraclinic').all()
    })
    

# url: /unit/medical/list/
def medical_list_page(request):

    return render(request, 'web/service-list/unit-list.html', {
        'units': UnitModel.objects.filter(~Q(subunit__title_fa='درمانگاه'), subunit__category='medical').all()
    })


# url: /unit/<unitId>/
def unit_page(request, unitId):

    unit = get_object_or_404(UnitModel, id=unitId)
    members = unit.unitmembermodel_set.all()

    return render(request, 'web/service-list/unit-info.html', {
        'unit': unit,
        'members': members,
    })
