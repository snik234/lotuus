from django.contrib import admin
from .models import Car, CarImage, ContactRequest, Favorite
from .models import Profile
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 3

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]
    list_display = ('title', 'owner', 'price', 'currency', 'created_at')

admin.site.register(ContactRequest)
admin.site.register(Favorite)
admin.site.register(Profile)