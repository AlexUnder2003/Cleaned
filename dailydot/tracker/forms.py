from django import forms

from tracker.models import Habit


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "invisible-input",
                    "placeholder": "Введите свою цель",
                }
            ),
        }
