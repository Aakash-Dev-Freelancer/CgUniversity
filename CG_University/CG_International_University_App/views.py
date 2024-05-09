from django.shortcuts import render
import json

# from .models import Courses
from CG_International_University_App.models.student import StudentInformation
from CG_International_University_App.models.courses import Courses
from CG_International_University_App.models.admin_info import AdminInfo
# from django.core.serializers import serialize

# from cgapp.models import Student, StudentData, MarkSheets
# from cgapp.serializers import StudentSerializer,MarkSheetSerializer,StudentDataSerializer



from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.conf import settings


import requests
# Home Page --------------------->



def admin(request):
    server = settings.SERVER_URL
    local = settings.LOCAL_HOST
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('login-type')

        print("Api Hit")
        api_url = f"{local}cg_api/login/"
        payload = {"user_type": user_type, "username": username, "password": password}

        
        response = requests.post(api_url, data=payload)
        print(response.json())
        # print(response.json())
        json_encoded = json.dumps(response.json())

            
        try:
            if response.status_code == 200:
                    admin_dict = response.json()
                    admin_info = AdminInfo.from_dict(admin_dict)
                    
                    return render(request, 'admin_cg_site/admin/admin.html', {
                        'is_logged_in': True,
                        'admin_info': admin_info,
                    })
                
            elif response.status_code == 401:
                error_message = "Incorrect Password. Please try again."
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
            
            elif response.status_code == 400:
                error_message = "User not Found. Please try again."

                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
            
            elif response.status_code == 404:
                error_message = "Your not Registered. Please Contact to admin."
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
            
            elif response.status_code == 500:
                error_message = "Server Error. Please try again later."
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
                
            
            else:
                error_message = "An error occurred. Please try again later."
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
        
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return HttpResponse("Error: Internal Server Error.", status=500)

    else:
        # Handle GET requests to the page
        return render(request, 'main_cg_site/auth/login.html')
    

def editStudent(request):
    server = settings.SERVER_URL
    local = settings.LOCAL_HOST


    try:
        # Get the ID from the request
        id = request.GET.get('id')
        student_url = f"{local}cg_api/students/{id}/"
        marksheet_url = f"{local}cg_api/marksheets/{id}/"
        student_data_url = f"{local}cg_api/student-data/{id}/"


        student = requests.get(student_url)
        marksheet_data = requests.get(marksheet_url)
        student_data = requests.get(student_data_url)
        print(student.json())
        print(marksheet_data.json())
        print(student_data.json)

        student.raise_for_status()
        marksheet_data.raise_for_status()
        student_data.raise_for_status()

        return render(request, 'admin_cg_site/admin/edit_student.html', {
            'student': student.json(),
            'student_data': student_data.json(),
            'marksheet_data': marksheet_data.json(),
        })
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")




def home(request):
    return render(request, 'main_cg_site/home/index.html',)




def student(request):
    server = settings.SERVER_URL
    local = settings.LOCAL_HOST


    if request.method == 'POST':
        enrollment_no = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('login-type')

        print("Api Hit")
        api_url = f"{local}cg_api/login/"
        payload = {"user_type": user_type, "username": enrollment_no, "password": password}
        
        response = requests.post(api_url, data=payload)
        # json_encoded = json.dumps(response.json())
        # print(json_encoded)

        try:
            if response.status_code == 200:
                    student_info_dict = response.json()
                    student_info = StudentInformation.from_dict(student_info_dict)
                    student_personal_info = student_info.student_info.student_personal_info
                    student_marksheets = student_info.student_info.student_marksheets
                    student_data = student_info.student_info.student_data

                    return render(request, 'student_cg_site/home/student.html', {'is_logged_in': True,'student_info': student_personal_info, 'student_data': student_data,'student_marksheets':student_marksheets})
                
                
                # Admin
            elif response.status_code == 401:
                error_message = "Incorrect Password. Please try again."
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
            
            elif response.status_code == 400:
                error_message = "User not Found. Please try again."

                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
            
            elif response.status_code == 404:
                error_message = "Your not Registered. Please Contact to admin."
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
            
            elif response.status_code == 500:
                error_message = "Server Error. Please try again later."
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
                
            
            else:
                error_message = "An error occurred. Please try again later."
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
        
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return HttpResponse("Error: Internal Server Error.", status=500)

    else:
        # Handle GET requests to the page
        return render(request, 'main_cg_site/auth/login.html')


# Login Page --------------------->
def login(request):
    return render(request, 'main_cg_site/auth/login.html')

# Register Page --------------------->


# About Us -------------------------->
def about(request):
    return render(request, 'main_cg_site/about_us/about.html',)


# Director Message -------------------------->
def directorMessage(request):
    return render(request, 'main_cg_site/about_us/director_message.html',)

# Vision And Mission -------------------------->


def visionAndMission(request):
    return render(request, 'main_cg_site/about_us/vision_and_mission.html',)

# Courses--------------------->


def courses(request):
    branch_objects = Courses.objects.all()
    branches_list = []  # List to hold each branch's information
    for branch in branch_objects:
        branch_info = {
            'title': branch.title,
            'description': branch.description,
            'courses': branch.courses.split(","),
        }
        branches_list.append(branch_info)
    return render(request, 'main_cg_site/courses/courses.html', {'branches': branches_list})


# Board_Member's------------------>


def boardMembers(request):
    return render(request, 'main_cg_site/board_members/board_members.html')
# Important-------------------->


def termsAndconditions(request):
    return render(request, 'main_cg_site/important/terms_and_conditions.html')


def rti(request):
    return render(request, 'main_cg_site/important/rti.html')
# Approval--------------->


def approval(request):
    return render(request, 'main_cg_site/approval/approval.html')

# Contact--------------->


def contact(request):
    return render(request, 'main_cg_site/contact/contact.html')


def logout_view(request):
    print("------------------------------------")
    logout(request)
    return redirect('login')