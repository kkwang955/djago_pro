from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect('menu')
            response.set_cookie('username', username)  # Adding username to the cookie
            return response
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        # print(1)
        username = request.POST['username']
        if not username:
            return render(request, 'register.html', {'error': '用户名不能为空'})
        print('username:',username)

        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'register.html', {'error': '两次密码输入不一致'})
        # 创建用户
        user = User.objects.create_user(username=username, password=password1)
        # 登录用户
        login(request, user)
        # 重定向到首页或其他页面
        return redirect('menu')
    else:
        return render(request, 'register.html')

@login_required(login_url='login')
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('login')
    else:
        return render(request, 'menu.html')
    
@login_required(login_url='login')
def menu(request):
    if request.user.is_authenticated:
        return render(request, 'menu.html')
    else:
        return redirect('login_view')
    
@login_required(login_url='login_view ')
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            return redirect('create_patient')  # 重定向到成功页面
    else:
        form = PatientForm()
    return render(request, 'create_patient.html', {'form': form})

@login_required(login_url='login') 
def patient_info_view(request):
    current_user = request.user
    patients = Patient.objects.filter(user=current_user)
    return render(request, 'patient_info.html', {'patients': patients})

@login_required(login_url='login')
def patient_info_entry(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            return redirect('patient_info_entry')
    else:
        form = PatientForm()
    return render(request, 'patient_info_entry.html', {'form': form})

@login_required(login_url='login')
def drug_info(request, patient_id):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            drug = form.save(commit=False)
            drug.patient_id = patient_id
            drug.save()
            return redirect('drug_info', patient_id=patient_id)
    else:
        form = MedicationForm()
    return render(request, 'drug_info.html', {'form': form, 'patient_id': patient_id})
    
@login_required(login_url='login')
def delete_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('id')
        patient = Patient.objects.get(id=patient_id)
        patient.delete()
        return redirect('patient_info_view')
    else:
        return redirect('patient_info_view')

@login_required(login_url='login')
def delete_drug(request):
    if request.method == 'POST':
        drug_id = request.POST.get('id')
        drug = Medication.objects.get(id=drug_id)
        drug.delete()
        return redirect('patient_info_view')
    else:
        return redirect('patient_info_view')
    

@login_required(login_url='login')
def update_medication(request):
    if request.method == 'POST':
        medication_id = request.POST.get('medicationID')
        column_name = request.POST.get('columnName')
        new_value = request.POST.get('newValue')
        medication = get_object_or_404(Medication, id=medication_id)
        if column_name == 'drug_name':
            medication.drug_name = new_value
        elif column_name == 'dosage':
            medication.dosage = new_value
        elif column_name == 'before_or_after_meal':
            medication.before_or_after_meal = new_value
        elif column_name == 'is_machine_dispensed':
            medication.is_machine_dispensed = new_value
        elif column_name == 'morning_dosage':
            medication.morning_dosage = new_value
        elif column_name == 'noon_dosage':
            medication.noon_dosage = new_value
        elif column_name == 'evening_dosage':
            medication.evening_dosage = new_value
        elif column_name == 'night_dosage':
            medication.night_dosage = new_value
        medication.save()

        return redirect('patient_info_view')
    else:
        return redirect('patient_info_view')
    

import csv
from django.http import HttpResponse

@login_required(login_url='login')
def export_patient_medications_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_medications.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['床号', '姓名', '药名', '计量', '餐前/餐后',
                     '是否分药机分药', '早', '中', '晚', '夜'])

    patients = Patient.objects.all()
    for patient in patients:
        bed_number = patient.bed_number
        patient_name = patient.patient_name
        
        for medication in patient.medications.all():
            row_data = [bed_number, patient_name,
                        medication.drug_name, medication.dosage,
                        medication.before_or_after_meal,
                        '是' if medication.is_machine_dispensed else '否',
                        '是' if medication.morning_dosage else '否', 
                        '是' if medication.noon_dosage else '否',
                        '是' if medication.evening_dosage else '否', 
                        '是' if medication.night_dosage else '否']
            writer.writerow(row_data)

    return response

from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username')
        if username:
            queryset = queryset.filter(username=username)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        for user_data in data:
            patient_data = []
            user_id = user_data['id']
            patients = Patient.objects.filter(user_id=user_id)
            for patient in patients:
                patient_serializer = PatientSerializer(patient)
                patient_data.append(patient_serializer.data)
                medications_data = []
                medications = patient.medications.all()
                for medication in medications:
                    medication_serializer = MedicationSerializer(medication)
                    medications_data.append(medication_serializer.data)
                patient_data[-1]['medications'] = medications_data
            user_data['patients'] = patient_data
        return Response(data)
    
class ImageUploadView(APIView):
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def upload_view(request):
    if request.method == 'POST':
        # 获取上传的图像文件
        uploaded_image = request.FILES.get('image')
        
        # 获取传入的 username
        username = request.POST.get('username')

        if uploaded_image and username:
            # 保存图像到数据库
            user = User.objects.get(username=username)

            image = Image(user=user, image=uploaded_image)
            image.save()
            serializer = ImageSerializer(image)
            return JsonResponse({'message': '图像上传成功！'}, status=200)
        else:
            return JsonResponse({'error': '未提供图像或用户名'}, status=400)
    else:
        return JsonResponse({'error': '仅支持 POST 请求'}, status=405)
    
def test(request):
    return render(request, 'test.html')