from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import User, Trip  

# Register your models here.
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
	"""docstring for UserAdmin"DefaultUserAdminf __init__(self, arg):
 		super(UserAdmin,DefaultUserAdmin.__init__( )
		self.arg = arg """
	pass

@admin.register(Trip)	
class TripAdmin(admin.ModelAdmin):
	fields = (
		'id', 'pick_up_address', 'drop_off_address', 
		'status', 'created', 'updated',
		)
	list_display = (
		'id', 'pick_up_address', 'drop_off_address', 
		'status', 'created', 'updated',
		)
	list_filter = ('status',)
	readonly_fields = ('id', 'created', 'updated',)
