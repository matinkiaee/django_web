from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify
from django.urls import reverse



#MANAGER
class PublishedManager(models.Manager):
     def get_queryset(self):
          return super().get_queryset().filter(status=Post.Status.PUBLISHED)



# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
         DRAFT= "df","draft"
         PUBLISHED="pb","published"
         REJECTED="rj", "rejected"

    CATEGORY_CHOICES = (
          ('تکنولوژی', 'تکنولوی'),
          ('زبان برنامه نویسی', 'زبان برنامه نویسی'),
          ('هوش مصنوعی', 'هوش مصنوعی'),
          ('بلاکچین', 'بلاکچین'),
          ('سایر', 'سایر'),
      )
     #relations
     #معنی foreignkey=به معنی رابطه یک به چند است و به نوعی میگوید که به طور مثال هر پست میتواند چند نویسنده داشته باشد یا بلعکس 
    author= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts",verbose_name="نویسنده")
     # data field
    title= models.CharField(max_length=250,verbose_name="عنوان")
    description=models.TextField(verbose_name="توضیحات")
    slug=models.SlugField(max_length=250, verbose_name="اسلاگ")
    
    #date field

    publish=jmodels.jDateTimeField(default= timezone.now, verbose_name="تاریخ انتشار ")
    created=jmodels.jDateTimeField(auto_now_add=True)
    update= jmodels.jDateTimeField(auto_now=True)

     # choice field
    status=models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT,verbose_name="وضعیت")
    reading_time=models.IntegerField(verbose_name="زمان مطالعه",default=0)
    category = models.CharField( verbose_name="دسته بندی", max_length=20, choices=CATEGORY_CHOICES, default='سایر')


    objects= jmodels.jManager()
    published=PublishedManager()

    class Meta:
         ordering=["-publish"]
         indexes = [
              models.Index(fields=["-publish"])
         ]
         verbose_name="پست"
         verbose_name_plural="پست ها"

    def __str__(self):
         return self.title
    

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])
    


    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super().save(*args,**kwargs)


    def delete(self,*args,**kwargs):
        for img in self.image.all():
            storage,path=img.image_file.storage,img.image_file.path
            storage.delete(path)
        super().delete(*args,**kwargs)
    
    


class Ticket(models.Model):
    message= models.TextField(verbose_name="پیام")
    name= models.CharField(verbose_name="نام",max_length=250)
    email= models.EmailField(verbose_name="ایمیل")
    phone= models.CharField(max_length=11, verbose_name="تلفن")
    subject= models.CharField(max_length=250,verbose_name="موضوع")

    class Meta:
        
         verbose_name="تیکت"
         verbose_name_plural="تیکت ها"

    def __str__(self):
         return self.subject
    


class Comment(models.Model):
     post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments",verbose_name="پست")
     name= models.CharField(verbose_name="نام",max_length=250)
     body= models.TextField(verbose_name="متن کامنت",max_length=250)
     created= jmodels.jDateField(auto_now_add=True ,verbose_name="تاریخ ایجاد")
     updated= jmodels.jDateField(auto_now=True, verbose_name="تاریخ ویرایش")
     active= models.BooleanField(default=False, verbose_name="وضعیت")

     class Meta:
        ordering=["created"]
        indexes = [
              models.Index(fields=["created"])
         ]
        verbose_name="کامنت"
        verbose_name_plural="کامنت ها"

     def __str__(self):
        return f'{self.name}:{self.post}' 
     



class Image(models.Model):
     post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images",verbose_name="پست")
     image_file=ResizedImageField(upload_to="post_image/",quality=100, crop=["middle","center"], size=[600, 400])
     title= models.CharField(max_length=250,verbose_name="عنوان",null=True, blank=True)
     description=models.TextField(verbose_name="توضیحات",null=True, blank=True)
     created= jmodels.jDateField(auto_now_add=True ,verbose_name="تاریخ ایجاد")
     

     class Meta:
        ordering=["created"]
        indexes = [
              models.Index(fields=["created"])
         ]
        verbose_name="تصویر"
        verbose_name_plural="تصویر ها"


     def __str__(self):
        return self.title  if self.title else "None"
     



class Account(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد", blank=True, null=True)
    bio = models.TextField(verbose_name="بایو", null=True, blank=True)
    photo = ResizedImageField(verbose_name="تصویر", upload_to="account_images/", size=[500, 500], quality=60, crop=['middle', 'center'], blank=True, null=True)
    job = models.CharField(max_length=250, verbose_name="شغل", null=True, blank=True)

    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها" 




class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  


    def __str__(self):
        return self.name

     


