from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from main_app.app_forms import Employee_form, LoginForm
from main_app.models import Employee
from main_app.users import people




# Create your views here.
def home_page(request):
    # name = "Ali Wangara"
    # age = 18
    #
    # data = {
    #     "Name": name,
    #     "Age": age
    #
    # }
    return render(request, "index.html", )


# def data(request):
#     name = "Wangara"
#     age = 21
#     users = people
#
#     data = {
#         "name" : name,
#         "age" : age,
#         "users":people
#     }
#
#     return render(request, "data.html" , context=data)
def about(request):
    return render(request, "about.html")

@login_required
def donate(request):
    return render(request, "charity.html")


def contact(request):
    return render(request, "contact.html")

@login_required
@permission_required('main_app.add_employee', raise_exception=True)
def team(request):
    if request.method == "POST":
        form = Employee_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, "Added successfully")
            return redirect("home")

    else:
        form = Employee_form()
    return render(request, 'employee.html', {"form": form})


# All employees
# one employee


def employee(request):
    employees = Employee.objects.all()
    # employees = Employee.objects.all().order_by("-salary")
    # employees = Employee.objects.filter(name__istartswith= "Al", salary__gt = 45000).order_by("dob")
    # employees = Employee.objects.filter(Q(name__contains="Al") | Q(salary__gt = 70000))
    # today = datetime.today()
    # day = today.day
    # month = today.month
    # employees = Employee.objects.filter(dob__day=day, dob__month= month)
    paginator = Paginator(employees, 30)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    return render(request, "all_employees.html", {"employees": data})


def employee_details(request, emp_id):
    employee = Employee.objects.get(pk=emp_id)  # SELECT * FROM employees
    return render(request, 'employee_details.html', {"employee": employee})

@login_required
@permission_required('main_app.delete_employee')
def employee_delete(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)
    employee.delete()
    messages.warning(request, 'Deleted successfully')
    return redirect("all")

@login_required
@permission_required('main_app.view_employee')
def search_employees(request):
    search_word = request.GET["search_word"]
    employees = Employee.objects.filter(Q(name__icontains=search_word) | Q(email__icontains=search_word)
                                        )
    paginator = Paginator(employees, 30)
    page_number = request.GET.get("page")
    data = paginator.get_page(page_number)
    # Elastic search
    return render(request, "all_employees.html", {"employees": data})

@login_required
@permission_required('main_app.change_employee')
def employee_update(request, emp_id):
    employee = get_object_or_404(Employee, pk=emp_id)  # SELECT *FROM employees WHERE id = 1
    if request.method == "POST":
        form = Employee_form(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "updated successfully")
            return redirect('details', emp_id)
    else:
        form = Employee_form(instance=employee)

    return render(request, 'update.html', {'form': form})


def signin(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data['password']
            user = authenticate(request, username = username,  password =password)
            if user:
                login(request, user)

                return redirect('home')
        messages.error(request, "Wrong username or password")
        return render(request, "login.html", {"form":form})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

# TODO add one to one again