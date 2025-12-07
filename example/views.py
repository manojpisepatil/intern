# example/views.py
from datetime import datetime

from django.http import HttpResponse

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel to manoj 2221 !</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)




# from django.shortcuts import render
# from django.http import HttpResponse
# from django.core.mail import EmailMessage
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from io import BytesIO
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# from .forms import ContactForm



# def index_view(request):
#     """
#     Renders the home page with index.html.
#     """
#     return render(request, 'index.html')



# def contact_view(request):
#     """
#     Handles the contact form submission, processes user data, generates a personalized internship offer letter as a PDF,
#     and emails it to the candidate with detailed content.
#     """
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             # Retrieve form data
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             domain = form.cleaned_data['domain']

#             # Define domain-specific details
#             domain_details = {
#                 'digital_marketing': {
#                     'title': 'Digital Marketing Intern',
#                     'responsibilities': (
#                         'collaborating with the marketing team to devise innovative and data-driven social media strategies, '
#                         'overseeing the implementation of email marketing campaigns, and providing regular performance reports. '
#                         'You will also contribute to brainstorming creative content ideas for engagement across different platforms.'
#                     ),
#                 },
#                 'web_development': {
#                     'title': 'Web Development Intern',
#                     'responsibilities': (
#                         'working on the development and maintenance of user-friendly, visually appealing, and functional websites. '
#                         'You will focus on optimizing websites for speed and performance, implementing responsive designs, '
#                         'and collaborating with backend developers to ensure seamless integration of various systems.'
#                     ),
#                 },
#                 'data_analysis': {
#                     'title': 'Data Analysis Intern',
#                     'responsibilities': (
#                         'analyzing large and complex datasets to identify trends, patterns, and insights that can guide strategic decisions. '
#                         'Your work will involve preparing detailed reports, creating interactive dashboards, and presenting findings '
#                         'in a clear and compelling manner to stakeholders.'
#                     ),
#                 },
#             }
#             selected_domain = domain_details[domain]

#             # Calculate dates
#             today = datetime.today()
#             start_date = (today + relativedelta(months=1)).replace(day=1)  # First day of next month
#             end_date = start_date + relativedelta(months=1) - relativedelta(days=1)  # 1-month duration
#             start_date_str = start_date.strftime('%d %B %Y')
#             end_date_str = end_date.strftime('%d %B %Y')

#             # Email body
#             email_body = f"""
# Company Letterhead

# Welcome to the FierceLeap Technologies Internship Program.

# Date: {today.strftime('%d %B %Y')}

# 🎉 Congratulations,  {name}! 🎉

# Dear {name},

# We are delighted to inform you that you have been selected for the {selected_domain['title']} position. 
# We were highly impressed by your qualifications and enthusiasm to learn during the selection process, and we are excited to welcome you to our team.

# Your internship will commence on {start_date_str} and will continue until {end_date_str}.
# This is an unpaid internship. 
# Your work will be conducted remotely.

# During your internship, your responsibilities will include {selected_domain['responsibilities']}.
# You will work under the supervision of FierceLeap Technologies, who will guide, mentor, and support you throughout your internship.

# Please note that this offer letter does not guarantee full-time employment with the company. 
# However, based on your performance, you may receive a pre-placement offer.

# If you have any questions, feel free to contact us at FierceLeapTechnologies@gmail.com.

# Sincerely,

# FierceLeap Technologies

# """

#             # Generate PDF
#             buffer = BytesIO()
#             p = canvas.Canvas(buffer, pagesize=letter)

#             # Header: Add company logo
#             logo_path = "tezoraa.jpg"  # Replace with the actual path to your logo
#             try:
#                 p.drawImage(logo_path, inch, 10.5 * inch, width=2 * inch, height=1 * inch)
#             except Exception:
#                 p.setFont("Helvetica-Bold", 14)
#                 p.drawString(inch, 10.5 * inch, "FierceLeap Technologies")

#             # Title
#             p.setFont("Helvetica-Bold", 16)
#             p.drawString(2.5 * inch, 10.25 * inch, "INTERNSHIP OFFER LETTER")

#             # Main content
#             p.setFont("Helvetica", 10)
#             y_position = 9.75 * inch
#             content_lines = [
#                 f"Date: {today.strftime('%d/%m/%Y')} | ID: CS{today.strftime('%y%m%d')}{name[:2].upper()}",
#                 "",
#                 f"Dear {name},",
#                 "",
#                 f"We are excited to extend an offer for the position of {selected_domain['title']} at FierceLeap Technologies. "
#                 "This internship is designed to provide you with an enriching and transformative experience that will help you "
#                 "develop practical skills, build professional relationships, and advance your career aspirations.",
#                 "",
#                 f"The internship will begin on {start_date_str} and conclude on {end_date_str}, spanning a duration of one month.",
#                 "",
#                 "Key Responsibilities:",
#                 f"{selected_domain['responsibilities']}",
#                 "",
#                 "Throughout your internship, you will work closely with experienced mentors and team members who will guide you in "
#                 "navigating the challenges and seizing the opportunities presented by your role. We aim to create an environment that fosters "
#                 "collaboration, innovation, and continuous learning.",
#                 "",
#                 "Please note that this is an unpaid internship, and your work will be conducted remotely. It is essential that you have a laptop "
#                 "available for your daily tasks during the internship period.",
#                 "",
#                 "This offer letter does not guarantee full-time employment with FierceLeap Technologies; however, exceptional performance during your "
#                 "internship may result in a pre-placement offer for a future role within our organization.",
#                 "",
#                 "We are delighted to have you on board and are confident that you will make the most of this opportunity.",
#                 "",
#                 "Warm regards,",
#                 "",
#                 "FierceLeap Technologies",
#             ]

#             for line in content_lines:
#                 p.drawString(inch, y_position, line.strip())
#                 y_position -= 0.3 * inch

#             # Footer: Add branding image
#             footer_image_path = "footer_image.jpg"  # Replace with the actual path to your footer image
#             try:
#                 p.drawImage(footer_image_path, inch, 0.5 * inch, width=5.5 * inch, height=1.5 * inch)
#             except Exception:
#                 p.setFont("Helvetica", 10)
#                 p.drawString(inch, 0.5 * inch, "FierceLeap Technologies - Shaping Future Leaders")

#             # Finalize PDF
#             p.showPage()
#             p.save()
#             buffer.seek(0)

#             # Send Email
#             mail = EmailMessage(
#                 subject="Internship Offer Letter",
#                 body=email_body,
#                 from_email="your_email@gmail.com",
#                 to=[email],
#             )
#             mail.attach("InternshipOfferLetter.pdf", buffer.getvalue(), "application/pdf")
#             mail.send()

#             return HttpResponse("Thank you! Your internship offer letter has been sent.")
#     else:
#         form = ContactForm()

#     return render(request, 'contact.html', {'form': form})
