from django.contrib import admin
from.models import CustomUser,UserProfile, Gallery, Enrollment, Trainer, MembershipPlan, VirtualFitnessClass

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Gallery)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(MembershipPlan)
admin.site.register(VirtualFitnessClass)

