from django.db import models
from auth_app.models import User, Project

class WTC(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    lang = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    district_corporation = models.CharField(max_length=100)
    taluka_zone = models.CharField(max_length=100)
    village_area = models.CharField(max_length=100)
    subject = models.TextField()
    department = models.CharField(max_length=100)
    email = models.EmailField()
    mode = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"WTC Entry {self.id} - {self.name}"