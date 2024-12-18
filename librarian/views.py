from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from . forms import Login,loan,Return,Delete_Book
from . models import Librarian_Profile,User
from django.contrib import messages
from django.urls import reverse
from books.forms import AddBook,AddBookCode
from books.models import Books,book_code,loaned_books
from django.db.models import F,Q,Subquery,OuterRef
from Users.models import Student_details
from dal import autocomplete
from django.contrib.auth import login,logout,authenticate
from django.contrib.sessions.models import Session
from django.contrib.auth.backends import BaseBackend
import itertools
from . forms import Login
# ############ Librarian Login ##########################
def log_out(request):
    logout(request)
    Session.objects.filter(session_key = request.session.session_key).delete()
    return HttpResponseRedirect('/')

def Username(request):
    if request.user.is_authenticated:
        return request.user.get_short_name()


def get_url(request):
    if request.user.is_authenticated:
        value = request.session.get('Emp_ID')
        if value:
            url = User.objects.get(Emp_ID = request.session['Emp_ID']).get_absolute_url()
            return url
    logout(request)
    Session.objects.filter(session_key = request.session.session_key).delete()
    return HttpResponseRedirect('/')


def librarian_login(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            st_id = form.cleaned_data['employee_id']
            password = form.cleaned_data['password']
            lib = User.objects.filter(Emp_ID=st_id)
            if lib:
                details = Librarian_Profile.objects.filter(user=lib[0])
                if details:
                    user = authenticate(request,Emp_ID=st_id,password=password)
                    if user:
                        if user.is_authenticated:
                            login(request,user)
                            request.session['Emp_ID'] = st_id
                            request.session.save()
                            return HttpResponseRedirect(get_url(request))
                        else:
                            return HttpResponseRedirect('/')
                    else:
                        messages.add_message(request, messages.INFO, 'Invalid Employee ID or Password')
                        form = Login(request.POST)
                        return HttpResponseRedirect(reverse('librarian_login'))
                else:
                    messages.add_message(request, messages.INFO, 'Invalid Employee ID or Password')
                    form = Login(request.POST)
                    return HttpResponseRedirect(reverse('librarian_login'))
            else:
                messages.add_message(request, messages.INFO, 'Invalid Employee ID or Password')
                form = Login(request.POST)
                return HttpResponseRedirect(reverse('librarian_login'))
        else:
            messages.add_message(request, messages.INFO, 'Invalid Employee ID or Password')
            form = Login(request.POST)
            return HttpResponseRedirect(reverse('librarian_login'))
    if request.user.is_authenticated:
        return HttpResponseRedirect(get_url(request))
    form = Login()
    return render(request,'library/login.html',{'form' : form})

# ############ Librarian Main Page ####################
def librarian_page(request,slug):
    if request.user.is_authenticated:
        return render(request,'library/library_page.html',{'username':Username(request),'url':get_url(request)})
    return HttpResponseRedirect('/')

# ################### search Books ######################
def search(request,slug):
    if request.user.is_authenticated:
        return render(request,'library/search.html',{'username':Username(request),"url" : get_url(request)})
    return HttpResponseRedirect('/')

# ############### Add Books To Database ################
def add_books(request,slug):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddBook(request.POST)
            if form.is_valid():
                book_name = form.cleaned_data['title']
                form.save()
                messages.add_message(request, messages.SUCCESS, book_name+' added Succesfully.')
                return HttpResponseRedirect(get_url(request)+'Add-Books')
            else:
                form = AddBook(request.POST)
                errors = form.errors.as_data()
                for key,value in errors.items():
                    err = list(value[0])[0]
                    if err == 'This field is required.':
                        err = key.replace('_',' ').capitalize()+' is required.'
                        messages.add_message(request, messages.ERROR, err)
                        return render(request,'library/add_books.html',{'form': form,'username':Username(request),"url" : get_url(request),})
                    else:
                        err = err.capitalize()
                        messages.add_message(request, messages.ERROR, err)
                        return render(request,'library/add_books.html',{'form': form,'username':Username(request),"url" : get_url(request),})
                messages.add_message(request, messages.ERROR, 'Book already Exists.')
                return render(request,'library/add_books.html',{'form': form,'username':Username(request),"url" : get_url(request),})
        form = AddBook()
        return render(request,'library/add_books.html',{'form': form,'username':Username(request),"url" : get_url(request)})
    return HttpResponseRedirect('/')

# ################ Add Codes for Books ########################
def add_book_codes(request,slug):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddBookCode(request.POST)
            if form.is_valid():
                book_name = form.cleaned_data['book']
                code = form.cleaned_data['code_no']
                code_values = book_code.objects.values_list('code_no',flat=True)
                if code not  in code_values:
                    book_code.objects.create(code_no = int(code),
                                            book = book_name)
                    Books.objects.filter(title=book_name).update(coded_books=F('coded_books') + 1)
                    messages.add_message(request, messages.SUCCESS,"Code - "+str(code)+" added to Book - "+str(book_name)+".")
                    return HttpResponseRedirect(get_url(request)+'Add-Book-Codes')
                form = AddBookCode(request.POST)
                messages.add_message(request, messages.ERROR, 'Code already mapped to a book, please select another code.')
                return render(request,'library/add_book_codes.html',{'form': form,'username':Username(request),"url" : get_url(request),})
            else:
                form = AddBookCode(request.POST)
                errors = form.errors.as_data()
                for key,value in errors.items():
                    err = list(value[0])[0]
                    if err == 'This field is required.':
                        err = key.replace('_',' ').capitalize()+' is required.'
                        messages.add_message(request, messages.ERROR, err)
                        return render(request,'library/add_book_codes.html',{'form': form,'username':Username(request),"url" : get_url(request),})
                    else:
                        err = err.capitalize()
                        messages.add_message(request, messages.ERROR, err)
                        return render(request,'library/add_book_codes.html',{'form': form,'username':Username(request),"url" : get_url(request),})
                messages.add_message(request, messages.ERROR, 'Code already mapped to a book, please select another code.')
                return render(request,'library/add_book_codes.html',{'form': form,'username':Username(request),"url" : get_url(request),})
        form = AddBookCode()
        return render(request,'library/add_book_codes.html',{'form':form,'username':Username(request),"url" : get_url(request),})
    return HttpResponseRedirect('/')

def listing(Model):
    values = []
    for i in Model:
        j = i.__dict__
        if i.studentname.all():
            i=i.studentname.all().values_list('user__Emp_ID')
            v = list(itertools.chain(*i))
            j["Studentname"] = ", ".join(list(map(str,v)))
        else:
            j["Studentname"] = "Nil"
        values.append(j)
    return values


# ################## List out all books #####################
def list_all_books(request,slug):
    if request.user.is_authenticated:
        j = Books.objects.all()
        values = listing(j)
        return render(request,'library/list_all_books.html',{"details": values,'username':Username(request),"url" : get_url(request),})
    return HttpResponseRedirect('/')

# #################### search books based on author,title or date ####################
def search_books(request,str):
    if request.user.is_authenticated:
        if str == 'Title':
            if request.method == 'POST':
                value = request.POST['search']
                model_value = Books.objects.filter(title__contains = value)
                if not model_value.exists():
                    messages.add_message(request, messages.ERROR, 'No Records Found For Book '+value)
                values = listing(model_value)
                return render(request,'library/list_all_books.html',{'title': True,'username':Username(request),"url" : get_url(request),'details':values})
            return render(request,'library/list_all_books.html',{'title': True,'username':Username(request),"url" : get_url(request)})
        elif str == 'Author':
            if request.method == 'POST':
                value = request.POST['search']
                model_value = Books.objects.filter(author__contains = value)
                if not model_value.exists():
                    messages.add_message(request, messages.ERROR, 'No Records Found For Author '+value)
                values = listing(model_value)
                return render(request,'library/list_all_books.html',{'author': True,'username':Username(request),"url" : get_url(request),'details':values})
            return render(request,'library/list_all_books.html',{'author': True,'username':Username(request),"url" : get_url(request)})
        elif str == 'Published-Date':
            if request.method == 'POST':
                value = request.POST['search']
                model_value = Books.objects.filter(published_date__gt = value)
                if not model_value.exists():
                    messages.add_message(request, messages.ERROR, 'No Records Found For Date '+value)
                values = listing(model_value)
                return render(request,'library/list_all_books.html',{'date': True,'username':Username(request),"url" : get_url(request),'details':values})
            return render(request,'library/list_all_books.html',{'date': True,'username':Username(request),"url" : get_url(request)})
    return HttpResponseRedirect('/')

# ##################### loan a book to student #########################
def loan_books(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = loan(request.POST)
            if form.is_valid():
                book_name = form.cleaned_data['book_title']
                code = form.cleaned_data['bookcode']
                stu_id = form.cleaned_data['student_id']
                if book_name.id == code.book_id:
                    student_id = User.objects.get(id = stu_id).Emp_ID
                    student_name = User.objects.filter(id = stu_id)[0].first_name
                    stu_exists = Student_details.objects.filter(user = stu_id)
                    if stu_exists.exists():
                        st_loaned_count = Books.objects.filter(studentname__id=stu_exists[0].id).count()
                        if st_loaned_count < 3:
                            bk_name = Books.objects.filter(id=book_name.id)[0].title
                            bk_codes = loaned_books.objects.filter(student_id = student_id)
                            if bk_codes:
                                for codes in bk_codes:
                                    bk_id = codes.student_book_code_id
                                    bk2_name = book_code.objects.get(id=bk_id).book
                                    if bk2_name.title == bk_name:
                                        form = loan()
                                        messages.add_message(request, messages.ERROR,'Student Id - '+str(student_id)+' already loaned '+bk_name+'.')
                                        return render(request,'library/loaned.html',{'form':form,'username':Username(request),"url" : get_url(request),})
                            map_book = Books.objects.filter(id=book_name.id)[0]
                            student = stu_exists[0]
                            map_book.studentname.add(student)
                            Books.objects.filter(id=book_name.id).update(current_copies = F('current_copies') - 1)
                            book_code.objects.filter(code_no = code.code_no).update(loaned = True)
                            loaned_books.objects.create(student_id = student_id,student_book_code_id = code.id)
                            messages.add_message(request, messages.SUCCESS,book_name.title+" loaned to "+student_name+"("+str(student_id)+") .")
                            return HttpResponseRedirect('Loan-Book')

                        else:
                            form = loan()
                            messages.add_message(request, messages.ERROR, 'Student Id - '+str(student_id)+' already loaned 3 books.Please return 1 book to loan this book.')
                            return render(request,'library/loaned.html',{'form':form,'username':Username(request),"url" : get_url(request),})
                    else:
                        form = loan()
                        messages.add_message(request, messages.ERROR, 'Student Id - '+str(student_id)+' doesn"t Exists. Please Enter correct Id.')
                        return render(request,'library/loaned.html',{'form':form,'username':Username(request),"url" : get_url(request),})
                form = loan()
                messages.add_message(request, messages.ERROR,"Please try again...!")
                return render(request,'library/loaned.html',{'form':form,'username':Username(request),"url" : get_url(request)})
            else:
                form = loan(request.POST)
                errors = form.errors.as_data()
                for key,value in errors.items():
                    err = list(value[0])[0]
                    if err == 'This field is required.':
                        err = key.replace('_',' ').capitalize()+' is required.'
                        messages.add_message(request, messages.ERROR, err)
                        return render(request,'library/loaned.html',{'form':form,'username':Username(request),"url" : get_url(request)})
                    else:
                        err = err.capitalize()
                        messages.add_message(request, messages.ERROR, err)
                        return render(request,'library/loaned.html',{'form':form,'username':Username(request),"url" : get_url(request)})
                messages.add_message(request, messages.ERROR,"Please try again...!")
                return render(request,'library/loaned.html',{'form':form,'username':Username(request),"url" : get_url(request)})
        else:
            form = loan()
            return render(request,'library/loaned.html',{'form':form,'username':Username(request),"url" : get_url(request)})
    return HttpResponseRedirect('/')

def return_book(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Return(request.POST)
            if form.is_valid():
                val = form.cleaned_data['student_ids']
                book_name = form.cleaned_data['book_title']
                book_id = Books.objects.get(title=book_name)
                if book_id:
                    loaned_book = book_code.objects.filter(book_id=book_id.id,loaned = True)
                    if loaned_book:
                        books_code = loaned_books.objects.filter(student_book_code_id__in=Subquery(loaned_book.values('id')),student_id=int(val))
                        if books_code:
                            book_code_id = books_code[0].student_book_code_id
                            loaned_id = books_code[0].id
                            st_val = User.objects.get(Emp_ID=val)
                            st_details = Student_details.objects.filter(user = st_val)[0]
                            if st_details:
                                ##removing manytomanyfield in database ##
                                book_id.studentname.remove(st_details)
                                ### updating loaned in book code model ###
                                book_code.objects.filter(id = book_code_id).update(loaned = False)
                                Books.objects.filter(id=book_id.id).update(current_copies = F('current_copies') + 1)
                                loaned_books.objects.filter(id = loaned_id)[0].delete()
                                messages.add_message(request, messages.SUCCESS,str(book_name)+" returned from "+st_val.get_short_name()+"("+str(val)+") to Library.")
                                return HttpResponseRedirect('Return-Book')
                form = Return()
                messages.add_message(request, messages.ERROR,"Please try again...!")
                return render(request,'library/return_book.html',{'form':form,'username':Username(request),"url" : get_url(request)})

            else:
                form = Return(request.POST)
                errors = form.errors.as_data()
                for key,value in errors.items():
                    err = list(value[0])[0]
                    if err == 'This field is required.':
                        err = key.replace('_',' ').capitalize()+' is required.'
                        messages.add_message(request, messages.ERROR, err)
                        return render(request,'library/return_book.html',{'form':form,'username':Username(request),"url" : get_url(request)})
                    else:
                        err = err.capitalize()
                        messages.add_message(request, messages.ERROR, err)
                        return render(request,'library/return_book.html',{'form':form,'username':Username(request),"url" : get_url(request)})
                messages.add_message(request, messages.ERROR,"Please try again...!")
                return render(request,'library/return_book.html',{'form':form,'username':Username(request),"url" : get_url(request)})
        form = Return()
        return render(request,'library/return_book.html',{'form':form,'username':Username(request),"url" : get_url(request)})
    return HttpResponseRedirect('/')

def list_students(request):
    if request.user.is_authenticated:
        student = Student_details.objects.all()
        result = []
        for i in student:
            details = i.__dict__
            if i.students.all():
                j = i.students.all().values_list('title')
                v = list(itertools.chain(*j))
                details['loaned_books'] = ','.join(v)
            else:
                details['loaned_books'] = 'No Books Loaned'
            details['student_id'] = i.user.Emp_ID
            details['email'] = i.user.email
            details['first_name'] = i.user.first_name
            details['last_name'] = i.user.last_name
            result.append(details)
        return render(request, 'library/list_students.html',{'username' : Username(request), 'url' : get_url(request), 'details' : result})
    return HttpResponseRedirect('/')

def delete_books(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Delete_Book(request.POST)
            if form.is_valid():
                book_title = form.cleaned_data['book_title']
                book_id = book_title.id
                value = book_code.objects.filter(loaned=True).values_list('book_id',)
                book_ids = list(itertools.chain(*value))
                if book_id not in book_ids:
                    messages.success(request, str(book_title)+' deleted.')
                    Books.objects.filter(id=book_id).delete()
                    form = Delete_Book()
                    return render(request, 'library/delete_books.html',{'username':Username(request),'url':get_url(request),'form':form})
                else:
                    messages.add_message(request, messages.ERROR, str(book_title)+" is loaned, cant be deleted !!")
                    form = Delete_Book()
                    return render(request, 'library/delete_books.html',{'username':Username(request),'url':get_url(request),'form':form})
            else:
                form = Delete_Book(request.POST)
                errors = form.errors.as_data()
                for key,value in errors.items():
                    err = list(value[0])[0]
                    if err == 'This field is required.':
                        err = key.replace('_',' ').capitalize()+' is required.'
                        messages.add_message(request, messages.ERROR, err)
                        return render(request, 'library/delete_books.html',{'username':Username(request),'url':get_url(request),'form':form})
                    else:
                        err = err.capitalize()
                        messages.add_message(request, messages.ERROR, err)
                        return render(request, 'library/delete_books.html',{'username':Username(request),'url':get_url(request),'form':form})
        form = Delete_Book()
        return render(request, 'library/delete_books.html',{'username':Username(request),'url':get_url(request),'form':form})
    return HttpResponseRedirect('/')

class ReturnBookAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = loaned_books.objects.all()
        stud_id= self.forwarded.get('student_ids', None)
        if stud_id:
            stud_id = Student_details.objects.filter(id = stud_id).values('user__Emp_ID')
            val = qs.filter(student_id=stud_id[0]['user__Emp_ID'])
            books_code = book_code.objects.filter(id__in=Subquery(val.values('student_book_code_id')))
            qs = Books.objects.filter(id__in=Subquery(books_code.values('book_id')))

        else:
            qs = None
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs

class BookAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Books.objects.filter(current_copies__gt = 0)
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs

class BookCodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = book_code.objects.all()
        book_title= self.forwarded.get('book_title', None)
        if book_title:
            qs = book_code.objects.filter(book_id = book_title, loaned = 0)

        else:
            qs = None
        if self.q:
            qs = qs.filter(code_no__istartswith=self.q)
        return qs

class StudentIdAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Student_details.objects.all()
        if self.q:
            qs = qs.filter(user__Emp_ID__istartswith=self.q)
        return qs

class BookTitleAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !

        qs = Books.objects.all()
        if self.q:
            qs = qs.filter(title__istartswith=self.q)
        return qs

