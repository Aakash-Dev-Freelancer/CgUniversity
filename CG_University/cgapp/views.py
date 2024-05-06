from rest_framework import generics, status
from rest_framework.response import Response
from .models import Student, StudentData, MarkSheets
from rest_framework.decorators import api_view
from .serializers import MarkSheetSerializer
from rest_framework.exceptions import ValidationError

from .serializers import StudentSerializer, StudentLoginSerializer, StudentDataSerializer, AdminLoginSerializer

from .models import AdminLogin

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class StudentLoginAPIView(generics.CreateAPIView):
    serializer_class = StudentLoginSerializer
    admin_serializer_class = AdminLoginSerializer


    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user_type = request.data.get('user_type')

        try:
            if(user_type == "student"):
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
                admin = AdminLogin.objects.get(username=username)
                adminLoginSerializer = AdminLoginSerializer(admin)
                if password == admin.password:
                    return Response({
                        'success': 'Logged in successfully',
                        'admin_info': adminLoginSerializer.data
                    })
                return Response({'success': False, 'message': 'Not Authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response({'success': False, 'message':  'Not Registered'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Server Error:", e)
            return Response({'error': 'Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        



class StudentDataListCreateAPIView(generics.ListCreateAPIView):
    queryset = StudentData.objects.all()
    serializer_class = StudentDataSerializer

@api_view(['POST'])
def upload_student_data(request):
    serializer = StudentDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MarkSheetListCreateView(generics.ListCreateAPIView):
    queryset = MarkSheets.objects.all()
    serializer_class = MarkSheetSerializer

class MarkSheetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MarkSheets.objects.all()
    serializer_class = MarkSheetSerializer


class AdminLoginListCreateView(generics.ListCreateAPIView):
    queryset = AdminLogin.objects.all()
    serializer_class = AdminLoginSerializer
class AdminLoginCreateView(generics.CreateAPIView):
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
