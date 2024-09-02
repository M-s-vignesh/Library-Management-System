from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from . forms import Login,student_form
from . models import Student_details
from django.contrib import messages
from django.urls import reverse
from books.models import Books


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            st_id = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            ST_ID = Student_details.objects.all().filter(student_id = st_id,password=password)
            if ST_ID:
                global stu_id 
                stu_id = st_id
                global uname
                uname = Student_details.objects.get(student_id = st_id).name
                global url
                global sl 
                sl = Student_details.objects.get(student_id = st_id).slug
                url = Student_details.objects.get(student_id = st_id).get_absolute_url()
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.INFO, 'Invalid Student ID or Password')
                form = Login(request.POST)
                return render(request,'Users/login.html',{'form' : form})
        else:
            messages.add_message(request, messages.INFO, 'Invalid Student ID or Password')
            form = Login(request.POST)
            return render(request,'Users/login.html',{'form' : form})
    form = Login()
    return render(request,'Users/login.html',{'form' : form})

def register(request):
    if request.method == 'POST':
        form = student_form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            valid_email = Student_details.objects.filter(email = email).exists()
            if valid_email:
                context = {'form': form,'Errors':"Email"}
                return render(request,'Users/register.html',context)
            pwd = form.cleaned_data['password']
            cn_pwd = form.cleaned_data['confirm_password']
            if  pwd == cn_pwd:
                form.save()
                return HttpResponseRedirect('/')
            context = {'form': form,'Errors':"Password"}
            return render(request,'Users/register.html',context)
        else:
            v = list(form.errors.as_data())
            if v[0] == 'email':
                v = 'Email'
            else:
                v = 'Student Id'
            form = student_form(request.POST)
            context = {'form': form,'Errors':v}
            return render(request,'Users/register.html',context)
    form = student_form()
    return render(request,'Users/register.html',{'form':form})


def student_page(request,slug):
    return render(request,'Users/member.html',{"username" : uname,'sl':sl}) 

def st_books(request,slug):
    return render(request,'Users/search.html',{'username':uname,'url':url,'id':stu_id,'sl':sl})

def search_books(request,str):
    if str == 'Title':
        if request.method == 'POST':
            value = request.POST['search']
            values = Books.objects.filter(title__contains = value).values()
            if not values.exists():
                messages.add_message(request, messages.INFO, 'No Records Found For Book '+value)
            return render(request,'library/list_all_books.html',{'title': True,'username':uname,"url" : url,'details':values}) 
        return render(request,'library/list_all_books.html',{'title': True,'username':uname,"url" : url})
    elif str == 'Author':
        if request.method == 'POST':
            value = request.POST['search']
            values = Books.objects.filter(author__contains = value).values()
            if not values.exists():
                messages.add_message(request, messages.INFO, 'No Records Found For Author '+value)
            return render(request,'library/list_all_books.html',{'author': True,'username':uname,"url" : url,'details':values})
        return render(request,'library/list_all_books.html',{'author': True,'username':uname,"url" : url}) 
    elif str == 'Published-Date':
        if request.method == 'POST':
            value = request.POST['search']
            values = Books.objects.filter(published_date__gt = value).values()
            if not values.exists():
                messages.add_message(request, messages.INFO, 'No Records Found For Date '+value)
            return render(request,'library/list_all_books.html',{'date': True,'username':uname,"url" : url,'details':values})
        return render(request,'library/list_all_books.html',{'date': True,'username':uname,"url" : url}) 

def list_all_books(request):
    values = Books.objects.all().values()
    return render(request,'library/list_all_books.html',{"details": values,'username':uname,"url" : url})