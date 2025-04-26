from django.db import models

# Create your models here.
from django.db import models
from clients.models import Client  # import the Client model

class Program(models.Model):  # Model for Programs
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model): # Model For enrollment(Customer & Program)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='enrollments')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'program')  # prevents duplicate enrollments

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name} - {self.program.name}"

