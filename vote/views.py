import pandas as pd
import re
import openpyxl
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from .models import ElectionManager,ElectionCampaign,Election,Candidate,Voter,Vote,ElectionOfficer,PresidingOfficer
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse
from django.core.files.storage import default_storage

def index(request):
    return render(request, 'index.html')

def register_manager(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number")
        profile_picture = request.FILES.get("profile_picture")
        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        errors = {}

        # ✅ Ensure ID Number is unique
        if ElectionManager.objects.filter(id_number=id_number).exists():
            errors["id_error"] = "ID number already exists."

        # ✅ Ensure Username is unique
        if ElectionManager.objects.filter(username=username).exists():
            errors["username_error"] = "Username already exists."

        # ✅ Ensure Email is unique
        if ElectionManager.objects.filter(email=email).exists():
            errors["email_error"] = "Email already registered."

        # ✅ Ensure Phone Number is unique
        if ElectionManager.objects.filter(phone_number=phone_number).exists():
            errors["phone_error"] = "Phone number already registered."

        # ✅ Ensure Full Name does not contain numbers
        if any(char.isdigit() for char in fullname):
            errors["fullname_error"] = "No numbers in full name."

        # ✅ Ensure Password has at least 8 characters
        if len(password) < 8:
            errors["password_length"] = "Password needs 8 chars"

        # ✅ Ensure Confirm Password matches Password
        if password != confirm_password:
            errors["password_error"] = "Passwords do not match."

        # ✅ If errors exist, re-render the form with previous data
        if errors:
            return render(request, "register_manager.html", {
                "errors": errors,
                "id_number": id_number,
                "fullname": fullname,
                "username": username,
                "phone_number": phone_number,
                "email": email,
                "address": address,
            })

        # ✅ Create Election Manager
        manager = ElectionManager(
            id_number=id_number,
            profile_picture=profile_picture,
            fullname=fullname,
            username=username,
            phone_number=phone_number,
            email=email,
            address=address,
            password=password  # ⚠️ Store securely in real applications
        )
        manager.save()

        return redirect("/login_manager/")  # ✅ Redirect to login after successful registration

    return render(request, "register_manager.html")


def login_manager(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            manager = ElectionManager.objects.get(username=username, password=password)
            return redirect("manager_dashboard", manager_id=manager.id)  # ✅ Pass manager_id correctly
        except ElectionManager.DoesNotExist:
            return render(request, "login_manager.html", {"error": "Invalid username or password"})

    return render(request, "login_manager.html")


def manager_dashboard(request, manager_id):
    manager = get_object_or_404(ElectionManager, id=manager_id)

    # ✅ Fetch campaigns only created by this manager
    campaigns = ElectionCampaign.objects.filter(manager=manager)

    return render(request, "manager_dashboard.html", {"manager": manager, "campaigns": campaigns})

def create_campaign(request, manager_id):  # ✅ Ensure manager_id is passed
    manager = get_object_or_404(ElectionManager, id=manager_id)  # ✅ Get Manager Object

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        image = request.FILES.get("image")

        # ✅ Create campaign with manager
        campaign = ElectionCampaign(
            manager=manager,  # ✅ Assign manager here
            name=name,
            description=description,
            start_time=start_time,
            end_time=end_time,
            image=image
        )
        campaign.save()

        return redirect(f"/manager/{manager.id}/dashboard/")  # ✅ Redirect to manager dashboard

    return render(request, "create_campaign.html", {"manager": manager})

# List All Campaigns
def campaign_list(request, manager_id):
    campaigns = ElectionCampaign.objects.all()
    manager = get_object_or_404(ElectionManager, id=manager_id)  # ✅ Ensure manager is retrieved
    return render(request, "campaign_list.html", {"campaigns": campaigns, "manager": manager})


def edit_campaign(request, campaign_id):
    campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
    manager = campaign.manager  # ✅ Get the manager from the campaign

    if request.method == "POST":
        campaign.name = request.POST.get("name")
        campaign.description = request.POST.get("description")
        campaign.start_time = request.POST.get("start_time")
        campaign.end_time = request.POST.get("end_time")

        if "image" in request.FILES:
            campaign.image = request.FILES["image"]

        campaign.save()

        return redirect(f"/manager/{manager.id}/dashboard/")  # ✅ Redirect with `manager_id`

    return render(request, "edit_campaign.html", {"campaign": campaign, "manager": manager})

# 

def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
    manager_id = campaign.manager.id  # ✅ Get manager ID before deleting
    campaign.delete()

    return redirect(f"/manager/{manager_id}/dashboard/")


# Create Election Inside a Campaign
def create_election(request, campaign_id):
    campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
    manager_id = campaign.manager.id  # ✅ Get the manager ID from the campaign
    manager = get_object_or_404(ElectionManager, id=manager_id)

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Election.objects.create(campaign=campaign, name=name)

        return redirect(f"/manager/{manager_id}/dashboard/")  # ✅ Redirect with `manager_id`

    return render(request, "create_election.html", {"campaign": campaign, "manager_id": manager_id,"manager":manager})

def edit_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    campaign = election.campaign
    manager_id = campaign.manager.id  # ✅ Get the manager ID from the campaign

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            election.name = name
            election.save()
            return redirect(f"/manager/{manager_id}/dashboard/")  # ✅ Redirect with `manager_id`

    return render(request, "edit_election.html", {"election": election, "manager_id": manager_id})


def delete_election(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    campaign = election.campaign
    manager_id = campaign.manager.id  # ✅ Get the manager ID from the campaign

    election.delete()

    return redirect(f"/manager/{manager_id}/dashboard/")  # ✅ Redirect with `manager_id`

def view_profile(request, manager_id):
    manager = get_object_or_404(ElectionManager, id=manager_id)
    return render(request, "view_profile.html", {"manager": manager})


def edit_profile(request, manager_id):
    manager = get_object_or_404(ElectionManager, id=manager_id)

    if request.method == "POST":
        manager.fullname = request.POST.get("fullname", manager.fullname)  # ✅ Ensure this matches models.py
        manager.phone_number = request.POST.get("phone_number", manager.phone_number)
        manager.email = request.POST.get("email", manager.email)
        manager.address = request.POST.get("address", manager.address)

        if "profile_picture" in request.FILES:
            manager.profile_picture = request.FILES["profile_picture"]

        manager.save()
        return redirect("view_profile", manager_id=manager.id)

    return render(request, "edit_profile.html", {"manager": manager})

def create_candidate(request, election_id):
    election = Election.objects.get(id=election_id)

    # ✅ Allow only Managers & Officers to Add Candidates
    if not (request.user.is_authenticated and (
            hasattr(request.user, 'electionmanager') or hasattr(request.user, 'electionofficer'))):
        return render(request, "error.html", {"error": "You do not have permission to add candidates."})

    if request.method == "POST":
        name = request.POST.get("name")
        subtitle = request.POST.get("subtitle")
        profile_picture = request.FILES.get("profile_picture")

        Candidate.objects.create(
            election=election,
            name=name,
            subtitle=subtitle,
            profile_picture=profile_picture
        )

        return redirect("create_candidate", election_id=election.id)

    return render(request, "create_candidate.html", {"election": election})

def edit_candidate(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)

    # ✅ Allow only Managers & Officers
    if not (request.user.is_authenticated and (
            hasattr(request.user, 'electionmanager') or hasattr(request.user, 'electionofficer'))):
        return render(request, "error.html", {"error": "You do not have permission to edit candidates."})

    if request.method == "POST":
        candidate.name = request.POST.get("name")
        candidate.subtitle = request.POST.get("subtitle")

        if 'profile_picture' in request.FILES:
            candidate.profile_picture = request.FILES['profile_picture']

        candidate.save()
        return redirect("create_candidate", election_id=candidate.election.id)

    return render(request, "edit_candidate.html", {"candidate": candidate})

def delete_candidate(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)

    # ✅ Allow only Managers & Officers
    if not (request.user.is_authenticated and (
            hasattr(request.user, 'electionmanager') or hasattr(request.user, 'electionofficer'))):
        return render(request, "error.html", {"error": "You do not have permission to delete candidates."})

    candidate.delete()
    return redirect("create_candidate", election_id=candidate.election.id)

def upload_voters(request, campaign_id):
    if request.method == "POST":
        file = request.FILES.get("excel_file")

        if not file:
            return render(request, "upload_voters.html", {"error": "No file uploaded"})

        try:
            df = pd.read_excel(file)
            campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
            
            for _, row in df.iterrows():
                Voter.objects.create(
                    campaign=campaign,
                    student_id=row["Student ID"],
                    name=row["Name"],
                    date_of_birth=row["Date of Birth"],
                    email=row["Email Address"],
                    phone_number=row["Phone Number"],
                    course_name=row["Course Name"],
                    department=row["Department"],
                    year_of_study=row["Year of Study"],
                    semester=row["Semester"],
                    is_approved=False  # Default unapproved until election manager approves
                )

            # ✅ Ensure officer_id is retrieved correctly
            officer = request.session.get("officer_id")  # Get officer_id from session
            if not officer:
                return render(request, "upload_voters.html", {"error": "Error: Officer not found in session."})

            return redirect("officer_dashboard", officer_id=officer)

        except Exception as e:
            return render(request, "upload_voters.html", {"error": f"Error: {str(e)}"})

    return render(request, "upload_voters.html")

def voters_list(request, campaign_id):
    campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
    voters = Voter.objects.filter(campaign=campaign)
    return render(request, "voter_list.html", {"campaign": campaign, "voters": voters})

def delete_all_voters(request, campaign_id):
    campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
    Voter.objects.filter(campaign=campaign).delete()
    return redirect("voters_list", campaign_id=campaign.id)

def voter_login(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")

        try:
            voter = Voter.objects.get(student_id=student_id)

            if not voter.is_approved:  # ✅ Check if voter is approved
                messages.error(request, "Your account is not approved yet. Please contact the election manager.")
                return redirect("voter_login")  # 🔄 Redirect back to login page with error

            # ✅ If approved, store voter ID in session
            request.session["voter_id"] = voter.id

            # ✅ Redirect to voter dashboard with voter ID
            return redirect(reverse("voter_dashboard", args=[voter.id]))

        except Voter.DoesNotExist:
            messages.error(request, "Invalid Student ID. Please try again.")
            return redirect("voter_login")

    return render(request, "voter_login.html")

def voter_dashboard(request, voter_id):
    voter = Voter.objects.get(id=voter_id)
    elections = Election.objects.filter(campaign__voter=voter)  # Get elections for this voter

    return render(request, "voter_dashboard.html", {"voter": voter, "elections": elections})

def vote_page(request, voter_id):
    elections = Election.objects.all()  # ✅ Fetch all elections
    return render(request, "vote_page.html", {"elections": elections})

def submit_vote(request, election_id):
    if request.method == "POST":
        voter = get_object_or_404(Voter, id=request.session.get("voter_id"))  # Ensure voter is logged in
        election = get_object_or_404(Election, id=election_id)
        candidate_id = request.POST.get("vote")

        # ✅ Check if the voter has already voted in this election
        if Vote.objects.filter(voter=voter, election=election).exists():
            messages.error(request, f"You have already voted in the election: {election.name}.")
            return redirect("vote_page", voter_id=voter.id)

        # ✅ Save the vote
        candidate = get_object_or_404(Candidate, id=candidate_id)
        Vote.objects.create(voter=voter, election=election, candidate=candidate)

        messages.success(request, f"Your vote for {candidate.name} in the election '{election.name}' has been submitted successfully!")
        return redirect("vote_page", voter_id=voter.id)


    return redirect("vote_page", voter_id=request.session.get("voter_id"))

def approve_voters(request, campaign_id):
    campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
    voters = Voter.objects.filter(campaign=campaign)  # Get voters of the campaign
    return render(request, "approve_voters.html", {"campaign": campaign, "voters": voters})

def approve_voter(request, voter_id):
    voter = get_object_or_404(Voter, id=voter_id)
    voter.is_approved = True
    voter.save()
    messages.success(request, f"Voter {voter.name} has been approved!")
    return redirect("approve_voters", campaign_id=voter.campaign.id)

def disapprove_voter(request, voter_id):
    voter = get_object_or_404(Voter, id=voter_id)
    voter.is_approved = False
    voter.save()
    messages.success(request, f"Voter {voter.name} has been disapproved.")
    return redirect("approve_voters", campaign_id=voter.campaign.id)

def election_results(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    total_votes = Vote.objects.filter(candidate__election=election).count()

    results = []
    for candidate in candidates:
        votes = Vote.objects.filter(candidate=candidate).count()
        percentage = (votes / total_votes) * 100 if total_votes > 0 else 0
        results.append({
            "candidate": candidate,
            "votes": votes,
            "percentage": round(percentage, 2)
        })

    return render(request, "election_results.html", {
        "election": election,
        "results": results,
        "total_votes": total_votes
    })

def register_election_officer(request):
    if request.method == "POST":
        id_number = request.POST.get("id_number")
        fullname = request.POST.get("fullname")
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_picture = request.FILES.get("profile_picture")
        created_by_id = request.POST.get("created_by")  # Election Manager ID

        errors = {}

        # ✅ Ensure ID Number is unique
        if ElectionOfficer.objects.filter(id_number=id_number).exists():
            errors["id_error"] = "ID number already exists."

        # ✅ Ensure Username is unique
        if ElectionOfficer.objects.filter(username=username).exists():
            errors["username_error"] = "Username already exists."

        # ✅ Ensure Email is unique
        if ElectionOfficer.objects.filter(email=email).exists():
            errors["email_error"] = "Email already registered."

        # ✅ Ensure Phone Number is unique
        if ElectionOfficer.objects.filter(phone_number=phone_number).exists():
            errors["phone_error"] = "Phone number already registered."

        # ✅ Ensure Full Name does not contain numbers
        if any(char.isdigit() for char in fullname):
            errors["fullname_error"] = "Full name should not contain numbers."

        # ✅ Ensure Password has at least 8 characters
        if len(password) < 8:
            errors["password_length"] = "Password must be at least 8 characters long."

        # ✅ Ensure Confirm Password matches Password
        if password != confirm_password:
            errors["password_error"] = "Passwords do not match."

        # ✅ Validate if Election Manager exists
        try:
            created_by = ElectionManager.objects.get(id_number=created_by_id)
        except ElectionManager.DoesNotExist:
            errors["created_by_error"] = "Invalid Election Manager ID."

        # If there are errors, re-render the form with errors
        if errors:
            return render(request, "register_election_officer.html", {"errors": errors})

        # Save profile picture if uploaded
        profile_picture_path = None
        if profile_picture:
            profile_picture_path = default_storage.save(f"officer_profiles/{profile_picture.name}", profile_picture)

        # Securely hash the password before saving
        hashed_password = make_password(password)

        # Create new election officer
        officer = ElectionOfficer.objects.create(
            id_number=id_number,
            fullname=fullname,
            username=username,
            phone_number=phone_number,
            email=email,
            password=hashed_password,  # Secure password storage
            profile_picture=profile_picture_path,
            created_by=created_by
        )

        messages.success(request, f"Election Officer {fullname} registered successfully!")
        return redirect("register_election_officer")

    return render(request, "register_election_officer.html")

def election_officer_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        # ✅ Ensure fields are not empty
        if not username or not password:
            return render(request, "election_officer_login.html", {"error": "Both fields are required."})

        try:
            officer = ElectionOfficer.objects.get(username=username)
            
            # ✅ Secure password checking
            if check_password(password, officer.password):
                request.session["officer_id"] = officer.id  # ✅ Store officer_id in session
                return redirect("officer_dashboard", officer_id=officer.id)
            else:
                return render(request, "election_officer_login.html", {"error": "Incorrect password."})

        except ElectionOfficer.DoesNotExist:
            return render(request, "election_officer_login.html", {"error": "User not found."})

    return render(request, "election_officer_login.html")


def officer_dashboard(request, officer_id):
    try:
        officer = ElectionOfficer.objects.get(id=officer_id)

        # ✅ Get the Election Manager (creator of the officer)
        manager_id = officer.created_by.id  # Assuming created_by is the ElectionManager

        # ✅ Get campaigns created by the officer's manager
        campaigns = ElectionCampaign.objects.filter(manager=officer.created_by)

        return render(request, "officer_dashboard.html", {
            "officer": officer,
            "campaigns": campaigns,
            "manager_id": manager_id,  # ✅ Pass manager_id to template
        })
    
    except ElectionOfficer.DoesNotExist:
        return render(request, "error.html", {"error": "Election Officer not found"})
    
def manage_candidates(request, campaign_id):
    campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
    candidates = Candidate.objects.filter(election__campaign=campaign)

    return render(request, "manage_candidates.html", {"campaign": campaign, "candidates": candidates})

def add_candidate(request, campaign_id):
    campaign = get_object_or_404(ElectionCampaign, id=campaign_id)
    elections = campaign.election_set.all()  # Get all elections in this campaign

    if request.method == "POST":
        name = request.POST.get("name")
        election_id = request.POST.get("election")
        profile_picture = request.FILES.get("profile_picture")

        if not name or not election_id:
            return render(request, "add_candidate.html", {"campaign": campaign, "elections": elections, "error": "All fields are required."})

        election = get_object_or_404(Election, id=election_id)

        Candidate.objects.create(
            name=name,
            election=election,
            profile_picture=profile_picture
        )

        return redirect("add_candidate", campaign_id=campaign_id)

    return render(request, "add_candidate.html", {"campaign": campaign, "elections": elections})

def edit_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)

    if request.method == "POST":
        candidate.name = request.POST.get("name", candidate.name)  # Avoids KeyError

        election_id = request.POST.get("election")
        if election_id:
            candidate.election_id = election_id  # Updates only if valid input exists

        if "profile_picture" in request.FILES:
            candidate.profile_picture = request.FILES["profile_picture"]

        candidate.save()
        return redirect("manage_candidates", campaign_id=candidate.election.campaign.id)

    return render(request, "edit_candidate.html", {"candidate": candidate})

    elections = candidate.election.campaign.election_set.all()
    return render(request, "edit_candidate.html", {"candidate": candidate, "elections": elections})

def delete_candidate(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    campaign_id = candidate.election.campaign.id
    candidate.delete()

    return redirect("manage_candidates", campaign_id=campaign_id)

def register_presiding_officer(request, manager_id):
    errors = {}

    # ✅ Ensure Election Manager ID exists
    manager = get_object_or_404(ElectionManager, id=manager_id)

    if request.method == "POST":
        id_number = request.POST["id_number"]
        profile_picture = request.FILES.get("profile_picture")
        fullname = request.POST["fullname"]
        username = request.POST["username"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST.get("confirm_password")  # ✅ Ensure confirm password is captured

        # ✅ Ensure ID Number is unique
        if PresidingOfficer.objects.filter(id_number=id_number).exists():
            errors["id_error"] = "ID number already exists."

        # ✅ Ensure Username is unique
        if PresidingOfficer.objects.filter(username=username).exists():
            errors["username_error"] = "Username already exists."

        # ✅ Ensure Email is unique
        if PresidingOfficer.objects.filter(email=email).exists():
            errors["email_error"] = "Email already registered."

        # ✅ Ensure Phone Number is unique
        if PresidingOfficer.objects.filter(phone_number=phone_number).exists():
            errors["phone_error"] = "Phone number already registered."

        # ✅ Ensure Full Name does not contain numbers
        if any(char.isdigit() for char in fullname):
            errors["fullname_error"] = "Full name should not contain numbers."

        # ✅ Ensure Password has at least 8 characters
        if len(password) < 8:
            errors["password_length"] = "Password must be at least 8 characters long."

        # ✅ Ensure Confirm Password matches Password
        if password != confirm_password:
            errors["password_error"] = "Passwords do not match."

        if errors:
            return render(request, "register_presiding_officer.html", {"errors": errors, "manager_id": manager_id})

        # ✅ Create and save Presiding Officer if no errors
        officer = PresidingOfficer.objects.create(
            id_number=id_number,
            profile_picture=profile_picture,
            fullname=fullname,
            username=username,
            phone_number=phone_number,
            email=email,
            created_by=manager,
            password=password,  # ✅ Hash this in production
        )

        messages.success(request, "Presiding Officer registered successfully.")
        return redirect("manager_dashboard", manager_id=manager.id)  # ✅ Redirect to Dashboard

    return render(request, "register_presiding_officer.html", {"manager_id": manager_id})

def register_presiding_officer_officer(request, manager_id):
    errors = {}

    # ✅ Ensure Election Manager ID exists
    manager = get_object_or_404(ElectionManager, id=manager_id)

    if request.method == "POST":
        id_number = request.POST["id_number"]
        profile_picture = request.FILES.get("profile_picture")
        fullname = request.POST["fullname"]
        username = request.POST["username"]
        phone_number = request.POST["phone_number"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST.get("confirm_password")  # ✅ Ensure confirm password is captured

        # ✅ Ensure ID Number is unique
        if PresidingOfficer.objects.filter(id_number=id_number).exists():
            errors["id_error"] = "ID number already exists."

        # ✅ Ensure Username is unique
        if PresidingOfficer.objects.filter(username=username).exists():
            errors["username_error"] = "Username already exists."

        # ✅ Ensure Email is unique
        if PresidingOfficer.objects.filter(email=email).exists():
            errors["email_error"] = "Email already registered."

        # ✅ Ensure Phone Number is unique
        if PresidingOfficer.objects.filter(phone_number=phone_number).exists():
            errors["phone_error"] = "Phone number already registered."

        # ✅ Ensure Full Name does not contain numbers
        if any(char.isdigit() for char in fullname):
            errors["fullname_error"] = "Full name should not contain numbers."

        # ✅ Ensure Password has at least 8 characters
        if len(password) < 8:
            errors["password_length"] = "Password must be at least 8 characters long."

        # ✅ Ensure Confirm Password matches Password
        if password != confirm_password:
            errors["password_error"] = "Passwords do not match."

        if errors:
            return render(request, "register_presiding_officer_officer.html", {"errors": errors, "manager_id": manager_id})

        # ✅ Create and save Presiding Officer if no errors
        officer = PresidingOfficer.objects.create(
            id_number=id_number,
            profile_picture=profile_picture,
            fullname=fullname,
            username=username,
            phone_number=phone_number,
            email=email,
            created_by=manager,
            password=password,  # ✅ Hash this in production
        )

        messages.success(request, "Presiding Officer registered successfully.")
        return redirect("officer_dashboard", manager_id=manager.id)  # ✅ Redirect to Dashboard

    return render(request, "register_presiding_officer_officer.html", {"manager_id": manager_id})

def presiding_officer_login(request):
    error_message = None

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            officer = PresidingOfficer.objects.get(username=username, password=password)
            return redirect("presiding_officer_dashboard", officer_id=officer.id)  # ✅ Redirect to dashboard if login successful
        except PresidingOfficer.DoesNotExist:
            error_message = "Invalid username or password. Please try again."

    return render(request, "presiding_officer_login.html", {"error_message": error_message})

def presiding_officer_dashboard(request, officer_id):
    try:
        officer = PresidingOfficer.objects.get(id=officer_id)
        campaigns = ElectionCampaign.objects.filter(manager=officer.created_by)  # ✅ Show only campaigns assigned to officer
    except PresidingOfficer.DoesNotExist:
        return render(request, "error.html", {"message": "Presiding Officer not found"})

    return render(request, "presiding_officer_dashboard.html", {
        "officer": officer,
        "campaigns": campaigns
    })

def logout_view(request):
    logout(request)  # ✅ Clears user session
    request.session.flush()  # ✅ Extra safety to clear all session data
    return redirect('index')

def manager_profile(request, manager_id):
    manager = get_object_or_404(ElectionManager, id=manager_id)

    if request.method == "POST":
        manager.fullname = request.POST.get("fullname")
        manager.username = request.POST.get("username")
        manager.phone_number = request.POST.get("phone_number")
        manager.email = request.POST.get("email")
        
        # Handle profile picture upload
        if "profile_picture" in request.FILES:
            manager.profile_picture = request.FILES["profile_picture"]

        # ✅ Password Change (if provided)
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        if new_password:
            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return render(request, "manager_profile.html", {"manager": manager})
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "manager_profile.html", {"manager": manager})
            
            manager.password = new_password  # ✅ Update password

        manager.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("manager_profile", manager_id=manager.id)

    return render(request, "manager_profile.html", {"manager": manager})



