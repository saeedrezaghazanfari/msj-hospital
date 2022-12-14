from django.views import generic
from hospital_setting.models import (
   FAQModel,
   HomeGalleryModel,
)
from hospital_blog.models import (
    BlogModel,
)


# url: /
class HomePage(generic.TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['gallery_items'] = HomeGalleryModel.objects.all()
        context['last_blogs'] = BlogModel.objects.all()[:6]
        context['faq_items'] = FAQModel.objects.all()
        return context

