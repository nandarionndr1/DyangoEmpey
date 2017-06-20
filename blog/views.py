from django.shortcuts import render, redirect
from .forms import AuthorForm, SignUpForm, PostForm,ImageUploadForm
from .models import Author, Post, Comment
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q

from django.utils.timezone import localtime, now


def signout(request):
    logout(request)
    return redirect('index')


def newPost(request):
    form = PostForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            Post.objects.create(author=Author.objects.get(username=request.user.username), date=localtime(now()),
                                title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            return redirect('home')
        else:
            form = PostForm()

    return render(request,  'blog/newPost.html', {'form': form,'guest': request.session['guest']})


def details(request, Post_id):

    post = Post.objects.get(id=Post_id)
    if request.method == "POST":

            comment = Comment(author=Author.objects.get(username=request.user.username), post=post,
                               cdate=localtime(now()), content=request.POST['commentz'])
            comment.save()
            print(request.POST['commentz'])


    return render(request, 'blog/postDet.html', {'post':post, 'guest': request.session['guest'], 'comment': Comment.objects.filter(post = post),'user': Author.objects.get(username=request.user.username) })

def index(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = Author(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
            author.save()
            redirect('index')
    else:
        form = AuthorForm()
    return render(request, 'blog/index.html', {'AuthorForm': form})


def req(request, onsuccess='/blog/home/', onfail='/blog/login/'):
    try:
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
    except:
        None

    form = AuthorForm(request.POST)
    post = Post.objects.all()
    if request.method =='GET':
        user = authenticate(username='guest', password='gu3stus3r')
        login(request, user)
        request.session['guest'] = False
        request.session['logged'] = True
        return render(request, 'blog/home.html',{'guest': request.session['guest'], 'check': False, 'posts': Post.objects.all(), 'comments': Comment.objects.all()})
    elif user is not None and request.method=='POST':
        request.session['username'] = user.username
        request.session['guest'] = True
        request.session['logged'] = True
        login(request, user)
        return render(request, 'blog/home.html', {'guest': request.session['guest'], 'check': False, 'posts': Post.objects.all(), 'comments': Comment.objects.all()})
    else:
        return render(request, 'blog/index.html', {'check': True})


def post(request):
    post = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': Post.objects.all(),'guest': request.session['guest'] })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password, first_name=first_name, last_name=last_name,
                                email=email)
            author = Author(username=username, first_name=first_name, last_name=last_name)
            author.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

def shows(request):
    if request.method == 'POST':
        show= True
    return render(request, 'blog/home.html',{'posts': Post.objects.all(), 'guest': request.session['guest'] , 'comments': Comment.objects.all(),'show': True})

def updates(request, Post_id):
        post = Post.objects.get(id=Post_id)
        if (Post is not None and post.author == Author.objects.get(username=request.user.username)):
            print('bobo ka')
            return render(request,'blog/postUpdate.html',  {'user': Author.objects.get(username=request.session['username']), 'guest': request.session['guest'], 'post': post})
        else:
            redirect('home')
def updatefin(request, Post_id):

    post = Post.objects.get(id=Post_id)
    if (Post is not None and post.author == Author.objects.get(username=request.user.username)):
        if request.method == 'POST':
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.save()
            redirect('home')
    return redirect('home')

def delete(request, Post_id):
    post = Post.objects.get(id=Post_id)
    if (Post is not None and post.author == Author.objects.get(username=request.user.username)):
        post.delete()
    return redirect('home')
def search(request):

    try:

        q = request.POST['q']
        posts = Post.objects.filter(title__contains=q) | \
                Post.objects.filter(author__first_name__contains=q) | \
                Post.objects.filter(author__last_name__contains=q) | \
                Post.objects.filter(content__contains=q)

    except:
        None
    return render(request, 'blog/results.html', {'posts': posts, 'q': q, 'comments': Comment})

def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        m = Author.objects.get(Author.username)
        m.avatar = request.POST['image']
        m.save()
        return redirect('home')
    return redirect('home')
def myPosts(request):
    post = Post.objects.all()
    author = Author.objects.get(username=request.user.username)
    return render(request, 'blog/myPosts.html', {'posts': post ,'guest': request.session['guest'] , 'comments': Comment,'author':author})
def home(request):
    post = Post.objects.all()
    author = Author.objects.get(username=request.user.username)
    if request.method == 'POST':
        try:
            if (request.POST['Author'] == 'Author'):
                post = Post.objects.filter().order_by('-author__last_name')
        except:
            None
        try:
            if (request.POST['DateCreate'] == 'DateCreate'):
                post = Post.objects.filter().order_by('-date')
        except:
            None
        try:
            if (request.POST['Title'] == 'Title'):
                post = Post.objects.filter().order_by('-title')
        except:
            None

    return render(request , 'blog/home.html',{'posts': post,  'guest': request.session['guest'],'comments':Comment, 'author': author})

# Create your views here.
