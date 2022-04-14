from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from games.models import GameTime, GameTimeInvitation

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

UserModel = get_user_model()


class SearchForm(forms.Form):
    term = forms.CharField(required=False)


class GameTimeForm(forms.ModelForm):
    class Meta:
        model = GameTime
        fields = ["start_time"]

    def __init__(self, *args, **kwargs):
        super(GameTimeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Create"))


class InviteeForm(forms.Form):
    email = forms.EmailField()

    _user = False

    def __init__(self, *args, **kwargs):
        super(InviteeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Invite"))

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            # cache for later
            self._user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise ValidationError(f"User with email address '{email}' was not found.")

        return email


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = GameTimeInvitation
        fields = ["is_attending"]

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields["is_attending"].label = "Attending?"
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Update Attendance"))
