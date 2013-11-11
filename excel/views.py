from django.views.generic.base import View

from .http import ExcelResponse

class Download(View):
    objs = []

    def get(self, request):
        return ExcelResponse(self.objs)

class Model(Download):
    model = None

    def dispatch(self, *args, **kwargs):
        if self.kwargs['model']:
            self.model = self.kwargs['model']

        self.objs = self.model.objects.all()
        super(Model, self).dispatch(*args, **kwargs)
