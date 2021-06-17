from django import forms


class ExpressionForm(forms.Form):
    expression_field = forms.CharField()
