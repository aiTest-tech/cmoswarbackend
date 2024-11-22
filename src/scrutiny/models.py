from django.db import models

class ScrutinyRecord(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()  # Field to store the input text data
    scrutiny_decision = models.CharField(max_length=50, null=True, blank=True)  # Field for scrutiny decision (e.g., Accept/Reject)
    department = models.CharField(max_length=255, null=True, blank=True)  # Field to store the assigned department
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the record was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for the last update

    def __str__(self):
        return f"Record {self.id}: {self.scrutiny_decision} - {self.department}"
