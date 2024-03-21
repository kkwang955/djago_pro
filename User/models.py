from django.db import models
from django.contrib.auth.models import User

    
class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bed_number = models.IntegerField(verbose_name='床号')
    patient_name = models.CharField(max_length=100, verbose_name='姓名')

    def __str__(self) -> str:
        return f'{self.bed_number} - {self.patient_name}'

    def delete(self):
        super().delete()

class Medication(models.Model):
    drug_name = models.CharField(max_length=100, verbose_name='药物名称')
    dosage = models.CharField(max_length=100, verbose_name='计量')
    before_or_after_meal = models.CharField(max_length=10, verbose_name='餐前/餐后')
    is_machine_dispensed = models.BooleanField(verbose_name='是否分药机分药')
    morning_dosage = models.BooleanField(verbose_name='早')
    noon_dosage = models.BooleanField(verbose_name='中')
    evening_dosage = models.BooleanField(verbose_name='晚')
    night_dosage = models.BooleanField(verbose_name='夜')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications', null=True, blank=True)
    def __str__(self) -> str:
        return f'{self.drug_name}'
    
    def delete(self):
        super().delete()

def user_directory_path(instance, filename):
    # 生成上传路径：images/<username>/<filename>
    return f'images/{instance.user.username}/{filename}'

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)