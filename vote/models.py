from django.db import models
from django.contrib.auth.models import User

class ElectionManager(models.Model):
    id_number = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    

class ElectionCampaign(models.Model):
    manager = models.ForeignKey(ElectionManager, on_delete=models.CASCADE)  # ✅ Link to manager
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    image = models.ImageField(upload_to="campaigns/", null=True, blank=True)

    def __str__(self):
        return self.name

class Election(models.Model):
    campaign = models.ForeignKey(ElectionCampaign, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # ✅ Only Election Name now

    def __str__(self):
        return f"{self.name} - {self.campaign.name}"
    
class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)  # ✅ Link to Election
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="candidate_profiles/", blank=True, null=True)

    def __str__(self):
        return self.name
    
class Voter(models.Model):
    campaign = models.ForeignKey(ElectionCampaign, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    course_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    year_of_study = models.IntegerField()
    semester = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)  # ✅ Approval status

    def __str__(self):
        return f"{self.name} ({self.student_id})"

    
class Vote(models.Model):
    voter = models.ForeignKey("Voter", on_delete=models.CASCADE)
    election = models.ForeignKey("Election", on_delete=models.CASCADE)
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("voter", "election")  # ✅ Prevent multiple votes

class ElectionOfficer(models.Model):
    id_number = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to="officers/", null=True, blank=True)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    created_by = models.ForeignKey(ElectionManager, on_delete=models.CASCADE)  # ✅ Link to Manager
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
class PresidingOfficer(models.Model):
    id_number = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to="presiding_officers/", null=True, blank=True)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    created_by = models.ForeignKey("ElectionManager", on_delete=models.CASCADE)  # ✅ Created by Election Manager
    password = models.CharField(max_length=255)  # Store hashed password (to be implemented later)

    def __str__(self):
        return self.username

