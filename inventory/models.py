from django.db import models
from django.contrib.auth.models import User

class InventoryItem(models.Model):
    no = models.CharField(max_length=255, db_column="NoInventaris")
    name = models.CharField(max_length=255, db_column="Item")
    specifications = models.TextField(db_column="SpesifikasiSubUnit")
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=255, db_column="LokasiUpdate2024")
    pic = models.CharField(max_length=255, db_column="User")
    condition = models.ForeignKey('Condition', on_delete=models.SET_NULL, blank=True, null=True)
    history = models.TextField(db_column="Keterangan")  # Renamed from 'history'
    tipe_unit = models.CharField(max_length=255, db_column="TipeUnit")
    digit_1 = models.IntegerField(db_column="Digit1", blank=True, null=True, default = 0)
    kode_asset = models.CharField(max_length=255, db_column="KodeAsset",blank=True, null=True, default = "default")
    digit_23 = models.IntegerField(db_column="Digit2_3", blank=True, null=True, default = 0)
    kode_golongan = models.CharField(max_length=255, db_column="KodeGolongan",blank=True, null=True, default = "default")
    digit_45 = models.IntegerField(db_column="Digit4_5", blank=True, null=True, default = 0)
    kode_jenisunit = models.CharField(max_length=255, db_column="KodeJenisUnit", blank=True, null=True, default = "default")
    urutan = models.IntegerField(db_column="Urutan", blank=True, null=True, default = 0)
    bulan = models.IntegerField(db_column="Bulan", blank=True, null=True, default = 0)
    tahun = models.IntegerField(db_column="Tahun", blank=True, null=True, default = 0)
    bpb_ppat = models.CharField(max_length=255, db_column="BPB/PPAT", blank=True, null=True, default = "default")
    po = models.CharField(max_length=255, db_column="PO", blank=True, null=True, default = "default")
    photo = models.ImageField(null=True, blank=True, upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(db_column="date_created",auto_now_add=True)

    
    def __str__(self):
        return self.name
    
class DescriptionModel(models.Model):
    first_digit = models.CharField(max_length=100)
    second_digit = models.TextField()
    third_digit = models.TextField()
    day = models.CharField(max_length=2)
    month = models.CharField(max_length=2)
    year = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.first_digit} - {self.day}/{self.month}/{self.year}'


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'departments'

    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'conditions'

    def __str__(self):
        return self.name
