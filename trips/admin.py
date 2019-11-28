from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import User 

# Register your models here.
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
	"""docstring for UserAdmin"DefaultUserAdminf __init__(self, arg):
 		super(UserAdmin,DefaultUserAdmin.__init__( )
		self.arg = arg """
	pass
		
