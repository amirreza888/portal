from django import forms
from .models import Student
from django.utils.translation import gettext_lazy as _

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'id_num', 'field', 'number_of_unit', 'grade')
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'id_num': _('شماره ی دانشجویی'),
            'field': _('رشته'),
            'number_of_unit': _('تعداد واحد'),
            'grade': _(' مقطع تحصیلی')
        }
