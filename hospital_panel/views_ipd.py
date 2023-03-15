from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from hospital_extentions.utils import write_action
from hospital_ipd.models import IPDModel
from .forms import IPDAnswerForm
from .decorators import ipd_required


# url: /panel/ipd/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@ipd_required(login_url=f'/{get_language()}/403')
def ipd_list_page(request):

    return render(request, 'panel/ipd/list.html', {
        'noanswered_ipds': IPDModel.objects.filter(doctor_answerer=request.user, is_answered=False).all(),
        'answered_ipds': IPDModel.objects.filter(doctor_answerer=request.user, is_answered=True).all(),
    })


# url: /panel/ipd/list/<ipdId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@ipd_required(login_url=f'/{get_language()}/403')
def ipd_info_page(request, ipdId):

    ipd_obj = get_object_or_404(IPDModel, id=ipdId, doctor_answerer=request.user)

    if request.method == 'POST':
        form = IPDAnswerForm(request.POST or None, instance=ipd_obj)

        if not request.POST.get('surement'):
            messages.info(request, _('برای ارسال پاسخ باید اطمینان کامل را داشته باشید.'))
            return redirect(f'/{get_language()}/panel/ipd/list/{ipdId}/')

        if form.is_valid():

            if not ipd_obj.is_answered:
                #TODO send sms ipd_obj.code to ipd + link + message(for about send answer)
                print(f'code: {ipd_obj.code}') #TODO delete here 
                write_action(f'{request.user.username} User Wrote answer for IPD. ipd: {ipd_obj.code}', 'USER')

            elif ipd_obj.is_answered:
                #TODO send sms ipd_obj.code to ipd + link + message(for about update answer)
                print(f'code: {ipd_obj.code}') #TODO delete here 
                write_action(f'{request.user.username} User Updated answer for IPD. ipd: {ipd_obj.code}', 'USER')

            ipd_obj.doctor_answerer = request.user
            ipd_obj.answer = form.cleaned_data.get('answer')
            ipd_obj.is_answered = True

            ipd_obj.save()

            messages.success(request, _('پاسخ شما با موفقیت ارسال شد.'))
            return redirect('panel:ipd-list')

    else:
        form = IPDAnswerForm(instance=ipd_obj)

    return render(request, 'panel/ipd/info.html', {
        'ipd': ipd_obj,
        'form': form,
    })


