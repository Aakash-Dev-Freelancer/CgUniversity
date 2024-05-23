from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, StudentData, MarkSheets, StudentLogin
from rest_framework.decorators import api_view, permission_classes
from .serializers import MarkSheetSerializer
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser

from django.conf import settings

from .serializers import StudentSerializer, StudentLoginSerializer, StudentDataSerializer, AdminLoginSerializer
from .models import AdminLogin

from rest_framework.exceptions import NotFound

# Define a custom exception handler for 404 errors
def custom_exception_handler(exc, context):
    # Check if the exception is a 404 error
    if isinstance(exc, NotFound):
        # Return a custom response for 404 errors
        return Response({"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
    # For any other exceptions, use the default exception handler
    return None

@api_view(['GET'])
@permission_classes([AllowAny])
def get_tokens_for_user(request):
    user = StudentLogin.objects.first()
    refresh = RefreshToken.for_user(user)
    return Response({ 
       'refresh': str(refresh),
       'access': str(refresh.access_token),
    })
    
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
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student created successfully"}, status=status.HTTP_201_CREATED)
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
        
        print(username, password, user_type)

        try:
            if user_type == "student":
                student = Student.objects.get(enrollment_no=username)
                studentData = StudentData.objects.get(pk=student.enrollment_no)
                studentMarksheets = MarkSheets.objects.filter(student_enrollment_no=student.enrollment_no)
                studentMarksheetsSerializer = MarkSheetSerializer(studentMarksheets, many=True)
                studentDataSerializer = StudentSerializer(student)
                studentSerializer = StudentDataSerializer(studentData)

                if password == student.password:
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
                students =  Student.objects.order_by("enrollment_no")
                studentsData = StudentData.objects.all()
                studentsMarksheets = MarkSheets.objects.all()
                studentMarksheetsSerializer = MarkSheetSerializer(studentsMarksheets, many=True)
                studentSerializer = StudentSerializer(students, many=True)
                studentDataSerializer = StudentDataSerializer(studentsData , many=True)
                admin = AdminLogin.objects.get(username=username)
                adminLoginSerializer = AdminLoginSerializer(admin)
                
                if password == admin.password:
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

    def retrieve(self, request, *args, **kwargs):
        enrollment_no = kwargs.get('student_enrollment_no')
        queryset = self.get_queryset().filter(student_enrollment_no=enrollment_no)
        if not queryset.exists():
            return Response({"message": "Student with this enrollment number does not exist."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Student data updated successfully"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Student data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class MarkSheetListCreateView(generics.ListCreateAPIView):
    queryset = MarkSheets.objects.all()
    serializer_class = MarkSheetSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True, "message": "Mark sheet created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MarkSheetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarkSheets.objects.all()
    serializer_class = MarkSheetSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Mark sheet updated successfully"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Mark sheet deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
   
class MarkSheetByEnrollmentView(generics.ListAPIView):
    serializer_class = MarkSheetSerializer

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
