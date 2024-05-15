from django.shortcuts import render
import json

from CG_International_University_App.models.student import StudentInformation
from CG_International_University_App.models.courses import Courses
from CG_International_University_App.models.admin_info import AdminInfo
from cgapp.models import MarkSheets
from django.views.decorators.csrf import csrf_protect


from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.conf import settings

import requests


@csrf_protect
def admin(request):
    print('---------------- Admin Function View ---------------- ')
    API_URL = settings.API_URL
    BASE_URL = settings.BASE_URL

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('login-type')
        
        api_url = f"{API_URL}login/"
        token_url = f"{API_URL}api/token/"

        token_payload = {"username": username, "password": password}
        token_response = requests.post(token_url, data=token_payload).json()
        access_token =token_response.get('access')
        print(access_token)

        payload = {"user_type": user_type, "username": username, "password": password,}
        print(payload)
        
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.post(api_url, headers=headers, data=payload)
        

        print(response.status_code)
        print(response.json())
        
        try:
            if response.status_code == 200:
                
                admin_dict = response.json()
                admin_info = AdminInfo.from_dict(admin_dict)
                return render(request, 'admin_cg_site/admin/admin.html', {
                    'is_logged_in': True,
                    'admin_info': admin_info,
                    'token': access_token,
                    'base_url': BASE_URL,
                    'api_url': API_URL,
                })

            elif response.status_code == 401:
                error_message = "Incorrect Password. Please try again."

            elif response.status_code == 400:
                error_message = "User not Found. Please try again."

            elif response.status_code == 404:
                error_message = "You're not Registered. Please contact the admin."

            elif response.status_code == 500:
                error_message = "Server Error. Please try again later."

            else:
                error_message = "An error occurred. Please try again later."

            return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return HttpResponse("Error: Internal Server Error.", status=500)

    else:
        return render(request, 'main_cg_site/auth/login.html')
    

# @csrf_protect
def editStudent(request):
    print('---------------- Edit Student Function View ---------------- ')
    

    API_URL = settings.API_URL
    BASE_URL = settings.BASE_URL

    try:
        student_id = request.GET.get('id')
        token = request.GET.get('token')

        student_url = f"{API_URL}students/{student_id}/"
        marksheet_url = f"{API_URL}marksheets/{student_id}/"
        student_data_url = f"{API_URL}student-data/{student_id}/"

        headers = {"Authorization": f"Bearer {token}"}

        student_response = requests.get(student_url, headers=headers)
        marksheet_response = requests.get(marksheet_url, headers=headers)
        student_data_response = requests.get(student_data_url, headers=headers)
        
        student_response.raise_for_status()
        marksheet_response.raise_for_status()
        student_data_response.raise_for_status()

        return render(request, 'admin_cg_site/admin/edit_student.html', {
            'student': student_response.json(),
            'student_data': student_data_response.json(),
            'marksheet_data': marksheet_response.json(),
            'is_logged_in': True,
            'base_url': BASE_URL,
            'api_url': API_URL
        })

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return HttpResponse("Error: Internal Server Error.", status=500)




def home(request):
    BASE_URL = settings.BASE_URL
    return render(request, 'main_cg_site/home/index.html', {'base_url': BASE_URL})


@csrf_protect
def student(request):
    print('---------------- Student Function View ---------------- ')
    API_URL = settings.API_URL
    BASE_URL = settings.BASE_URL

    if request.method == 'POST':
        enrollment_no = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('login-type')

        api_url = f"{API_URL}login/"
        token_url = f"{API_URL}token/"

        token_response = requests.get(token_url).json()
        access_token = token_response.get('access')
        print(access_token)
        
        payload = {"user_type": user_type, "username": enrollment_no, "password": password}
        print(payload)
        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.post(api_url, headers=headers, data=payload)
            response.raise_for_status()
            print(response.json())
            print(response.status_code)
            if response.status_code == 200:
                student_info_dict = response.json()
                student_info = StudentInformation.from_dict(student_info_dict)
                student_personal_info = student_info.student_info.student_personal_info
                student_marksheets = student_info.student_info.student_marksheets
                student_data = student_info.student_info.student_data

                return render(request, 'student_cg_site/home/student.html', {
                    'is_logged_in': True,
                    'token': access_token,
                    'student_info': student_personal_info,
                    'student_data': student_data,
                    'student_marksheets': student_marksheets,
                    'base_url': BASE_URL
                })

            elif response.status_code == 401:
                error_message = "Incorrect Password. Please try again."

            elif response.status_code == 400:
                error_message = "User not Found. Please try again."

            elif response.status_code == 404:
                error_message = "You're not Registered. Please contact the admin."

            elif response.status_code == 500:
                error_message = "Server Error. Please try again later."

            else:
                error_message = "An error occurred. Please try again later."

            return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return HttpResponse("Error: Internal Server Error.", status=500)

    else:
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

@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('login')