from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Layout, Submit
from django import forms
from fuglelittbase.profiles.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "avatar",
        )

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.layout = Layout(
            Div(
                Field("first_name"),
                Field("last_name"),
                Field("avatar"),
                ButtonHolder(
                    Submit("submit", "save", css_class="btn btn-success"),
                    css_class="d-flex justify-content-end",
                ),
            )
        )
