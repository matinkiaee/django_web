from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import  Category





# Create your views here.
def index(request):
    last_post = Post.published.all().order_by('-publish')[0]
    return render(request, "blog/index.html", {"last_post": last_post})


    
def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
                       #view a posts in page   ,#number of post in the page
    paginator = Paginator(posts, 3)
                 #IF exist page is view,   #elif go to default mode(page=1) 
    page_number = request.GET.get('page', 1)
    try:
       # آن پیجی که در پیج نامبر ذخیره شده را به وسیله پگینیتور فراخوانی کن
        posts = paginator.page(page_number)
    except EmptyPage:
         #زمانی که استثنا رخ داد به وسیله پگینیتور اخرین صفحه را به نمایش بگذار
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    print(posts, type(posts))
    context = {
        'posts': posts,
        'category': category
    }
    return render(request, "blog/list.html", context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, "blog/detail.html", context)

def post_list_by_category(request, category):
    category = get_object_or_404(Category, slug=category)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/post_list.html', {'posts': posts})







    
def ticket(request):
      #منظور از پست در اینجا یعنی انتشار کردن یا گذاشتن
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
             #سی دی مخفف clean data
            cd = form.cleaned_data
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'],
                                  phone=cd['phone'], subject=cd['subject'])
            return redirect("blog:index")
    else:
        form = TicketForm()
    context={
          'form': form
        }
    return render(request, "forms/ticket.html",context )





def post_comment (request):
    #منظور از پست در اینجا یعنی انتشار کردن یا گذاشتن
    if request.method == "POST":
        comment_obj= Comment.objects.create()
        form = CommentForm(request.POST)
        if form.is_valid():
            #سی دی مخفف clean data
            cd= form.cleaned_data
            comment_obj.name=cd["name"]
            comment_obj.post=cd[Post]
            comment_obj.body=cd["body"]
            comment_obj.created=cd["created"]
            comment_obj.updated=cd["updated"]
            comment_obj.active=cd["active"]
            comment_obj.save()
            return redirect("blog:index")
        else:
            form= CommentForm()
            context={
                "form":form,
                "post":Post,
                "comment":Comment
            }
        return render (request, "forms/comment.html", context)
    

def post_search(request):
    query=None
    results=[]
    if "query" in request.GET:
        form= SearchForm(data=request.GET)
        if form.is_valid():
         query=form.cleaned_data["query"]
            #تعریف q object=این امورد باعث میشود که شما بتوانید همزمان چند فیلد را سرچ کنید
                                        #q object, field_lookup
         results=Post.published.filter(Q(title__search=query)|Q(description__search=query))

    context={
        "query":query,
        "results":results,
        
    }
    return render(request,"blog/search.html",context) 


@login_required
def profile(request):
    user=request.user
    posts=Post.published.filter(author=user)

    context={
       "posts":posts
    }

    return render(request,"blog/profile.html",context)


    
@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post= post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm()
    return render(request, 'forms/create_post.html', {'form': form})    



@login_required
def delete_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method=="POST":
        post.delete()
        return redirect("blog:profile")
    
    context={
        "post":post
    }
    return render(request,"delete_post.html",context)


def delete_image(request,image_id):
    post=get_object_or_404(Image,id=image_id)
    if request.method=="POST":
        Image.delete()
        return redirect("blog:profile")
    


@login_required
def edit_post(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method=="POST":
        
        form=CreatePostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            Image.objects.create(image_file=form.changed_data["image1"],post=post)
            Image.objects.create(image_file=form.changed_data["image2"],post=post)
            return redirect("blog:profile")
        else:
             form=CreatePostForm(instance=post)

        context={
            "form":form,
            "post":post
        }

        return render(request,"forms/create_post.html",context)
    



def user_login(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            cd=form.changed_data
            user=authenticate(request,username=cd["username"],password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse("you are now login")
                else:
                    return HttpResponse("your account is disabled")
            
            else:
                return HttpResponse("you are not login")
    else:
         form=LoginForm()
         context={
             "form":form
         }

    return render(request,"registration/login.html",context)


def log_out(request):
    logout(request)
    return redirect("blog:profile")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            context={
                'user': user
        }
            return  render(request, 'registration/register_done.html', context)
    else:
        form = UserRegisterForm()

    context={
        'form': form
    }
    return render(request, 'registration/register.html', context)


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = AccountEditForm(request.POST, instance=request.user.account, files=request.FILES)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    context ={
        'account_form': account_form,
        'user_form': user_form
    }
    return render(request, 'registration/edit_account.html', context)
        
        

        




    
 