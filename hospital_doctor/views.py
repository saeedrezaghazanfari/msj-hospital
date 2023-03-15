from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib import messages
from django.views import generic
from .models import (
    DoctorModel
)


# url: /doctor/list/
class DoctorList(generic.ListView):
    template_name = 'doctor/list.html'
    model = DoctorModel
    paginate_by = 1
    #TODO edit paginateby to some digits
    def get_queryset(self):
        return DoctorModel.objects.filter(is_active=True).all()[:12]


# url: /doctor/search/
def doctor_search(request):

    doctor_search = request.GET.get('doctor')
    skill_search = request.GET.get('skill')
    degree_search = request.GET.get('degree')
    gender_search = request.GET.get('gender')
    medicalteam = request.GET.get('medicalteam')
    international = request.GET.get('international')

    if gender_search and not gender_search in ['male', 'female']:
        return redirect(f'/{get_language()}/404')

    all_doctors_fullname = {}
    doctor_found = []
    doctors = []

    for doctor in DoctorModel.objects.filter(is_active=True).iterator():
        all_doctors_fullname[doctor.id] = doctor.user.get_full_name()

    # search with doctor full name
    if doctor_search:
        for k, v in all_doctors_fullname.items():
            if doctor_search in v:
                doctor_found.append(str(k))

        if len(doctor_found) >= 1:
            for doctorid in doctor_found:
                doctors.append(get_object_or_404(DoctorModel, id=doctorid, is_active=True))

    # search with degree or skill or gender
    elif skill_search or degree_search or gender_search:
        doctors_all = DoctorModel.objects.filter(is_active=True).all()

        if degree_search and not skill_search:
            for doctor in doctors_all:
                if doctor.degree.title == degree_search:
                    doctors.append(doctor)

        elif not degree_search and skill_search:
            for doctor in doctors_all:
                if doctor.skill_title.title == skill_search:
                    doctors.append(doctor)

        elif degree_search and skill_search:
            for doctor in doctors_all:
                if doctor.skill_title.title == skill_search and doctor.degree.title == degree_search:
                    doctors.append(doctor)

        if gender_search:
            if doctors:
                for doctor in doctors:
                    if doctor.user.gender != gender_search:
                        doctors.remove(doctor)
            else:
                for doctor in doctors_all:
                    if doctor.user.gender == gender_search:
                        doctors.append(doctor)

        if medicalteam:
            if doctors:
                for doctor in doctors:
                    if not doctor.is_medicalteam:
                        doctors.remove(doctor)
            else:
                for doctor in doctors_all:
                    if doctor.is_medicalteam:
                        doctors.append(doctor)

        if international:
            if doctors:
                for doctor in doctors:
                    if not doctor.is_international:
                        doctors.remove(doctor)
            else:
                for doctor in doctors_all:
                    if doctor.is_international:
                        doctors.append(doctor)

    else:
        doctors = DoctorModel.objects.filter(is_active=True).all()[:30]
    
    return render(request, 'doctor/search.html', {
        'doctors': doctors,
    })


# url: /doctor/info/<medicalId>/
def doctor_info(request, medicalId):
    doctor = get_object_or_404(DoctorModel, id=medicalId)
    
    return render(request, 'doctor/info.html', {
        'doctor': doctor,
        'work_times': doctor.doctorworktimemodel_set.all()
    })
