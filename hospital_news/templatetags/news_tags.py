from django import template
from hospital_blog.models import CategoryModel


register = template.Library()


@register.simple_tag
def last_categories():
    categories_numblogs = []
    categories = CategoryModel.objects.all()
    if categories:
        for category in categories:
            categories_numblogs.append({
                'category_name': category.title, 
                'num': category.newsmodel_set.count()
            })
        return categories_numblogs
    return None
