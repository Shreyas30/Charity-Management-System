from django.contrib import admin

# Register your models here.
from .models import CharityUser,Donor,Contact

admin.site.register(CharityUser)
admin.site.register(Donor)
admin.site.register(Contact)