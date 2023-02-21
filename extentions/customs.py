from django import forms
from django.forms.forms import BaseForm
# from django.forms.utils import RenderableFormMixin
# from django.forms.formsets import BaseFormSet


### customize as_p in template ###


class CustomBaseForm(BaseForm):
    template_name_p = "forms/customform.html"


# class CustomRenderableFormMixin(RenderableFormMixin):
#     def as_customform(self):
#         return self.render(self.template_name_customform)


# class CustomBaseFormSet(BaseFormSet):
#     template_name_ul = "django/forms/formsets/ul.html"


class CustomizedForm(CustomBaseForm, metaclass=forms.forms.DeclarativeFieldsMetaclass):
    pass





# # these are imports of method1
# from django.forms.utils import ErrorList
# from django.core.exceptions import (
#     NON_FIELD_ERRORS,
#     ValidationError
# )
# from itertools import chain
# from django.forms.models import InlineForeignKeyField, construct_instance


# method1
# class BaseModelForm(CustomBaseForm):
#     def __init__(
#         self,
#         data=None,
#         files=None,
#         auto_id="id_%s",
#         prefix=None,
#         initial=None,
#         error_class=ErrorList,
#         label_suffix=None,
#         empty_permitted=False,
#         instance=None,
#         use_required_attribute=None,
#         renderer=None,
#     ):
#         opts = self._meta
#         if opts.model is None:
#             raise ValueError("ModelForm has no model class specified.")
#         if instance is None:
#             # if we didn't get an instance, instantiate a new one
#             self.instance = opts.model()
#             object_data = {}
#         else:
#             self.instance = instance
#             object_data = forms.model_to_dict(instance, opts.fields, opts.exclude)
#         # if initial was provided, it should override the values from instance
#         if initial is not None:
#             object_data.update(initial)
#         # self._validate_unique will be set to True by BaseModelForm.clean().
#         # It is False by default so overriding self.clean() and failing to call
#         # super will stop validate_unique from being called.
#         self._validate_unique = False
#         super().__init__(
#             data,
#             files,
#             auto_id,
#             prefix,
#             object_data,
#             error_class,
#             label_suffix,
#             empty_permitted,
#             use_required_attribute=use_required_attribute,
#             renderer=renderer,
#         )
#         for formfield in self.fields.values():
#             forms.models.apply_limit_choices_to_to_formfield(formfield)

#     def _get_validation_exclusions(self):
#         """
#         For backwards-compatibility, exclude several types of fields from model
#         validation. See tickets #12507, #12521, #12553.
#         """
#         exclude = set()
#         # Build up a list of fields that should be excluded from model field
#         # validation and unique checks.
#         for f in self.instance._meta.fields:
#             field = f.name
#             # Exclude fields that aren't on the form. The developer may be
#             # adding these values to the model after form validation.
#             if field not in self.fields:
#                 exclude.add(f.name)

#             # Don't perform model validation on fields that were defined
#             # manually on the form and excluded via the ModelForm's Meta
#             # class. See #12901.
#             elif self._meta.fields and field not in self._meta.fields:
#                 exclude.add(f.name)
#             elif self._meta.exclude and field in self._meta.exclude:
#                 exclude.add(f.name)

#             # Exclude fields that failed form validation. There's no need for
#             # the model fields to validate them as well.
#             elif field in self._errors:
#                 exclude.add(f.name)

#             # Exclude empty fields that are not required by the form, if the
#             # underlying model field is required. This keeps the model field
#             # from raising a required error. Note: don't exclude the field from
#             # validation if the model field allows blanks. If it does, the blank
#             # value may be included in a unique check, so cannot be excluded
#             # from validation.
#             else:
#                 form_field = self.fields[field]
#                 field_value = self.cleaned_data.get(field)
#                 if (
#                     not f.blank
#                     and not form_field.required
#                     and field_value in form_field.empty_values
#                 ):
#                     exclude.add(f.name)
#         return exclude

#     def clean(self):
#         self._validate_unique = True
#         return self.cleaned_data

#     def _update_errors(self, errors):
#         # Override any validation error messages defined at the model level
#         # with those defined at the form level.
#         opts = self._meta

#         # Allow the model generated by construct_instance() to raise
#         # ValidationError and have them handled in the same way as others.
#         if hasattr(errors, "error_dict"):
#             error_dict = errors.error_dict
#         else:
#             error_dict = {NON_FIELD_ERRORS: errors}

#         for field, messages in error_dict.items():
#             if (
#                 field == NON_FIELD_ERRORS
#                 and opts.error_messages
#                 and NON_FIELD_ERRORS in opts.error_messages
#             ):
#                 error_messages = opts.error_messages[NON_FIELD_ERRORS]
#             elif field in self.fields:
#                 error_messages = self.fields[field].error_messages
#             else:
#                 continue

#             for message in messages:
#                 if (
#                     isinstance(message, ValidationError)
#                     and message.code in error_messages
#                 ):
#                     message.message = error_messages[message.code]

#         self.add_error(None, errors)

#     def _post_clean(self):
#         opts = self._meta

#         exclude = self._get_validation_exclusions()

#         # Foreign Keys being used to represent inline relationships
#         # are excluded from basic field value validation. This is for two
#         # reasons: firstly, the value may not be supplied (#12507; the
#         # case of providing new values to the admin); secondly the
#         # object being referred to may not yet fully exist (#12749).
#         # However, these fields *must* be included in uniqueness checks,
#         # so this can't be part of _get_validation_exclusions().
#         for name, field in self.fields.items():
#             if isinstance(field, InlineForeignKeyField):
#                 exclude.add(name)

#         try:
#             self.instance = construct_instance(
#                 self, self.instance, opts.fields, opts.exclude
#             )
#         except ValidationError as e:
#             self._update_errors(e)

#         try:
#             self.instance.full_clean(exclude=exclude, validate_unique=False)
#         except ValidationError as e:
#             self._update_errors(e)

#         # Validate uniqueness if needed.
#         if self._validate_unique:
#             self.validate_unique()

#     def validate_unique(self):
#         """
#         Call the instance's validate_unique() method and update the form's
#         validation errors if any were raised.
#         """
#         exclude = self._get_validation_exclusions()
#         try:
#             self.instance.validate_unique(exclude=exclude)
#         except ValidationError as e:
#             self._update_errors(e)

#     def _save_m2m(self):
#         """
#         Save the many-to-many fields and generic relations for this form.
#         """
#         cleaned_data = self.cleaned_data
#         exclude = self._meta.exclude
#         fields = self._meta.fields
#         opts = self.instance._meta
#         # Note that for historical reasons we want to include also
#         # private_fields here. (GenericRelation was previously a fake
#         # m2m field).
#         for f in chain(opts.many_to_many, opts.private_fields):
#             if not hasattr(f, "save_form_data"):
#                 continue
#             if fields and f.name not in fields:
#                 continue
#             if exclude and f.name in exclude:
#                 continue
#             if f.name in cleaned_data:
#                 f.save_form_data(self.instance, cleaned_data[f.name])

#     def save(self, commit=True):
#         """
#         Save this form's self.instance object if commit=True. Otherwise, add
#         a save_m2m() method to the form which can be called after the instance
#         is saved manually at a later time. Return the model instance.
#         """
#         if self.errors:
#             raise ValueError(
#                 "The %s could not be %s because the data didn't validate."
#                 % (
#                     self.instance._meta.object_name,
#                     "created" if self.instance._state.adding else "changed",
#                 )
#             )
#         if commit:
#             # If committing, save the instance and the m2m data immediately.
#             self.instance.save()
#             self._save_m2m()
#         else:
#             # If not committing, add a method to the form to allow deferred
#             # saving of m2m data.
#             self.save_m2m = self._save_m2m
#         return self.instance

#     save.alters_data = True


# method 2
class BaseModelForm(CustomBaseForm, BaseForm):
    pass


class CustomizeModelForm(BaseModelForm, metaclass=forms.models.ModelFormMetaclass):
    pass