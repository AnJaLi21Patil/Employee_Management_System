from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages

# ===================== In-Memory Data =====================
EMPLOYEES = []
EMPLOYEE_ID_COUNTER = 1  # To simulate auto-increment IDs

DEPARTMENTS = [{"id": 1, "name": "HR"}, {"id": 2, "name": "IT"}, {"id": 3, "name": "Finance"}]
ROLES = [{"id": 1, "name": "Manager"}, {"id": 2, "name": "Developer"}, {"id": 3, "name": "Analyst"}]

# ===================== AUTHENTICATION =====================
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Simulate registration
        messages.success(request, f"✅ User '{username}' registered (simulation).")
        return redirect("login")
    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            request.session["user"] = username
            messages.success(request, f"✅ Login successful. Welcome {username}!")
            return redirect("index")
        else:
            messages.error(request, "❌ Invalid username or password.")
    return render(request, "login.html")

def logout_user(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect("login")

# ===================== DASHBOARD =====================
def index(request):
    if "user" not in request.session:
        return redirect("login")
    return render(request, "index.html")

# ===================== EMPLOYEE CRUD =====================
def all_emp(request):
    if "user" not in request.session:
        return redirect("login")
    return render(request, "all_emp.html", {"emps": EMPLOYEES})

def add_emp(request):
    global EMPLOYEE_ID_COUNTER
    if "user" not in request.session:
        return redirect("login")

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        dept_id = int(request.POST.get("dept"))
        role_id = int(request.POST.get("role"))
        salary = float(request.POST.get("salary"))
        bonus = float(request.POST.get("bonus") or 0)
        phone = request.POST.get("phone")
        hire_date_str = request.POST.get("hire_date")
        hire_date = datetime.strptime(hire_date_str, "%Y-%m-%d").date() if hire_date_str else datetime.now().date()

        # Add employee to the in-memory list
        EMPLOYEES.append({
            "id": EMPLOYEE_ID_COUNTER,
            "first_name": first_name,
            "last_name": last_name,
            "dept": next((d["name"] for d in DEPARTMENTS if d["id"] == dept_id), ""),
            "role": next((r["name"] for r in ROLES if r["id"] == role_id), ""),
            "salary": salary,
            "bonus": bonus,
            "phone": phone,
            "hire_date": hire_date,
        })

        EMPLOYEE_ID_COUNTER += 1
        messages.success(request, "✅ Employee added successfully.")
        return redirect("all_emp")

    return render(request, "add_emp.html", {"departments": DEPARTMENTS, "roles": ROLES})

def remove_emp(request, emp_id):
    if "user" not in request.session:
        return redirect("login")

    global EMPLOYEES
    EMPLOYEES = [emp for emp in EMPLOYEES if emp["id"] != emp_id]
    messages.success(request, f"✅ Employee {emp_id} removed successfully.")
    return redirect("all_emp")

def filter_emp(request):
    if "user" not in request.session:
        return redirect("login")

    if request.method == "POST":
        search_name = request.POST.get("name", "").lower()
        filtered = [emp for emp in EMPLOYEES if search_name in emp["first_name"].lower() or search_name in emp["last_name"].lower()]
        return render(request, "all_emp.html", {"emps": filtered})

    return render(request, "filter_emp.html")
