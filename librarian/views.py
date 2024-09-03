from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from . forms import Login,loan
from . models import Librarian
from django.contrib import messages
from django.urls import reverse
from books.forms import AddBook,AddBookCode
from books.models import Books,book_code
from django.db.models import F,Q
from Users.models import Student_details


# Create your views here.

def librarian_login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            st_id = form.cleaned_data['employee_id']
            password = form.cleaned_data['password']
            ST_ID = Librarian.objects.all().filter(employee_id = st_id,password=password)
            if ST_ID:
                global uname
                uname = Librarian.objects.get(employee_id = st_id).name
                global emp_id
                emp_id = st_id
                global url
                url = Librarian.objects.get(employee_id = st_id).get_absolute_url()
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.INFO, 'Invalid Employee ID or Password')
                form = Login(request.POST)
                return render(request,'library/login.html',{'form' : form})
        else:
            messages.add_message(request, messages.INFO, 'Invalid Employee ID or Password')
            form = Login(request.POST)
            return render(request,'library/login.html',{'form' : form})
    form = Login()
    return render(request,'library/login.html',{'form' : form})

def librarian_page(request,slug):
    return render(request,'library/library_page.html',{'username':uname,"url" : url})

def search(request,slug):
    return render(request,'library/search.html',{'username':uname,"url" : url})

def add_books(request,slug):
    if request.method == "POST":
        form = AddBook(request.POST)
        if form.is_valid():
            book_name = form.cleaned_data['title']
            form.save()
            messages.add_message(request, messages.SUCCESS, book_name+' added Succesfully.')
            return HttpResponseRedirect(url+'Add-Books')
        else:
            form = AddBook(request.POST)
            return render(request,'library/add_books.html',{'form': form,'username':uname,"url" : url,'errors':'Book already Exists.'})
    form = AddBook()
    return render(request,'library/add_books.html',{'form': form,'username':uname,"url" : url})

def add_book_codes(request,slug):
    if request.method == "POST":
        form = AddBookCode(request.POST)
        if form.is_valid():
            book_name = form.cleaned_data['book']
            code = form.cleaned_data['code_no']
            form.save()
            Books.objects.filter(title=book_name).update(coded_books=F('coded_books') + 1)
            messages.add_message(request, messages.SUCCESS,"Code - "+str(code)+" added to Book - "+str(book_name)+" Succesfully.")
            return HttpResponseRedirect(url+'Add-Book-Codes')
        else:
            form = AddBookCode(request.POST)
            return render(request,'library/add_book_codes.html',{'form': form,'username':uname,"url" : url,'errors':'Code already mapped to a book, please select another code.'})
    form = AddBookCode()
    return render(request,'library/add_book_codes.html',{'form':form,'username':uname,"url" : url,'id':emp_id})

def list_all_books(request):
    values = Books.objects.all().values()
    return render(request,'library/list_all_books.html',{"details": values,'username':uname,"url" : url})

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

def loan_books(request):
    if request.method == 'POST':
      form = loan(request.POST)
      if form.is_valid():
          code = form.cleaned_data['bookcode']
          stu_id = form.cleaned_data['studentid']
          stu_exists = Student_details.objects.filter(student_id = stu_id).exists()
          if stu_exists:
            #book_code.objects.filter(code_no = code.code_no).update(loaned = True)
            return HttpResponse("ok")
          return HttpResponse("Student doesn't exists")
      else:
          print(form.errors.as_data())
          return HttpResponse(form.errors.as_data())
    else:
        form = loan()
        return render(request,'library/loaned.html',{'form':form,'username':uname,"url" : url}) 
def loadcodes(request):
    book_name = request.GET.get("book_title")
    values = book_code.objects.filter(book_id=book_name)
    return render(request,'library/codes.html',{'values':values})