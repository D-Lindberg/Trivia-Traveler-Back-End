from django.contrib import admin
from .models import CustomUser, Country, Airport, Flight, Inventory, Item, UserFlights


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

class ItemAdmin(admin.ModelAdmin):
    model = Item

class CountryAdmin(admin.ModelAdmin):
    model = Country

class FlightAdmin(admin.ModelAdmin):
    model = Flight

class AirportAdmin(admin.ModelAdmin):
    model = Airport

class InventoryAdmin(admin.ModelAdmin):
    model = Inventory

class UserFlightsAdmin(admin.ModelAdmin):
    model = UserFlights


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Airport, AirportAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(UserFlights, UserFlightsAdmin)