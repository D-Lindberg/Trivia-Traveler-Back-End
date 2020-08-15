from django.forms import ModelForm
from .models import Item, Inventory, UserFlights

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'currency_modifier', 'duration',]


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ['user', 'item', 'turn_purchased', 'turns_remaining', 'status']


class UserFlightsForm(ModelForm):
    class Meta:
        model = UserFlights
        fields = ['user', 'flight', 'turn_count']