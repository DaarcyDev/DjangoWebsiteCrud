from django.forms import ModelForm
from .models import Task

class TaksForm(ModelForm):
    class Meta:
        model = Task
        fields =['title','description','important']