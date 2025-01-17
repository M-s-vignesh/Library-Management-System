from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from . forms import Login,student_form,student_main_form
from . models import Student_details
from django.contrib import messages
from django.urls import reverse
from books.models import Books
from . forms import Login,Update_Student_Details
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,logout,authenticate
from django.contrib.sessions.models import Session
from django.db.models import F,Q,Subquery,OuterRef
from librarian.forms import Reset_Password
from django.contrib.auth.hashers import(
                check_password,
                make_password,
                )
from django.utils.timezone import now

User = get_user_model()

def csrf_failure(request, reason=""):
    messages.error(request, "Your session has expired. Please log in again.")
    return HttpResponseRedirect('/')

def log_out_users(request):
    current_session_key = request.session.session_key

    # Get all active sessions
    active_sessions = Session.objects.filter(expire_date__gte=now())

    for session in active_sessions:
        session_data = session.get_decoded()
        # Check if the session belongs to a different user
        if session_data.get('_auth_user_id') and session.session_key != current_session_key:
            logged_in_user_id = session_data.get('_auth_user_id')
            
            try:
                # Fetch the user object for the active session
                logged_in_user = get_user_model().objects.get(id=logged_in_user_id)

                # Check if the logged-in user type is different
                if request.user.is_superuser != logged_in_user.is_superuser:
                    session.delete()  # Logout the other user
            except Exception as e:
                # Handle edge cases, e.g., user might have been deleted
                print(f"Error logging out user: {e}")


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
                return st_det[0].get_url()
            return None
    return log_out(request)

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
                            log_out(request)
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
            #return HttpResponseRedirect('/')
    if request.user.is_authenticated :
        if not request.user.is_superuser:
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
        else:
            log_out_users(request)
            form = Login()
            return render(request,'Users/login.html',{'form' : form})
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
                    messages.add_message(request, messages.SUCCESS,
                                          'Account Created. Please Login.')
                    form = student_main_form(request.POST)
                    form1 = student_form(request.POST)
                    context = {'form':form,'form1':form1,'success': True,}
                    return render(request,
                                   'Users/register.html', context)
                else:
                    messages.add_message(request, messages.ERROR,
                                          'Password Mismatch !!')
                    return render(request,'Users/register.html',
                                  {'form':form,'form1':form1,})
            else:
                errors = form1.errors.as_data()
                for key,value in errors.items():
                    err = list(value[0])[0]
                    if err == 'This field is required.':
                        err = key.replace('_',' ').capitalize()+' is required.'
                        messages.add_message(request, messages.ERROR, err)
                        context = {'form':form,'form1':form1,}
                        return render(request,
                                   'Users/register.html', context)
                    else:
                        err = err.capitalize()
                        if key == 'year':
                            err = 'Year Should be between 1 and 4'
                        messages.add_message(request, messages.ERROR, err)
                        context = {'form':form,'form1':form1,}
                        return render(request, 
                                  'Users/register.html', context)
        else:
            errors = form.errors.as_data()
            for key,value in errors.items():
                err = list(value[0])[0]
                if err == 'This field is required.':
                    if key == 'Emp_ID':
                        key = 'Student ID'
                    err = key.replace('_',' ').capitalize()+' is required.'
                    messages.add_message(request, messages.ERROR, err)
                    context = {'form':form,'form1':form1,}
                    return render(request,
                                   'Users/register.html', context)
                else:
                    err = err.capitalize()
                    if key == 'Emp_ID':
                        err = 'Student ID already exists !!'
                    messages.add_message(request, messages.ERROR, err)
                    context = {'form':form,'form1':form1,}
                    return render(request, 
                                  'Users/register.html', context)
    form = student_main_form()
    form1 = student_form()
    return render(request,'Users/register.html',
                  {'form':form,'form1':form1})


def student_page(request,slug):
    if request.user.is_authenticated :
        if not request.user.is_superuser:
            uname = Username(request)
            user_id = Student_details.objects.get(user=request.user)
            return render(request,'Users/member.html',
                        {"username" : uname, 
                            'url':get_url(request),
                            }) 
        else:
            log_out_users(request)
            return HttpResponseRedirect('/')
    return log_out(request)

def st_books(request,slug):
    if request.user.is_authenticated :
        if not request.user.is_superuser:
            uname = Username(request)
            user_id = Student_details.objects.get(user=request.user)
            return render(request,'Users/search.html',
                        {'username':uname,
                        'url':get_url(request),
                        })
        else:
            log_out_users(request)
            return HttpResponseRedirect('/')
    return log_out(request)

def search_books(request,slug,str):
    if request.user.is_authenticated :
        if not request.user.is_superuser:
            user_id = Student_details.objects.get(user=request.user)
            if str == 'Title':
                if request.method == 'POST':
                    value = request.POST['search']
                    values = Books.objects.filter(title__contains = value).values()
                    if not values.exists():
                        messages.add_message(request, messages.INFO, 'No Records Found For Book '+value)
                    return render(request,'Users/list_books.html',
                                {'title': True,
                                'username':Username(request),
                                "url" : get_url(request),
                                'details':values,
                                }) 
                return render(request,'Users/list_books.html',
                            {'title': True,
                            'username':Username(request),
                            "url" : get_url(request)})
            elif str == 'Author':
                if request.method == 'POST':
                    value = request.POST['search']
                    values = Books.objects.filter(author__contains = value).values()
                    if not values.exists():
                        messages.add_message(request, messages.INFO, 'No Records Found For Author '+value)
                    return render(request,'Users/list_books.html',
                                {'author': True,
                                'username':Username(request),
                                "url" : get_url(request),
                                'details':values})
                return render(request,'Users/list_books.html',
                            {'author': True,
                            'username':Username(request),
                            "url" : get_url(request)}) 
            elif str == 'Published-Date':
                if request.method == 'POST':
                    value = request.POST['search']
                    values = Books.objects.filter(published_date__gt = value).values()
                    if not values.exists():
                        messages.add_message(request, messages.INFO, 'No Records Found For Date '+value)
                    return render(request,'Users/list_books.html',
                                {'date': True,
                                'username':Username(request),
                                "url" : get_url(request),
                                'details':values})
                return render(request,'Users/list_books.html',
                            {'date': True,
                            'username':Username(request),
                            "url" : get_url(request)})
        else:
            log_out_users(request)
            return HttpResponseRedirect('/') 
    return log_out(request)

def list_all_books(request,slug):
    if request.user.is_authenticated :
        if not request.user.is_superuser:
            user_id = Student_details.objects.get(user=request.user)
            values = Books.objects.all().values()
            return render(request,'Users/list_books.html',
                                {'username':Username(request),
                                "url" : get_url(request),
                                'details':values,
                                })
        else:
            log_out_users(request)
            return HttpResponseRedirect('/')
    return log_out(request)

def loaned_books(request, slug):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            user_id = Student_details.objects.get(user=request.user)
            student = Student_details.objects.filter(user=request.user)
            loaned_books = student[0].students.all()
            if loaned_books:
                detail = Books.objects.filter(
                            id__in=Subquery(
                            loaned_books.values('id')))
                return render(request,'Users/loaned_books.html',
                                {'username':Username(request),
                                "url" : get_url(request),
                                'details' : loaned_books,
                                })
            messages.add_message(request,
                                messages.INFO, "You haven't loaned any books.")
            return HttpResponseRedirect(reverse('student_page',
                                        kwargs = {'slug':request.user.slug}))
        else:
            log_out_users(request)
            return HttpResponseRedirect('/')
    return log_out(request)


def student_profile(request, slug):
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            user_id = Student_details.objects.get(user=request.user)
            email = request.user.email
            studentid = request.user.Emp_ID
            department = Student_details.objects.get(
                            user=request.user).department
            year = Student_details.objects.get(
                            user=request.user).year
            
            context = {'email' : email,'department':department,'year':year,
                    'studentid':studentid,
                    'username':Username(request),'url':get_url(request)}
            return render(request,
                        'Users/profile.html',
                        context
                        )
        else:
            log_out_users(request)
            return HttpResponseRedirect('/')
    return log_out(request)


def update_student_profile(request,slug):
    """Function to update student details in db"""
    if request.user.is_authenticated:
        if not request.user.is_superuser:
            if request.method == 'POST':
                form = Update_Student_Details(request.POST)
                if form.is_valid():
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    user_id = request.user.id
                    email_exists = User.objects.filter(
                        email=email).exclude(
                            id=user_id).exists()
                    if email_exists:
                        messages.error(request, 'Email already taken.')
                        context = {'form':form, 'username':Username(request),
                                    'url':get_url(request)}
                        return render(request, 'Users/update.html', context)
                    User.objects.filter(id=user_id).update(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,

                    )
                    messages.success(request, 'Profile Updated')
                    return HttpResponseRedirect(reverse(
                        'update_student_profile',args=[request.user.Emp_ID])
                        )
                else:
                    errors = form.errors.as_data()
                    for key,value in errors.items():
                        err = list(value[0])[0]
                        if err == 'This field is required.':
                            err = key.replace('_',' ').capitalize()+' is required.'
                            messages.add_message(request, messages.ERROR, err)
                            form = Update_Student_Details(request.POST)
                            context = {'form':form, 'username':Username(request), 'url':get_url(request)}
                            return render(request, 'Users/update.html', context)
                        else:
                            err = err.capitalize()
                            messages.add_message(request, messages.ERROR, err)
                            form = Update_Student_Details(request.POST)
                            context = {'form':form, 'username':Username(request),
                                        'url':get_url(request)}
                            return render(request, 'Users/update.html', context)
                    return HttpResponseRedirect(reverse('update_student_profile',
                                                        args=[request.user.Emp_ID]))
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            data = {'first_name':first_name,
                        'last_name':last_name,
                        'email':email,
                        }
            form = Update_Student_Details(data)
            return render(request,
                        'Users/update.html',
                        {'username':Username(request),
                            'url' : get_url(request),
                            'form' : form,
                        })
        else:
            log_out_users(request)
            return HttpResponseRedirect('/')
    return log_out(request)

def reset_password(request, slug):
    """Function resets user password"""
    if request.user.is_authenticated :
        if  not request.user.is_superuser:
            if request.method == "POST":
                form = Reset_Password(request.POST)
                if form.is_valid():
                    old_password = form.cleaned_data['old_password']
                    new_password = form.cleaned_data['new_password']
                    confirm_password = form.cleaned_data['confirm_password']
                    old_pass = User.objects.get(
                                    id=request.user.id).password
                    if not check_password(old_password, old_pass):
                        messages.add_message(
                                            request, 
                                            messages.ERROR, 
                                            'Please Provide Correct Old Password')
                        return HttpResponseRedirect(reverse('student_reset_password',
                                                        args=[request.user.Emp_ID]))
                    if not new_password == confirm_password:
                        messages.add_message(
                                            request, 
                                            messages.ERROR, 
                                            'Password Mismatch !!')
                        return HttpResponseRedirect(reverse('student_reset_password',
                                                        args=[request.user.Emp_ID]))
                    hashed_password = make_password(new_password)
                    User.objects.filter(
                                    id=request.user.id).update(
                                        password=hashed_password
                                    )
                    return render(request, 'Users/reset_password.html', {
                        'success': True,  # This flag is used in the template to trigger SweetAlert
                        'username': Username(request),
                        'url': get_url(request),
                        'form': form,
                    })
                else:
                    errors = form.errors.as_data()
                    for key,value in errors.items():
                        err = list(value[0])[0]
                        if err == 'This field is required.':
                            err = key.replace('_',' ').capitalize()+' is required.'
                            messages.add_message(request, messages.ERROR, err)
                            context = {'form':form, 'username':Username(request),
                                        'url':get_url(request)}
                            return render(request, 'Users/reset_password.html', context)
                        else:
                            err = err.capitalize()
                            messages.add_message(request, messages.ERROR, err)
                            context = {'form':form, 'username':Username(request),
                                        'url':get_url(request)}
                            return render(request, 'Users/reset_password.html', context)
                    return HttpResponseRedirect(reverse('reset_password',
                                                        args=[request.user.Emp_ID]))
            form = Reset_Password()
            context = {'form':form, 'username':Username(request),
                        'url':get_url(request)}
            return render(request, 'Users/reset_password.html',context)
        else:
            log_out_users(request)
            return HttpResponseRedirect('/')
    return log_out(request)