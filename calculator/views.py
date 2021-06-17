from django.shortcuts import render
from django.views import View
from calculator.forms import ExpressionForm
from django.views.generic.base import ContextMixin
import cexprtk


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'home.html')


class CalculatorView(ContextMixin, View):
    form_class = ExpressionForm

    def get(self, request, *args, **kwargs):
        context_kwargs = {'form': self.form_class}
        context = self.get_context_data(**context_kwargs)

        return render(self.request, 'calculator/calculator-form-page.html', context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)

        if not form.is_valid():
            return self.form_invalid(form)
        return self.form_valid(form)

    def form_valid(self, form):
        raw_expression = form.data['expression_field']

        try:
            computed_expression = cexprtk.evaluate_expression(raw_expression, {})
        except cexprtk.ParseException:
            form.add_error('expression_field', 'Invalid Expression')
            return self.form_invalid(form)

        context = {'result': computed_expression}
        return render(self.request, 'calculator/calculator-result-page.html', context)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, 'calculator/calculator-form-page.html', context)
