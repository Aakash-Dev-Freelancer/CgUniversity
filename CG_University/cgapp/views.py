from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, StudentData, MarkSheets, StudentLogin
from rest_framework.decorators import api_view, permission_classes
from .serializers import MarkSheetSerializer
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from .serializers import StudentSerializer, StudentLoginSerializer, StudentDataSerializer, AdminLoginSerializer
from .models import AdminLogin, Center

from rest_framework.exceptions import NotFound


def custom_exception_handler(exc, context):
    print(exc)
    if isinstance(exc, Http404):
        return Response({"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "An unexpected error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_tokens_for_user(request):
    try:
        user_type = request.data.get('user_type')
        username =  request.data.get('username')
        user = None
        if user_type == 'student':
            user = StudentLogin.objects.first()
        elif user_type == 'center':
            try:
                user = Center.objects.get(username=username)
                print(f"Found center: {user}")
            except ObjectDoesNotExist:
                return Response({'error': 'Center user not found'}, status=status.HTTP_404_NOT_FOUND)
        elif user_type == 'admin':
            print(f"Username: {username}")
            user = AdminLogin.objects.get(username=username)
        else:
            return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)
        print(f"Refresh token: {refresh}")
        return Response({ 
           'refresh': str(refresh),
           'access': str(refresh.access_token),
        })
    except Exception as e:
        print(f"Exception occurred: {e}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class AddStudent(generics.ListCreateAPIView):
    queryset = StudentLogin.objects.all()
    serializer_class = StudentLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student Login created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        marksheets = MarkSheets.objects.filter(student_enrollment_no=request.data['enrollment_no'], )
        marksheet_id = []
        for marksheet in marksheets: 
            marksheet_id.append(marksheet.id)
        request.data['list_of_integers'] = marksheet_id
        
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Student created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data
        for field in data.keys():
            if not data[field]:
                data.pop(field)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class StudentLoginAPIView(generics.ListCreateAPIView):
    serializer_class = StudentLoginSerializer
    admin_serializer_class = AdminLoginSerializer

    def create(self, request, *args, **kwargs):
        
        username = request.data.get('username')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        
        try:
            if user_type == "student":
                student_login = StudentLogin.objects.get(username=username)
                
                if password == student_login.password:
                    student = Student.objects.get(enrollment_no=username)
                    studentData = StudentData.objects.get(pk=student.enrollment_no)
                    studentMarksheets = MarkSheets.objects.filter(student_enrollment_no=student.enrollment_no)
                    
                    studentSerializer = StudentDataSerializer(studentData)
                    studentDataSerializer = StudentSerializer(student)
                    studentMarksheetsSerializer = MarkSheetSerializer(studentMarksheets, many=True)
                    
                    print(studentSerializer.data)
                    print(studentDataSerializer.data)
                    print(studentMarksheetsSerializer.data)
                    
                    return Response({
                        'success': 'Logged in successfully',
                        "student_info": {
                            "student_data": studentSerializer.data,
                            "student_personal_info": studentDataSerializer.data,
                            "student_marksheets": studentMarksheetsSerializer.data
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, 'message': 'Incorrect Password'}, status=status.HTTP_401_UNAUTHORIZED)
            
            elif user_type == "admin":
                admin = AdminLogin.objects.get(username=username)
                
                if password == admin.password:
                    students =  Student.objects.order_by("enrollment_no")
                    studentsData = StudentData.objects.all()
                    studentsMarksheets = MarkSheets.objects.all()
                    studentMarksheetsSerializer = MarkSheetSerializer(studentsMarksheets, many=True)
                    studentSerializer = StudentSerializer(students, many=True)
                    studentDataSerializer = StudentDataSerializer(studentsData , many=True)
                    adminLoginSerializer = AdminLoginSerializer(admin)
                    
                    return Response({
                        'success': 'Logged in successfully',
                        'admin_info': adminLoginSerializer.data,
                        'students': studentSerializer.data,
                        'students_data': studentDataSerializer.data,
                        'students_marksheets': studentMarksheetsSerializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False, 'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
                
        except Student.DoesNotExist:
            return Response({'success': False, 'message':  'Student not registered'}, status=status.HTTP_404_NOT_FOUND)
        
        except AdminLogin.DoesNotExist:
            return Response({'success': False, 'message':  'Admin not registered'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print("Server Error:", e)
            return Response({'error': 'Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        

class StudentDataListCreateAPIView(generics.ListCreateAPIView):
    queryset = StudentData.objects.all()
    serializer_class = StudentDataSerializer

    def post(self, request, *args, **kwargs):
        enrollment_no = request.data.get('student_enrollment_no')
        provision_file = request.FILES.get('student_provision')
        admit_card_file = request.FILES.get('student_admit_card')
        affidevit_file = request.FILES.get('student_affidevit')
        migrations_file = request.FILES.get('student_migrations')
        
        data = {
            'student_enrollment_no': enrollment_no,
            'student_provision': provision_file,
            'student_admit_card': admit_card_file,
            'student_affidevit': affidevit_file,
            'student_migrations': migrations_file
        }
        
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student data created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDataRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentData.objects.all()
    serializer_class = StudentDataSerializer
    lookup_field = 'student_enrollment_no'
    parser_classes = [MultiPartParser, FormParser]

    def retrieve(self, request, *args, **kwargs):
        try:
            enrollment_no = kwargs.get('student_enrollment_no')
            queryset = self.get_queryset().filter(student_enrollment_no=enrollment_no)
            if not queryset.exists():
                return Response({"message": "Student with this enrollment number does not exist."}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            enrollment_no = kwargs.get('student_enrollment_no')
            instance = self.get_queryset().filter(student_enrollment_no=enrollment_no).first()
            
            if not instance:
                return Response({"message": "Student with this enrollment number does not exist."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Student data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class MarkSheetListCreateView(generics.ListCreateAPIView):
    queryset = MarkSheets.objects.all()
    serializer_class = MarkSheetSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            student_enrollment_no = request.data.get('student_enrollment_no')
            all_mark_sheets = MarkSheets.objects.filter(student_enrollment_no=student_enrollment_no)
            all_ids = all_mark_sheets.values_list('id', flat=True)
            return Response({
                'success': True, 
                'message': "Mark sheet created successfully", 
                'id_list': list(all_ids)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkSheetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarkSheets.objects.all()
    serializer_class = MarkSheetSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = self.get_queryset().filter(pk=pk)
        if not queryset.exists():
            return Response({"message": "Mark sheet with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response({"message": "Mark sheet with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Mark sheet updated successfully"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = self.get_queryset().filter(pk=pk).first()
        if not instance:
            return Response({"message": "Mark sheet with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(instance)
        return Response({"message": "Mark sheet deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class MarkSheetByEnrollmentView(generics.ListCreateAPIView):
    serializer_class = MarkSheetSerializer
    permission_classes = [IsAuthenticated]  # Optional: Ensure that only authenticated users can access this view

    def get_queryset(self):
        enrollment_no = self.kwargs.get('enrollment_no')
        queryset = MarkSheets.objects.filter(student_enrollment_no=enrollment_no)
        if not queryset.exists():
            raise NotFound("No mark sheets found for this enrollment number")
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        enrollment_no = self.kwargs.get('enrollment_no')
        mark_sheet_id = self.kwargs.get('pk')
        try:
            mark_sheet = MarkSheets.objects.get(student_enrollment_no=enrollment_no, id=mark_sheet_id)
        except MarkSheets.DoesNotExist:
            raise NotFound("No mark sheet found for this enrollment number and ID")

        serializer = self.serializer_class(mark_sheet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        enrollment_no = self.kwargs.get('enrollment_no')
        mark_sheet_id = self.kwargs.get('pk')
        try:
            mark_sheet = MarkSheets.objects.get(student_enrollment_no=enrollment_no, id=mark_sheet_id)
        except MarkSheets.DoesNotExist:
            raise NotFound("No mark sheet found for this enrollment number and ID")

        mark_sheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminLoginListCreateView(generics.ListCreateAPIView):
    queryset = AdminLogin.objects.all()
    serializer_class = AdminLoginSerializer


class AdminLoginUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminLogin.objects.all()
    serializer_class = AdminLoginSerializer

    def perform_update(self, serializer):
        username = serializer.validated_data.get('username')
        if AdminLogin.objects.exclude(pk=self.kwargs['pk']).filter(username=username).exists():
            raise ValidationError("Username already exists. Please choose a different one.")
        serializer.save()
