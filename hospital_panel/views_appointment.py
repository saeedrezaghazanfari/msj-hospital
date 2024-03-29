import calendar
from jalali_date import date2jalali
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from hospital_doctor.models import TitleSkillModel
from hospital_units.models import (
    UnitModel, LimitTurnTimeModel, AppointmentTimeModel, PatientTurnModel, 
    AppointmentTipModel, SubUnitModel, ElectronicPrescriptionModel, AppointmentTipSMSModel
)
from hospital_setting.models import PriceAppointmentModel, InsuranceModel
from hospital_doctor.models import DoctorModel, DoctorVacationModel, DegreeModel
from hospital_extentions.utils import date_range_list
from hospital_extentions.utils import write_action
from .decorators import online_appointment_required
from . import forms


# url: /panel/online-appointment
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def online_appointment_page(request):
    return render(request, 'panel/online-appointment/home.html', {})


# url: /panel/online-appointment/limit-time/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_limit_time_page(request):

    if request.method == 'POST':
        form = forms.LimitTurnTimeForm(request.POST or None)

        if form.is_valid():
            if LimitTurnTimeModel.objects.exists():
                LimitTurnTimeModel.objects.all().delete()

            form.save()
            write_action(f'{request.user.username} User set limit time in Appointment panel.', 'USER')

            messages.success(request, _('حد زمانی نوبت اینترنتی با موفقیت تنظیم شد.'))
            return redirect('panel:appointment-limittime')

    else:
        form = forms.LimitTurnTimeForm(instance=LimitTurnTimeModel.objects.first())

    return render(request, 'panel/online-appointment/limittime.html', {
        'limit_time': LimitTurnTimeModel.objects.last(),
        'form': form
    })


# url: /panel/online-appointment/insurances/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_insurances_page(request):

    insurances = InsuranceModel.objects.all()
    degrees = DegreeModel.objects.all()

    if request.method == 'POST':
        form = forms.InsuranceForm(request.POST, request.FILES or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User set insurance in Appointment panel. insuranceId: {obj.id}', 'USER')

            list_data = []
            for insurance in insurances:
                for degree in degrees:
                    if not PriceAppointmentModel.objects.filter(insurance=insurance, degree=degree).exists():
                        list_data.append(
                            PriceAppointmentModel(
                                insurance=insurance,
                                degree=degree,
                                price=0,
                            )
                        )
            for degree in degrees:
                if not PriceAppointmentModel.objects.filter(insurance=None, degree=degree).exists():
                    list_data.append(
                        PriceAppointmentModel(
                            insurance=None,
                            degree=degree,
                            price=0,
                        )
                    )
            PriceAppointmentModel.objects.bulk_create(list_data)

            messages.success(request, _('بیمه ی مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-insurances')

    else:
        form = forms.InsuranceForm()

    return render(request, 'panel/online-appointment/insurances.html', {
        'form': form,
        'insurances': insurances
    })


# url: /panel/online-appointment/tips/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_tips_page(request):

    if request.method == 'POST':
        form = forms.AppointmentTipForm(request.POST or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User set a tip in Appointment panel. tipId: {obj.id}', 'USER')
            
            messages.success(request, _('نکته ی نوبت دهی مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-tips')

    else:
        form = forms.AppointmentTipForm()

    return render(request, 'panel/online-appointment/tips.html', {
        'form': form,
        'tips': AppointmentTipModel.objects.all()
    })


# url: /panel/online-appointment/tips/sms/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_smstips_page(request):

    if request.method == 'POST':
        form = forms.AppointmentTipSMSForm(request.POST or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User set a sms tip in Appointment panel. smstipId: {obj.id}', 'USER')

            messages.success(request, _('نکته ی نوبت دهی پیامکی مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-smstips')

    else:
        form = forms.AppointmentTipSMSForm()

    return render(request, 'panel/online-appointment/sms-tips.html', {
        'form': form,
        'tips': AppointmentTipSMSModel.objects.all()
    })


# url: /panel/online-appointment/skill/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_skilltitle_page(request):

    if request.method == 'POST':
        form = forms.SkillForm(request.POST or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a skill in Appointment panel. skillId: {obj.id}', 'USER')

            messages.success(request, _('تخصص مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-skill')

    else:
        form = forms.SkillForm()

    return render(request, 'panel/online-appointment/skill.html', {
        'form': form,
        'skills': TitleSkillModel.objects.all()
    })


# url: /panel/online-appointment/degree/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_degree_page(request):

    insurances = InsuranceModel.objects.all()
    degrees = DegreeModel.objects.all()

    if request.method == 'POST':
        form = forms.DegreeForm(request.POST or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a degree in Appointment panel. degreeId: {obj.id}', 'USER')

            list_data = []
            for insurance in insurances:
                for degree in degrees:
                    if not PriceAppointmentModel.objects.filter(insurance=insurance, degree=degree).exists():
                        list_data.append(
                            PriceAppointmentModel(
                                insurance=insurance,
                                degree=degree,
                                price=0,
                            )
                        )
            for degree in degrees:
                if not PriceAppointmentModel.objects.filter(insurance=None, degree=degree).exists():
                    list_data.append(
                        PriceAppointmentModel(
                            insurance=None,
                            degree=degree,
                            price=0,
                        )
                    )
            PriceAppointmentModel.objects.bulk_create(list_data)

            messages.success(request, _('مدرک مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-degree')

    else:
        form = forms.DegreeForm()

    return render(request, 'panel/online-appointment/degree.html', {
        'form': form,
        'degrees': degrees
    })


# url: /panel/online-appointment/unit/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_unit_page(request):

    if request.method == 'POST':
        form = forms.UnitForm(request.POST, request.FILES or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a unit in Appointment panel. unitId: {obj.id}', 'USER')

            messages.success(request, _('بخش مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-unit')

    else:
        form = forms.UnitForm()

    return render(request, 'panel/online-appointment/unit.html', {
        'form': form,
        'units': UnitModel.objects.all()
    })


# url: /panel/online-appointment/subunit/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_subunit_page(request):

    paraclinics_en = ['Physiotherapy', 'Laboratory', 'Pathology', 'Imaging']
    medicals_en = ['Dialysis', 'IPD', 'Emergency', 'Clinic', 'Heart', 'CCU', 'Angiography', 'Operating Room', 'CSR', 'Adult ICU', 'Gynecological surgery', 'Obstetrics and Gynecology', "Men's surgery", 'Pediatrics and Infants or NICU']
    officials_en = ['Accounting', 'Human Resources', 'Medical Documents', 'Clearance and Admission', 'IT', 'Facilities', 'Lingerie', 'Kitchen', 'Medical Equipment', 'Health Professional', 'Environmental Health', 'Improve Quality', 'Guarding', 'Helper', 'Warehouses', 'Garbage Incinerator', 'Committee']
    paraclinics_ar = ['العلاج الطبيعي', 'معمل', 'علم الأمراض', 'التصوير']
    medicals_ar = ['غسيل الكلى', 'IPD', 'طارئ', 'عيادة', 'قلب', 'CCU', 'تصوير الأوعية', 'غرفة العمليات', 'المسؤولية الاجتماعية للشركات', 'وحدة العناية المركزة للبالغين', 'جراحة أمراض النساء', 'أمراض النساء والتوليد', 'جراحة الرجال', 'طب الأطفال والرضع NICU']
    officials_ar = ['محاسبة', 'الموارد البشرية', 'المستندات الطبية', 'التخليص والقبول', 'IT', 'مرافق', 'الملابس الداخلية', 'مطبخ', 'معدات طبية', 'الصحة المهنية', 'الصحة البيئية', 'حسن الجودة', 'حراسة', 'المساعد', 'المستودعات', 'محرقة نفايات', 'لجنة']
    paraclinics_ru = ['Физиотерапия', 'Лаборатория', 'Патология', 'визуализация']
    medicals_ru = ['Диализ', 'ИПД', 'чрезвычайная ситуация', 'клиника', 'Сердце', 'центральный блок управления', 'ангиография', 'операционная', 'КСО', 'ОИТ для взрослых', 'Гинекологическая хирургия', 'Акушерство и гинекология', 'мужская хирургия', 'Педиатрия и младенцы или NICU']
    officials_ru = ['Бухгалтерский учет', 'человеческие ресурсы', 'Медицинские документы', 'Оформление и допуск', 'это', 'удобства', 'Дамское белье', 'кухня', 'Медицинское оборудование', 'Медицинский работник', 'Состояние окружающей среды', 'Улучшить качество', 'охрана', 'помощник', 'складские помещения', 'Мусоросжигатель', 'комитет']

    paraclinics = ['فیزیوتراپی', 'آزمایشگاه', 'پاتولوژی', 'تصویربرداری']
    medicals = ['دیالیز', 'IPD', 'اورزانس', 'درمانگاه', 'قلب', 'CCU', 'آنژیوگرافی', 'اتاق عمل', 'CSR', 'ICU بزرگسال', 'جراحی زنان', 'زنان و زایمان', 'جراحی مردان', 'اطفال و نوزادان یا NICU']
    officials = ['حسابداری', 'منابع انسانی', 'اسناد پزشکی', 'ترخیص و پذیرش', 'آی‌تی', 'تاسیسات', 'لنژری', 'آشپزخانه', 'تجهیزات پزشکی', 'بهداشت حرفه‌ای', 'بهداشت محیط', 'بهبود کیفیت', 'نگهبانی', 'مددکاری', 'انبارها', 'زباله سوز', 'کمیته']
    paraclinics_list = []
    medicals_list = []
    officials_list = []

    for index, item in enumerate(paraclinics):
        if not SubUnitModel.objects.filter(category='paraclinic', title_fa=item).exists():
            if item == 'آزمایشگاه' or item == 'تصویربرداری':
                paraclinics_list.append(
                    SubUnitModel(category='paraclinic', title_fa=item, title_en=str(paraclinics_en[index]), title_ar=str(paraclinics_ar[index]), title_ru=str(paraclinics_ru[index]), have_2_box=True)
                )
            else:
                paraclinics_list.append(
                    SubUnitModel(category='paraclinic', title_fa=item, title_en=str(paraclinics_en[index]), title_ar=str(paraclinics_ar[index]), title_ru=str(paraclinics_ru[index]))
                )

    for index, item in enumerate(medicals):
        if not SubUnitModel.objects.filter(category='medical', title_fa=item).exists():
            medicals_list.append(
                SubUnitModel(category='medical', title_fa=item, title_en=str(medicals_en[index]), title_ar=str(medicals_ar[index]), title_ru=str(medicals_ru[index]))
            )

    for index, item in enumerate(officials):
        if not SubUnitModel.objects.filter(category='official', title_fa=item).exists():
            officials_list.append(
                SubUnitModel(category='official', title_fa=item, title_en=str(officials_en[index]), title_ar=str(officials_ar[index]), title_ru=str(officials_ru[index]))
            )

    if len(paraclinics_list) > 0:
        SubUnitModel.objects.bulk_create(paraclinics_list)
    if len(medicals_list) > 0:
        SubUnitModel.objects.bulk_create(medicals_list)
    if len(officials_list) > 0:
        SubUnitModel.objects.bulk_create(officials_list)

    if request.method == 'POST':
        form = forms.SubUnitForm(request.POST or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a subunit in Appointment panel. subunitId: {obj.id}', 'USER')

            messages.success(request, _('زیربخش مورد نظر با موفقیت اضافه شد.'))
            return redirect('panel:appointment-subunit')

    else:
        form = forms.SubUnitForm()

    return render(request, 'panel/online-appointment/subunit.html', {
        'form': form,
        'subunits': SubUnitModel.objects.all()
    })


# url: /panel/online-appointment/doctor/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_doctorlist_page(request):
    doctors = DoctorModel.objects.filter(is_active=True).all()

    for doctor in doctors:
        doctor.have_not_accecpted_vac = False
        if doctor.doctorvacationmodel_set.filter(is_accepted=False).exists():
            doctor.have_not_accecpted_vac = True

    return render(request, 'panel/online-appointment/doctor-list.html', {
        'doctors': doctors
    })


# url: /panel/online-appointment/doctor/create/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_doctorcreate_page(request):

    if request.method == 'POST':
        form = forms.DoctorForm(request.POST or None)

        if form.is_valid():
            obj = form.save()
            write_action(f'{request.user.username} User created a doctor in Appointment panel. doctormedicalCode: {obj.medical_code}', 'USER')

            messages.success(request, _('پزشک با موفقیت اضافه شد.'))
            return redirect('panel:appointment-doctorlist')

    else:
        form = forms.DoctorForm()

    return render(request, 'panel/online-appointment/doctor-create.html', {
        'form': form
    })


# url: /panel/online-appointment/doctor/<doctorId>/times/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_doctorlist_time_page(request, doctorId):

    doctor = get_object_or_404(DoctorModel, id=doctorId, is_active=True)

    if doctor:

        works = doctor.doctorworktimemodel_set.all()
        vacations = doctor.doctorvacationmodel_set.all()

        # update vacation of doctor
        if request.GET.get('vid') and DoctorVacationModel.objects.filter(id=request.GET.get('vid')).exists():
            doc_vac = DoctorVacationModel.objects.get(id=request.GET.get('vid'))
            doc_vac.is_accepted=True
            doc_vac.save()

        return render(request, 'panel/online-appointment/doctor-time.html', {
            'doctor': doctor,
            'works': works,
            'vacations': vacations,
        })
    return redirect(f'/{get_language()}/404')


# url: /panel/online-appointment/doctor/<doctorId>/edit/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_doctorlist_edit_page(request, doctorId):

    doctor = get_object_or_404(DoctorModel, id=doctorId, is_active=True)

    if request.method == 'POST':
        form = forms.DoctorForm(request.POST, request.FILES or None, instance=doctor)

        if form.is_valid():
            form.save()
            write_action(f'{request.user.username} User edited a doctor in Appointment panel. doctorMedicalcode: {doctor.medical_code}', 'USER')
            
            messages.success(request, _('پزشک مورد نظر با موفقیت ویرایش شد.'))
            return redirect('panel:appointment-doctorlist')

    else:
        form = forms.DoctorForm(instance=doctor)

    return render(request, 'panel/online-appointment/doctor-edit.html', {
        'form': form
    })


# url: /panel/online-appointment/price/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_price_page(request):

    insurances = InsuranceModel.objects.all()
    degrees = DegreeModel.objects.all()

    list_data = []
    for insurance in insurances:
        for degree in degrees:
            if not PriceAppointmentModel.objects.filter(insurance=insurance, degree=degree).exists():
                list_data.append(
                    PriceAppointmentModel(
                        insurance=insurance,
                        degree=degree,
                        price=0,
                    )
                )
                
    for degree in degrees:
        if not PriceAppointmentModel.objects.filter(insurance=None, degree=degree).exists():
            list_data.append(
                PriceAppointmentModel(
                    insurance=None,
                    degree=degree,
                    price=0,
                )
            )

    PriceAppointmentModel.objects.bulk_create(list_data)

    prices = PriceAppointmentModel.objects.all()
    context = {
        'prices': prices,
    }

    if request.method == 'POST':
        price = int(request.POST.get('price'))
        data_id = request.POST.get('data')

        if price == 0:
            messages.error(request, _('مقدار مبلغ را وارد کنید.'))
            return redirect('panel:appointment-price')

        if price < 0:
            messages.error(request, _('مقدار این مبلغ نمیتواند منفی باشد.'))
            return redirect('panel:appointment-price')

        if price and data_id and PriceAppointmentModel.objects.filter(id=data_id).exists():
            appointment = PriceAppointmentModel.objects.get(id=data_id)
            appointment.price = price

            appointment.save()
            write_action(f'{request.user.username} User updated a appointment price in Appointment panel. appointmentPriceId: {appointment.id}', 'USER')

        messages.success(request, _('تعرفه ی مورد نظر شما با موفقیت بروزرسانی شد.'))
        return redirect('panel:appointment-price')

    return render(request, 'panel/online-appointment/price-appointment.html', context)


# url: /panel/online-appointment/time/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_time_page(request):

    times = None
    
    if request.GET.get('type') == 'doctors':
        times = AppointmentTimeModel.objects.filter(
            unit=None,
            date__gt=timezone.now()
        ).all()

    elif request.GET.get('type') == 'labs':
        times = AppointmentTimeModel.objects.filter(
            unit__subunit__category='paraclinic',
            unit__subunit__title_fa='آزمایشگاه',
            date__gt=timezone.now()
        ).all()

    elif request.GET.get('type') == 'imaging':
        times = AppointmentTimeModel.objects.filter(
            unit__subunit__category='paraclinic',
            unit__subunit__title_fa='تصویربرداری',
            date__gt=timezone.now()
        ).all()

    elif not request.GET.get('type') or request.GET.get('type') == 'all':
        times = AppointmentTimeModel.objects.filter(
            date__gt=timezone.now()
        ).all()
    
    return render(request, 'panel/online-appointment/time-appointment.html', {
        'times': times,
    })


# url: /panel/online-appointment/time/<appointmentID>/edit/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_time_edit_page(request, appointmentID):

    if not appointmentID or not AppointmentTimeModel.objects.filter(id=appointmentID).exists():
        return redirect(f'/{get_language()}/404')

    appointment = AppointmentTimeModel.objects.get(id=appointmentID)

    if request.method == 'POST':
        form = forms.AllAppointmentForm(request.POST or None)

        if form.is_valid():

            if request.POST.get('unit') and request.POST.get('unit') != 'doctors':
                appointment.unit = UnitModel.objects.get(id=request.POST.get('unit'))
            elif request.POST.get('unit') and request.POST.get('unit') == 'doctors':
                appointment.unit = None
            if request.POST.getlist('insurances') and len(request.POST.getlist('insurances')) > 0:
                appointment.insurances.clear()
                for item in request.POST.getlist('insurances'):
                    appointment.insurances.add(InsuranceModel.objects.get(id=item))
            if form.cleaned_data.get('time_from'):
                appointment.time_from = form.cleaned_data.get('time_from')
            if form.cleaned_data.get('time_to'):
                appointment.time_to = form.cleaned_data.get('time_to')
            if form.cleaned_data.get('capacity'):
                appointment.capacity = form.cleaned_data.get('capacity')
            if form.cleaned_data.get('tip'):
                appointment.tip = form.cleaned_data.get('tip')
            if form.cleaned_data.get('tip_sms'):
                appointment.tip_sms = form.cleaned_data.get('tip_sms')
            if form.cleaned_data.get('status'):
                appointment.status = form.cleaned_data.get('status')

            appointment.save()
            write_action(f'{request.user.username} User edited time appointment in Appointment panel. appointmentId: {appointment.id}', 'USER')
            
            messages.success(request, _('زمان نوبت دهی موردنظر با موفقیت تغییر یافت.'))
            return redirect('panel:appointment-time')

    else:
        form = forms.AllAppointmentForm(instance=appointment)

    return render(request, 'panel/online-appointment/edit-time-appointment.html', {
        'form': form,
        'appointment': appointment,
        'units': UnitModel.objects.all(),
        'times': AppointmentTimeModel.objects.filter(date__gt=timezone.now()).all(),
        'insurances': [insurance for insurance in appointment.doctor.insurances.all()]
    })


# url: /panel/online-appointment/time/create/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_time_create0_page(request):

    units = UnitModel.objects.all()

    if request.method == 'POST':
        unit = request.POST.get('units')

        if unit == 'doctors':
            return HttpResponseRedirect(reverse('panel:appointment-timep1', args=('doctors',)))
        return HttpResponseRedirect(reverse('panel:appointment-timep1', args=(unit,)))

    return render(request, 'panel/online-appointment/time-p0-appointment.html', {
        'units': units,
    })


# url: /panel/online-appointment/time/create/<unitID>/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_time_create1_page(request, unitID):

    if unitID != 'doctors' and UnitModel.objects.filter(id=unitID).exists():
        unit = UnitModel.objects.get(id=unitID)
    elif unitID == 'doctors':
        unit = None
    elif not unitID:
        return redirect(f'/{get_language()}/404')

    if request.method == 'POST':
        
        if request.POST.get('doctor'):

            doctor = None
            if DoctorModel.objects.filter(id=request.POST.get('doctor')).exists():
                doctor = DoctorModel.objects.get(id=request.POST.get('doctor'))

            if doctor and unit:
                return HttpResponseRedirect(reverse('panel:appointment-timep2', args=(unit.id, doctor.id)))
            elif doctor and not unit:
                return HttpResponseRedirect(reverse('panel:appointment-timep2', args=('doctors', doctor.id)))            
            else:
                messages.error(request, _('باید حداقل یکی از فیلد ها مقدار داشته باشد.'))
                return redirect('panel:appointment-timep1')

    return render(request, 'panel/online-appointment/time-p1-appointment.html', {
        'doctors': DoctorModel.objects.filter(is_active=True).all(), 
    })


# url: /panel/online-appointment/time/create/<unitID>/<doctorId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_time_create2_page(request, unitID, doctorId):

    if unitID != 'doctors' and UnitModel.objects.filter(id=unitID).exists():
        unit = UnitModel.objects.get(id=unitID)
    elif unitID == 'doctors':
        unit = None
    elif not unitID:
        return redirect(f'/{get_language()}/404')

    if doctorId != 'doctors' and DoctorModel.objects.filter(is_active=True, id=doctorId).exists():
        doctor = DoctorModel.objects.get(is_active=True, id=doctorId)
    elif doctorId == 'doctors' or not doctorId:
        return redirect(f'/{get_language()}/404')

    if request.method == 'POST':
        form = forms.Time2AppointmentForm(request.POST or None)

        if len(request.POST.getlist('days')) == 0:
            messages.info(request, _('لطفا روز های مورد نظر خود را انتخاب کنید.'))
            return redirect(f'/{get_language()}/panel/online-appointment/time/create/{unitID}/{doctorId}/')

        if form.is_valid():
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            range_date = date_range_list(date_from, date_to)
            insurances_list = request.POST.getlist('insurances')
            days_list = request.POST.getlist('days')

            insurances_obj = []
            if len(insurances_list) > 0:
                for insurance_id in insurances_list:
                    if InsuranceModel.objects.filter(id=insurance_id).exists():
                        insurances_obj.append(InsuranceModel.objects.get(id=insurance_id))

            for date in range_date:
                day = calendar.day_name[date.weekday()].lower()
                if day in days_list:

                    time = AppointmentTimeModel.objects.create(
                        unit=unit,
                        doctor=doctor,
                        date=date,
                        day=day,
                        time_from=form.cleaned_data.get('time_from'),
                        time_to=form.cleaned_data.get('time_to'),
                        capacity=form.cleaned_data.get('capacity'),
                        reserved=0,
                        tip=form.cleaned_data.get('tip'),
                    )
                    # add insurances to queryset
                    for item in insurances_obj:
                        time.insurances.add(item)

            write_action(f'{request.user.username} User created a time appointment in Appointment panel.', 'USER')
            messages.success(request, _('زمان نوبت دهی مورد نظر شما با موفقیت اضافه شد.'))
            return redirect('panel:appointment-time')

    else:
        form = forms.Time2AppointmentForm()

    return render(request, 'panel/online-appointment/time-p2-appointment.html', {
        'form': form,
        'insurances': [insurance for insurance in doctor.insurances.all()]
    })


# url: /panel/online-appointment/patient/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_patient_page(request):

    if request.GET.get('paid') == 'yes':
        patients = PatientTurnModel.objects.filter(
            is_paid=True,
            appointment__date__gt=timezone.now()
        ).all()

    elif request.GET.get('paid') == 'no':
        patients = PatientTurnModel.objects.filter(
            is_paid=False,
            appointment__date__gt=timezone.now()
        ).all()

    elif request.GET.get('returned') == 'yes':
        patients = PatientTurnModel.objects.filter(
            is_canceled=True,
            is_returned=True,
            appointment__date__gt=timezone.now()
        ).all()

    elif request.GET.get('returned') == 'no':
        patients = PatientTurnModel.objects.filter(
            is_canceled=True,
            is_returned=False,
            appointment__date__gt=timezone.now()
        ).all()

    else:
        patients = PatientTurnModel.objects.filter(
            appointment__date__gt=timezone.now()
        ).all()

    return render(request, 'panel/online-appointment/patient.html', {
        'patients': patients, 
    })


# url: /panel/online-appointment/e-turn/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_eturn_list_page(request):

    turns = ElectronicPrescriptionModel.objects.filter(is_send=False).all()
    return render(request, 'panel/online-appointment/eturns.html', {
        'turns': turns, 
    })


# url: /panel/online-appointment/e-turn/<eturnID>/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_eturn_check_page(request, eturnID):

    if eturnID and ElectronicPrescriptionModel.objects.filter(id=eturnID).exists():
        turn = ElectronicPrescriptionModel.objects.get(id=eturnID)

    if request.method == 'POST':
        form = forms.ElectronicPrescriptionForm(request.POST or None)

        if form.is_valid():
            
            if not form.cleaned_data.get('doctor') or not form.cleaned_data.get('unit'):
                messages.error(request, _('باید تمامی فیلدها مقدار داشته باشند.'))
                return redirect(f'/{get_language()}/panel/online-appointment/e-turn/{eturnID}/')

            turn.doctor = form.cleaned_data.get('doctor')
            turn.unit = form.cleaned_data.get('unit')
            turn.selected_date = form.cleaned_data.get('selected_date')
            turn.selected_time = form.cleaned_data.get('selected_time')
            turn.is_send = True
            
            turn.save()
            write_action(f'{request.user.username} User set time for e-turn of patient in Appointment panel. turnId: {turn.id}', 'USER')

            # TODO  send sms to patient

            pg = 'آقای'
            dg = 'آقای'
            jalali_selected_date = date2jalali(turn.selected_date).strftime('%y/%m/%d')

            if turn.patient.gender == 'female':
                pg = 'خانم'
            if turn.doctor.user.gender == 'female':
                dg = 'خانم'

            msg = f"""
            جناب {pg} {turn.patient.get_full_name()}، به اطلاع می‌رساند که نوبت شما جهت معاینه توسط
             جناب {dg} دکتر {turn.doctor.user.get_full_name()} {turn.doctor.degree} {turn.doctor.skill_title.title}، تاریخ {jalali_selected_date} ساعت {turn.selected_time} در محل
             بیمارستان موسی‌ابن‌جعفر، {turn.unit.address} می‌باشد. لطفا 15 دقیقه قبل از ساعت مذکور در 
            محل پذیرش بیمارستان حضور داشته باشید، در غیراینصورت به منزله انصراف خواهد بود. با تشکر
            """
            print(msg)

            messages.success(request, _('.....'))
            return redirect('panel:appointment-eturnlist')
    
    else:
        form = forms.ElectronicPrescriptionForm()

    return render(request, 'panel/online-appointment/eturns-check.html', {
        'form': form,
        'turn': turn
    })


# ### mission ### #

# url: /panel/online-appointment/missions/lvl1/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_mission_1(request):
    return render(request, 'panel/missions/lvl1.html', {
        'limit': LimitTurnTimeModel.objects.first().hours if LimitTurnTimeModel.objects.exists() else 6,
        'insurances': InsuranceModel.objects.all()
    })


# url: /panel/online-appointment/missions/lvl2/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_mission_2(request):
    return render(request, 'panel/missions/lvl2.html', {
        'units': UnitModel.objects.all()
    })


# url: /panel/online-appointment/missions/lvl3/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_mission_3(request):
    return render(request, 'panel/missions/lvl3.html', {
        'doctors': DoctorModel.objects.filter(is_active=True).all()
    })


# url: /panel/online-appointment/missions/lvl4/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_mission_4(request):
    return render(request, 'panel/missions/lvl4.html', {
        'tips': AppointmentTipModel.objects.all(),
    })


# url: /panel/online-appointment/missions/lvl5/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_mission_5(request):
    return render(request, 'panel/missions/lvl5.html', {
        'sms_tips': AppointmentTipSMSModel.objects.all(),
    })


# url: /panel/online-appointment/missions/lvl6/
@login_required(login_url=reverse_lazy('auth:signin'))
@online_appointment_required(login_url=f'/{get_language()}/403')
def oa_mission_6(request):
    return render(request, 'panel/missions/lvl6.html')