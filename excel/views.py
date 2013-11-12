from django.views.generic.base import View
from django.contrib.contenttypes.models import ContentType

from .http import ExcelResponse, ExcelBookResponse

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

class Database(View):
    def get(self, request):
        book = []
        for objtype in ContentType.objects.all():
            model = objtype.model_class()
            if model.objects.count() > 0:
                book = book + [model.objects.all()]

        return ExcelBookResponse(book)
