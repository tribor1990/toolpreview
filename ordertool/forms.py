from django.forms import ModelForm
from .models import Userjob
from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput


#class Dtinput(forms.SplitDateTimeWidget):
 #   input_type = 'date'

class Newjobform(ModelForm):
    class Meta:
        model = Userjob
        
        fields = ['title', 'comment', 'important', 'deadlinedate', 'amountimages', 'id']
        widgets = {'deadlinedate' : DateTimePickerInput() 
        }