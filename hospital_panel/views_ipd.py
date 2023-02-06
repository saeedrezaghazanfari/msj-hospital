from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from extentions.utils import write_action
from hospital_ipd.models import IPDModel
from hospital_ipd.forms import IPDForm
from .decorators import ipd_required


# url: /panel/ipd/list/
@login_required(login_url=reverse_lazy('auth:signin'))
@ipd_required(login_url=f'/{get_language()}/403')
def ipd_list_page(request):

    return render(request, 'panel/ipd/list.html', {
        'noanswered_ipds': IPDModel.objects.filter(is_answered=False).all(),
        'answered_ipds': IPDModel.objects.filter(is_answered=True).all(),
    })


# url: /panel/ipd/list/<ipdId>/
@login_required(login_url=reverse_lazy('auth:signin'))
@ipd_required(login_url=f'/{get_language()}/403')
def ipd_info_page(request, ipdId):

    ipd_obj = get_object_or_404(IPDModel, id=ipdId)

    # if request.method == 'POST':
        # form = forms.

        # if form.is_valid():
            # ...

    #TODO send sms code to ipd + message         


    # else:
        # form = forms.

    return render(request, 'panel/ipd/info.html', {
        'ipd': ipd_obj,
        'form': '',
    })