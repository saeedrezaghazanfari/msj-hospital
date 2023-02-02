from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
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

    def get_queryset(self):
        doctor_search = self.request.GET.get('doctor')
        skill_search = self.request.GET.get('skill')
        degree_search = self.request.GET.get('degree')
        gender_search = self.request.GET.get('gender')

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

        else:
            doctors = DoctorModel.objects.filter(is_active=True).all()[:12]
        return doctors


# url: /doctor/info/<medicalId>/
def doctor_info(request, medicalId):
    doctor = get_object_or_404(DoctorModel, id=medicalId)
    
    return render(request, 'doctor/info.html', {
        'doctor': doctor,
        'work_times': doctor.doctorworktimemodel_set.all()
    })
