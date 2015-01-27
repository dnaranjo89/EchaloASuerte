from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, HTML, Div

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


class RandomNumberDrawForm(forms.Form):
    range_min = forms.IntegerField(label=_("From"), initial=0, required=True)
    range_max = forms.IntegerField(label=_("To"), required=True)
    number_of_results = forms.IntegerField(label=_("Number of results"), required=True, initial=1, max_value=1000)
    allow_repeat = forms.BooleanField(label=_("Allow repetitions"), required=False)

    def __init__(self, *args, **kwargs):
        super(RandomNumberDrawForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.field_template = 'eas_crispy_field.html'
        self.helper.form_id = 'form-random_number'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-xs-7 text-right'
        self.helper.field_class = 'col-xs-4'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('random_number')
        self.helper.layout = Layout(
            Row(
                'range_min',
                'range_max',
                'number_of_results',
                'allow_repeat',
            ),
            HTML("{% include 'render_errors.html' %}"),
            Div(
                Submit('submit', _("Toss"), css_class='btn-toss'),
                css_class='text-center',
            )
        )

    def clean_number_of_results(self):
        if 0 < self.cleaned_data.get('number_of_results', 1) < 50:
            return self.cleaned_data.get('number_of_results', '')
        raise ValidationError(_("Between 1 and 50"))

    def clean(self):
        range_min = self.cleaned_data.get('range_min', 0)
        range_max = self.cleaned_data.get('range_max', 0)
        if range_min >= range_max:
            raise ValidationError(_("Range is too small"))

        if not self.cleaned_data.get('allow_repeat', False):
            if range_max - range_min < self.cleaned_data.get('number_of_results', 0):
                raise ValidationError(_("Range is too small, may be you want to allow repeated numbers?"))
        return self.cleaned_data