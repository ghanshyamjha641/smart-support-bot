from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chat

import json
import nltk

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download NLTK Data (Run First Time)
nltk.download('punkt')
nltk.download('punkt_tab')

# Stemmer Object
ps = PorterStemmer()

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def get_response(request):

    if request.method == "POST":

        try:

            # Load JSON Data
            data = json.loads(request.body)

            # User Message
            user_message = data.get("message", "").lower()

            # NLP Tokenization
            tokens = word_tokenize(user_message)
           

            # Stemming
            tokens = [ps.stem(word) for word in tokens]
            print("Original:", user_message)
            print("Tokens:", tokens)
            # ---------------- GREETING ---------------- #

            greeting_words = [ps.stem(word) for word in [
                "hello", "hi", "hey", "hlo", "hy"
            ]]

            if any(word in tokens for word in greeting_words):

                response = """
                <b>Welcome to Smart Support Bot 🎓</b><br><br>

                I can help you with:<br><br>

                • Admission<br>
                • Courses<br>
                • Fees<br>
                • Placements<br>
                • Hostel<br>
                • Scholarships<br>
                • Contact Information<br>
                • Exams
                """

            # ---------------- ADMISSION ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "admission", "admissions",
                "apply", "enrollment", "adm"
            ]]):

                response = """
                <b>Admissions Open 🎓</b><br><br>

                Available Programs:<br><br>

                • BCA<br>
                • MCA<br>
                • MBA<br>
                • MSc Programs<br><br>

                <b>Required Documents:</b><br><br>

                • 10th Marksheet<br>
                • 12th Marksheet<br>
                • Graduation Certificate<br>
                • ID Proof
                """

            # ---------------- COURSES ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "course", "courses",
                "program", "programs",
                "bca", "mca", "mba", "msc"
            ]]):

                response = """
                <b>Courses Offered 📚</b><br><br>

                • BCA → Bachelor of Computer Applications<br>
                • MCA → Master of Computer Applications<br>
                • MBA → Master of Business Administration<br>
                • MSc DS → Master of Science in Data Science<br><br>

                These programs include:<br><br>

                • Industry-focused curriculum<br>
                • Practical labs<br>
                • Placement assistance<br>
                • Experienced faculty
                """

            # ---------------- FEES ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "fee", "fees",
                "payment", "payments"
            ]]):

                response = """
                <b>Course Fees 💳</b><br><br>

                • MCA → ₹80,000<br>
                • BCA → ₹60,000<br>
                • MBA → ₹1,20,000<br>
                • MSc → ₹90,000<br><br>

                Installment facility is available.
                """

            # ---------------- PLACEMENT ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "placement", "placements",
                "job", "jobs",
                "company", "companies"
            ]]):

                response = """
                <b>Placement Information 💼</b><br><br>

                Top Recruiters:<br><br>

                • TCS<br>
                • Infosys<br>
                • Wipro<br>
                • Accenture<br>
                • Cognizant<br><br>

                Placement training and mock interviews are also provided.
                """

            # ---------------- HOSTEL ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "hostel", "hostels",
                "room", "rooms",
                "accommodation"
            ]]):

                response = """
                <b>Hostel Facilities 🏨</b><br><br>

                • WiFi<br>
                • Mess Facility<br>
                • Laundry<br>
                • 24x7 Security<br>
                • Study Rooms
                """

            # ---------------- SCHOLARSHIP ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "scholarship", "scholarships",
                "financial", "aid"
            ]]):

                response = """
                <b>Scholarship Information 🎓</b><br><br>

                Scholarships are available for:<br><br>

                • Merit Students<br>
                • Sports Quota<br>
                • Financially Weak Students
                """

            # ---------------- LIBRARY ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "library", "libraries",
                "book", "books"
            ]]):

                response = """
                <b>Library Facilities 📖</b><br><br>

                • Digital Library<br>
                • Research Journals<br>
                • Reading Hall<br>
                • Computer Labs
                """

            # ---------------- EXAMS ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "exam", "exams",
                "result", "results",
                "semester", "semesters"
            ]]):

                response = """
                <b>Examination Information 📝</b><br><br>

                Students can check:<br><br>

                • Results<br>
                • Admit Cards<br>
                • Exam Schedule<br><br>

                through the student portal.
                """

            # ---------------- CONTACT ---------------- #

            elif any(word in tokens for word in [ps.stem(w) for w in [
                "contact", "contacts",
                "phone", "mobile",
                "email"
            ]]):

                response = """
                <b>Contact Information 📞</b><br><br>

                Phone: +91 9999999999<br>
                Email: support@cu-support.edu<br>
                Website: www.cu-support.edu
                """

            # ---------------- DEFAULT ---------------- #

            else:

                response = """
                <b>Sorry ❌</b><br><br>

                I could not understand your query.<br><br>

                Please ask about:<br><br>

                • Admission<br>
                • Courses<br>
                • Fees<br>
                • Placements<br>
                • Hostel<br>
                • Scholarships<br>
                • Contact Information<br>
                • Exams
                """

            # Save Chat in Database
            Chat.objects.create(
                user_message=user_message,
                bot_response=response
            )

            # Return Response
            return JsonResponse({
                "response": response
            })

        except Exception as e:

            return JsonResponse({
                "response": f"Error: {str(e)}"
            })

    return JsonResponse({
        "response": "Invalid Request"
    })

