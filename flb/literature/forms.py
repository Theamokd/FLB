from crispy_forms.bootstrap import FieldWithButtons, FormActions, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Fieldset, Layout, Row, Submit
from django import forms
from django.urls.base import reverse_lazy
from django_select2 import forms as s2forms
from fuglelittbase.literature.models import Article, Author, Issue, Journal

from .custom_layout_object import Formset


class AuthorWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            "first_name",
            "last_name",
            "org",
        )

    # Define the layout using crispy forms formHelper
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("first_name"),
            Field("last_name"),
            Field("org"),
            Submit("submit", "Submit", css_class="btn, btn-success"),
        )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("name", "abstract", "text", "file", "link", "authors", "tags")

        widgets = {
            "abstract": forms.Textarea(attrs={"rows": 2}),
            "authors": AuthorWidget,
        }
        # Setting the link for add another
        labels = {
            "authors": 'The authors <a href="#" id="add-author"><i>(Add another)<i/></a>',
        }

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-2 create-label'
        # self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            Div(
                Div(Field("name"), css_class="col-md-6"),
                Div(Field("authors"), css_class="col-md-6"),
                Div(Field("abstract"), css_class="col-md-12"),
                Div(Field("file"), css_class="col-md-12"),
                Div(Field("text"), css_class="col-md-12"),
                Div(
                    Fieldset("Add images", Formset("inline_formset")),
                    css_class="col-md-12 mb-3 border p-2",
                ),
                Div(Field("link"), css_class="col-md-12"),
                Div(Field("tags"), css_class="col-md-12"),
                Div(
                    FormActions(Submit("submit", "save", css_class="btn btn-success")),
                    css_class="col-md-12 d-flex justify-content-end",
                ),
                css_class="row",
            ),
        )


# Widget for date input
class DateInput(forms.DateInput):
    input_type = "date"


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = (
            "name",
            "volume",
            "date",
            "issn",
            "file",
            "desc",
            "link",
            "f_cover",
            "b_cover",
            "redactor",
            "journal",
        )

        widgets = {
            "date": DateInput,
        }

    # Define the layout using crispy forms formHelper
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")  # Must be before calling super
        super().__init__(*args, **kwargs)

        # Filtering the journals by editor
        editors_journals = Journal.objects.filter(editors=self.user)
        self.fields["journal"].queryset = editors_journals

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name"),
                Column("volume"),
                Column("date"),
            ),
            Row(
                Column("file"),
                Column("f_cover"),
                Column("b_cover"),
            ),
            Row(
                Column("issn"),
                Column("link"),
            ),
            Row(
                Column("redactor"),
                Column("journal"),
            ),
            Row(
                Column("desc"),
            ),
            Submit("submit", "Submit", css_class="btn, btn-success"),
            Submit("submit", "Cancel", css_class="btn, btn-warning"),
        )


class MainSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.form_style = "inline"
        self.helper.form_show_labels = False
        self.helper.form_action = reverse_lazy("literature:search")
        self.helper.layout = Layout(
            Div(
                FieldWithButtons(
                    Field(
                        "q",
                        placeholder="Search for keywords in tags, titles, authors and abstracts",
                    ),
                    StrictButton("Search", type="submit", css_class="btn btn-success"),
                ),
                css_class="mt-3",
            )
        )
