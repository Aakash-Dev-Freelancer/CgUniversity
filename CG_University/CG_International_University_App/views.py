from django.shortcuts import render
import json

from CG_International_University_App.models.student import StudentInformation
from CG_International_University_App.models.courses import Courses
from CG_International_University_App.models.admin_info import AdminInfo
from cgapp.models import MarkSheets, Center, Student, StudentData
from cgapp.serializers import MarkSheetSerializer, StudentSerializer, StudentDataSerializer
from django.views.decorators.csrf import csrf_protect


from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.conf import settings

import requests
import logging

from django.http import JsonResponse
# New Changes

@csrf_protect
def admin(request):
    print('---------------- Admin Function View ---------------- ')
    API_URL = settings.API_URL

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('login-type')
        
        api_url = f"{API_URL}login/"
        token_url = f"{API_URL}token/"

        token_payload = {"username": username, "password": password, "user_type": user_type}
        print("Token Payload :: ", token_payload)
        token_response = requests.get(token_url, data=token_payload)
        token_json = token_response.json()
        access_token = token_json.get('access')
        print("Access Token :: ", access_token)
        csrf_token = request.POST.get('csrfmiddlewaretoken')

        payload = {"user_type": user_type, "username": username, "password": password, 'X-CSRFToken': csrf_token}
        
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.post(api_url, headers=headers, data=payload)
        
        
        try:
            if response.status_code == 200:
                admin_dict = response.json()
                admin_info = AdminInfo.from_dict(admin_dict)
                return render(request, 'admin_cg_site/admin/admin.html', {
                    'is_logged_in': True,
                    'admin_info': admin_info,
                    'token': access_token,
                    'base_url': settings.BASE_URL,
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

            return render(request, 'main_cg_site/auth/login.html',{'error_message': error_message})

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            error_message = "An error occurred. Please try again later."
            return render(request, 'main_cg_site/auth/login.html',{'error_message': error_message})

    else:
        error_message = "Invalid request. Please try again."
        return render(request, 'main_cg_site/auth/login.html',{'error_message': error_message})

    

@csrf_protect
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
        print(student_response.json())
        
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
        error_message = "An error occurred. Please try again later."
        return render(request, 'admin_cg_site/admin/edit_student.html', {'error_message': error_message})
    
    
@csrf_protect
def viewStudent(request):
    print('---------------- View Student Function View ---------------- ')
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
        print(student_response.json())
        
        student_response.raise_for_status()

        return render(request, 'center_cg_site/templates/view_student.html', {
            'student': student_response.json(),
            'is_logged_in': True,
            'base_url': BASE_URL,
            'api_url': API_URL
        })

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        error_message = "An error occurred. Please try again later."
        return render(request, 'center_cg_site/tamplates/view_student.html', {'error_message': error_message})


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
        csrf_token = request.POST.get('csrfmiddlewaretoken')

        api_url = f"{API_URL}login/"
        token_url = f"{API_URL}token/"
        
        print("Enrollment No :: ", enrollment_no)
        print("Password :: ", password)
        print("User Type :: ", user_type)
        print("API URl :: ", api_url)
        print("Token URL :: ", token_url)

        try:
            payload = {"user_type": user_type, "username": enrollment_no, "password": password,}
            token_response = requests.get(token_url, data=payload)
            token_response.raise_for_status()
            token_json = token_response.json()
            access_token = token_json.get('access')
            print("Access Token :: ", access_token)
            
            print("Payload :: ", payload)
            headers = {"Authorization": f"Bearer {access_token}", "X-CSRFToken": csrf_token}

            response = requests.post(api_url, headers=headers, data=payload)
            print("Response :: ", response)
            print("Status Code :: ", response.status_code)

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
                    'base_url': BASE_URL,
                })
            else:
                error_message = {
                    401: "Incorrect Password. Please try again.",
                    400: "User not Found. Please try again.",
                    404: "You're not Registered. Please contact the admin.",
                    500: "Server Error. Please try again later."
                }.get(response.status_code, "An error occurred. Please try again later.")
                
                print("Error Message :: ", error_message)
                return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})

        except requests.exceptions.RequestException as e:
            print("Error:", e)
            error_message = "An error occurred. Please try again later."
            return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})

    else:
        error_message = "Invalid request. Please try again."
        return render(request, 'main_cg_site/auth/login.html', {'error_message': error_message})
    

@csrf_protect
def center(request):
    print('---------------- Center Function View ---------------- ')
    API_URL = settings.API_URL

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('login-type')
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        
        print("Api URL :: ", API_URL)

        print("Username :: ", username)
        print("Password :: ", password)
        print("User Type :: ", user_type)
        token_url = f"{API_URL}token/"
        
        try:
            center = Center.objects.get(username=username)
            print("Center :: ", center)
            print("Token URL :: ", token_url)
            token_response = requests.get(token_url, data={"username": username, "password": password, "user_type": user_type})
            token_response.raise_for_status()
            token_json = token_response.json()
            access_token = token_json.get('access')
            print("Access Token :: ", access_token)
            
            if username == center.username and password == center.password and access_token is not None:
                print("Login Successful")
                studentDataList = []
                students = Student.objects.filter(center_id=center.id)
                for student in students:
                    # stu_data = StudentData.objects.get(student_enrollment_no=student.enrollment_no)
                    # stu_marksheets = MarkSheets.objects.filter(student_enrollment_no=student.enrollment_no)
                    
                    # studentMarksheetsSerializer = M÷arkSheetSerializer(stu_marksheets, many=True)
                    studentSerializer = StudentSerializer(student)
                    # studentSerializer = StudentDataSerializer(stu_data)
            
                    studentDataList.append({
                        'student_personal_info': studentSerializer.data,
                        # 'student_data': studentSerializer.data,
                        # 'student_marksheets': studentMarksheetsSerializer.data,
                    })
                
                return render(request, 'center_cg_site/home/center.html', {
                    'is_logged_in': True,
                    'center_name': center.center_name,
                    'center_id': center.id,
                    'students': studentDataList,
                    'api_url': API_URL,
                    'token': access_token,
                })
            else:
                return render(request, 'main_cg_site/auth/login.html', {'error_message': 'Incorrect Password. Please try again.'})
        
        except Center.DoesNotExist:
            print("Center does not exist")
            return render(request, 'main_cg_site/auth/login.html', {'error_message': 'Center not found. Please try again.'})
        
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return render(request, 'main_cg_site/auth/login.html', {'error_message': 'Something Went Wrong. Please try again.'})
        
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

# Logout -------------->
@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('login')