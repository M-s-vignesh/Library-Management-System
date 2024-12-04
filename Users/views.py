from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from . forms import Login,student_form,student_main_form
from . models import Student_details
from django.contrib import messages
from django.urls import reverse
# from books.models import Books
from . forms import Login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,logout,authenticate
from django.contrib.sessions.models import Session


User = get_user_model()

def log_out(request):
    logout(request)
    Session.objects.filter(session_key = request.session.session_key).delete()
    return HttpResponseRedirect('/')

def Username(request):
    return request.user.get_short_name()
  

def get_url(request):
    if request.user.is_authenticated:
        value = request.session.get('Emp_ID')
        if value:
            url = User.objects.get(Emp_ID = request.session['Emp_ID'])
            st_det = Student_details.objects.filter(user = url)
            if st_det:
                return st_det[0].get_absolute_url()
            return None
    logout(request)
    Session.objects.filter(session_key = request.session.session_key).delete()
    return HttpResponseRedirect('/')
# Create your views here.
def User_login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            st_id = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            student = User.objects.filter(Emp_ID=st_id)
            ##### check student or librarian id #####
            if student:
                details = Student_details.objects.filter(user = student[0])
                if details:
                    user = authenticate(request,Emp_ID=st_id,password=password)
                    if user:
                        if user.is_authenticated:
                            login(request,user)
                            request.session['Emp_ID'] = st_id
                            request.session.save()
                            url = get_url(request)
                            return HttpResponseRedirect(url)
                        else:
                            return HttpResponseRedirect('/')  
                    else:
                        messages.add_message(request, messages.INFO, 'Invalid Student ID or Password')
                        form = Login(request.POST)
                        return HttpResponseRedirect(reverse('login'))  
                else:
                    messages.add_message(request, messages.INFO, 'Invalid Student ID or Password')
                    form = Login(request.POST)
                    return HttpResponseRedirect(reverse('login'))  
            else:
                messages.add_message(request, messages.INFO, 'Invalid Student ID or Password')
                form = Login(request.POST)
                return HttpResponseRedirect(reverse('login'))  
        else:
            messages.add_message(request, messages.INFO, 'Invalid Student ID or Password')
            form = Login(request.POST)
            return HttpResponseRedirect(reverse('login'))  
    if request.user.is_authenticated:
        value = request.session.get('Emp_ID')
        if value:
            url = User.objects.get(Emp_ID = request.session['Emp_ID'])
            st_det = Student_details.objects.filter(user = url)
            if st_det:
                url = get_url(request)
                if url is not None:
                    return HttpResponseRedirect(url)
                else:
                    messages.add_message(request, messages.INFO, 'Invalid Student ID or Password')
                    form = Login(request.POST)
                    return HttpResponseRedirect(reverse('login'))  
            return HttpResponseRedirect(reverse('librarian_login'))
    form = Login()
    return render(request,'Users/login.html',{'form' : form})

def register(request):
    if request.method == 'POST':
        form = student_main_form(request.POST)
        form1 = student_form(request.POST)
        if form.is_valid():
            if form1.is_valid():
                pwd = form.cleaned_data['password']
                cn_pwd = form1.cleaned_data['confirm_password']
                st_id = form.cleaned_data['Emp_ID']
                if  pwd == cn_pwd: 
                    form = form.save(commit=False)
                    form.password = make_password(form.password)
                    form.save()
                    Form = User.objects.get(Emp_ID=st_id)
                    Form1 = form1.save(commit=False)
                    Form1.user = Form
                    Form1.save()
                    return HttpResponseRedirect('/')
                else:
                    form = student_main_form(request.POST)
                    form1 = student_form(request.POST)
                    return render(request,'Users/register.html',{'form':form,'form1':form1,'Errors':'Confirm Password'})
            else:
                form = student_main_form(request.POST)
                form1 = student_form(request.POST)
                return render(request,'Users/register.html',{'form':form,'form1':form1,'Errors':'Year'})
        else:
            form = student_main_form(request.POST)
            err = list(form.errors.as_data())
            error = None
            if err:
                if err[0] == 'email':
                    error = 'Email'
                else:
                    error = 'Student Id'
            form1 = student_form(request.POST)
            return render(request,'Users/register.html',{'form':form,'form1':form1,'Errors':error})
    form = student_main_form()
    form1 = student_form()
    return render(request,'Users/register.html',{'form':form,'form1':form1})


def student_page(request,slug):
    if request.user.is_authenticated:
        uname = Username(request)
        return render(request,'Users/member.html',{"username" : uname,}) 
    return HttpResponseRedirect('/')

# def st_books(request,slug):
#     return render(request,'Users/search.html',{'username':uname,'url':url,'id':stu_id,'sl':sl})

# def search_books(request,str):
#     if str == 'Title':
#         if request.method == 'POST':
#             value = request.POST['search']
#             values = Books.objects.filter(title__contains = value).values()
#             if not values.exists():
#                 messages.add_message(request, messages.INFO, 'No Records Found For Book '+value)
#             return render(request,'library/list_all_books.html',{'title': True,'username':uname,"url" : url,'details':values}) 
#         return render(request,'library/list_all_books.html',{'title': True,'username':uname,"url" : url})
#     elif str == 'Author':
#         if request.method == 'POST':
#             value = request.POST['search']
#             values = Books.objects.filter(author__contains = value).values()
#             if not values.exists():
#                 messages.add_message(request, messages.INFO, 'No Records Found For Author '+value)
#             return render(request,'library/list_all_books.html',{'author': True,'username':uname,"url" : url,'details':values})
#         return render(request,'library/list_all_books.html',{'author': True,'username':uname,"url" : url}) 
#     elif str == 'Published-Date':
#         if request.method == 'POST':
#             value = request.POST['search']
#             values = Books.objects.filter(published_date__gt = value).values()
#             if not values.exists():
#                 messages.add_message(request, messages.INFO, 'No Records Found For Date '+value)
#             return render(request,'library/list_all_books.html',{'date': True,'username':uname,"url" : url,'details':values})
#         return render(request,'library/list_all_books.html',{'date': True,'username':uname,"url" : url}) 

# def list_all_books(request):
#     values = Books.objects.all().values()
#     return render(request,'library/list_all_books.html',{"details": values,'username':uname,"url" : url})