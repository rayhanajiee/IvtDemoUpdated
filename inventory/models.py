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
    condition = models.CharField(max_length=255, db_column="Kondisi")
    history = models.TextField(db_column="Keterangan")  # Renamed from 'history'
    tipe_unit = models.CharField(max_length=255, db_column="TipeUnit")
    digit_1 = models.IntegerField(db_column="Digit1", blank=True, null=True, default = 0)
    kode_asset = models.CharField(max_length=255, db_column="KodeAsset",blank=True, null=True, default = "default")
    digit_23 = models.IntegerField(db_column="Digit2&3", blank=True, null=True, default = 0)
    kode_golongan = models.CharField(max_length=255, db_column="KodeGolongan",blank=True, null=True, default = "default")
    digit_45 = models.IntegerField(db_column="Digit4&5", blank=True, null=True, default = 0)
    kode_jenisunit = models.CharField(max_length=255, db_column="KodeJenisUnit", blank=True, null=True, default = "default")
    urutan = models.IntegerField(db_column="Urutan", blank=True, null=True, default = 0)
    bulan = models.IntegerField(db_column="Bulan", blank=True, null=True, default = 0)
    tahun = models.IntegerField(db_column="Tahun", blank=True, null=True, default = 0)
    bpb_ppat = models.CharField(max_length=255, db_column="BPB/PPAT", blank=True, null=True, default = "default")
    po = models.CharField(max_length=255, db_column="PO", blank=True, null=True, default = "default")
    photo = models.ImageField(null=True, blank=True, upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
