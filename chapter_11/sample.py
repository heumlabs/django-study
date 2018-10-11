# add to stores/views.py
from django.views.generic import ListView
from .models import Store
from core.views import TitleSearchMixin

class IceCreamStoreListView(TitleSearchMixin, ListView):
    model = Store