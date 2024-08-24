from blog.models import Image
from blog.models import Comment,Account
from django.contrib import admin
from .models import Post, Ticket
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin




# Register your models here.


admin.sites.AdminSite.site_header="پنل مدیریت جنگو"
admin.sites.AdminSite.site_title="پنل"
admin.sites.AdminSite.index_title="پنل مدیریت"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display=["author", "title","category",  "publish", "status"]
    ordering=[ "title", "publish"]
    list_filter=["status", "author", ("publish",JDateFieldListFilter)]
    search_fields=["title", "description"]
    list_editable=["status",]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display=["name", "subject", "phone"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=["post", "name", "created", "active"]
    list_filter=["active",("created",JDateFieldListFilter),("updated",JDateFieldListFilter),]
    search_fields=["name", "body"]
    list_editable=["active"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display=["post","created","title"]



@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display=["user","date_of_birth","bio","job","photo"]
    
