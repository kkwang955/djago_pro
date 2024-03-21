from django.urls import path, include
from .views import *
urlpatterns = [
    path('', login_view),
    path('patient_info_view/', patient_info_view, name='patient_info_view'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('patient_info_entry/', patient_info_entry, name='patient_info_entry'),
    path('logout/', logout, name='logout'),
    path('menu/', menu, name='menu'),
    path('index/', index, name='index'),
    path('drug/<int:patient_id>/', drug_info, name='drug_info'),
    path('test/', test, name='test'),
    path('delete_patient', delete_patient, name='delete_patient'),
    path('delete_drug', delete_drug, name='delete_drug'),
    path('update_medication/', update_medication, name='update_medication'),
    path('create_patient/',create_patient,name='create_patient'),
    path('export2excel', export_patient_medications_csv, name='export2excel'),
    path('UserList', UserListView.as_view(), name='UserList'),
    path('upload', upload_view, name='image_upload'),

]