from django.forms import ModelForm
from store.models import Product
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'