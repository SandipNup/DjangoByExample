from django.contrib import admin
from .models import Post,Comment
# Register your models here.

# admin.site.register(Post)   #adds blog model to the adminstration site
@admin.register(Post)  #perform the same function as admin.site.register()
class PostAdmin(admin.ModelAdmin):
    list_display=('title','slug','author','publish','status')   #The list_display attribute allows you to set the fields of your model that you want to display in the admin object list page


class CommentAdmin(admin.ModelAdmin):
    list_display=('name','email','post','created','active') #adds the field to display in admin site
    list_filter=('active','created','updated') #add the filter by field in admin site
    search_fields=('name','email','body') #adds the search field in admin site

admin.site.register(Comment,CommentAdmin)
