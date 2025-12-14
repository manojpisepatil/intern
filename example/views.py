from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .forms import ContactForm


def index_view(request):
    """Renders the home page."""
    return render(request, 'index.html')


def contact_view(request):
    """Handles contact form, generates PDF offer letter, and sends it via email immediately."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            domain = form.cleaned_data['domain']

            # Domain-specific details
            domain_details = {
                'digital_marketing': {
                    'title': 'Digital Marketing Intern',
                    'responsibilities': (
                        'collaborating with the marketing team to devise innovative and data-driven social media strategies, '
                        'overseeing the implementation of email marketing campaigns, and providing regular performance reports. '
                        'You will also contribute to brainstorming creative content ideas for engagement across different platforms.'
                    ),
                },
                'web_development': {
                    'title': 'Web Development Intern',
                    'responsibilities': (
                        'working on the development and maintenance of user-friendly, visually appealing, and functional websites. '
                        'You will focus on optimizing websites for speed and performance, implementing responsive designs, '
                        'and collaborating with backend developers to ensure seamless integration of various systems.'
                    ),
                },
                'data_analysis': {
                    'title': 'Data Analysis Intern',
                    'responsibilities': (
                        'analyzing large and complex datasets to identify trends, patterns, and insights that can guide strategic decisions. '
                        'Your work will involve preparing detailed reports, creating interactive dashboards, and presenting findings '
                        'in a clear and compelling manner to stakeholders.'
                    ),
                },
            }
            selected_domain = domain_details[domain]

            # Calculate internship dates
            today = datetime.today()
            start_date = (today + relativedelta(months=1)).replace(day=1)
            end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
            start_date_str = start_date.strftime('%d %B %Y')
            end_date_str = end_date.strftime('%d %B %Y')

            # Email body text
            email_body = f"""
Company Letterhead

Welcome to the FierceLeap Technologies Internship Program.

Date: {today.strftime('%d %B %Y')}

🎉 Congratulations, {name}! 🎉

Dear {name},

We are delighted to inform you that you have been selected for the {selected_domain['title']} position. 
We were highly impressed by your qualifications and enthusiasm to learn during the selection process, and we are excited to welcome you to our team.

Your internship will commence on {start_date_str} and will continue until {end_date_str}.
This is an unpaid internship. 
Your work will be conducted remotely.

During your internship, your responsibilities will include:
{selected_domain['responsibilities']}

You will work under the supervision of FierceLeap Technologies, who will guide, mentor, and support you throughout your internship.

Please note that this offer letter does not guarantee full-time employment with the company. 
However, based on your performance, you may receive a pre-placement offer.

If you have any questions, feel free to contact us at FierceLeapTechnologies@gmail.com.

Sincerely,

FierceLeap Technologies
"""

            # Generate PDF
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            # Header logo (fallback to text if image missing)
            logo_path = "static/tezoraa.jpg"  # Adjust path if needed
            try:
                p.drawImage(logo_path, inch, height - 1.5*inch, width=2*inch, height=1*inch, preserveAspectRatio=True)
            except Exception:
                p.setFont("Helvetica-Bold", 14)
                p.drawString(inch, height - inch, "FierceLeap Technologies")

            # Title
            p.setFont("Helvetica-Bold", 18)
            p.drawCentredString(width / 2, height - 2*inch, "INTERNSHIP OFFER LETTER")

            # Content
            p.setFont("Helvetica", 11)
            y = height - 3*inch
            lines = [
                f"Date: {today.strftime('%d %B %Y')} | ID: CS{today.strftime('%y%m%d')}{name[:3].upper()}",
                "",
                f"Dear {name},",
                "",
                f"We are excited to extend an offer for the position of {selected_domain['title']} at FierceLeap Technologies.",
                "This internship is designed to provide you with an enriching and transformative experience.",
                "",
                f"The internship will begin on {start_date_str} and conclude on {end_date_str}.",
                "",
                "Key Responsibilities:",
                selected_domain['responsibilities'],
                "",
                "You will work remotely and receive mentorship throughout.",
                "",
                "This is an unpaid internship. Exceptional performance may lead to a pre-placement offer.",
                "",
                "Warm regards,",
                "",
                "FierceLeap Technologies",
            ]

            for line in lines:
                p.drawString(inch, y, line)
                y -= 0.25 * inch
                if y < inch:
                    p.showPage()
                    y = height - inch

            # Footer image (fallback to text)
            footer_path = "static/footer_image.jpg"
            try:
                p.drawImage(footer_path, inch, 0.5*inch, width=width-2*inch, height=1.5*inch)
            except Exception:
                p.setFont("Helvetica-Oblique", 10)
                p.drawString(inch, 0.7*inch, "FierceLeap Technologies - Shaping Future Leaders")

            p.showPage()
            p.save()
            buffer.seek(0)

            # Send email with PDF attached
            mail = EmailMessage(
                subject="Internship Offer Letter - FierceLeap Technologies",
                body=email_body,
                from_email=settings.EMAIL_HOST_USER,
                to=[email],
            )
            mail.attach("InternshipOfferLetter.pdf", buffer.getvalue(), "application/pdf")
            mail.send()

            return HttpResponse("Thank you! Your internship offer letter has been sent to your email.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
