from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import EmailMessage

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from io import BytesIO
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

from .forms import ContactForm
from .models import ScheduledEmail


# ================= HOME PAGE =================
def index_view(request):
    return render(request, 'index.html')


# ================= CONTACT FORM =================
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            domain = form.cleaned_data['domain']

            domain_details = {
                'digital_marketing': {
                    'title': 'Digital Marketing Intern',
                    'responsibilities': (
                        'Working with marketing campaigns, social media strategies, '
                        'email marketing, and performance analysis.'
                    ),
                },
                'web_development': {
                    'title': 'Web Development Intern',
                    'responsibilities': (
                        'Developing responsive websites, improving performance, '
                        'and collaborating with backend developers.'
                    ),
                },
                'data_analysis': {
                    'title': 'Data Analysis Intern',
                    'responsibilities': (
                        'Analyzing datasets, preparing reports, and creating dashboards.'
                    ),
                },
            }

            selected_domain = domain_details[domain]

            today = datetime.today()
            start_date = (today + relativedelta(months=1)).replace(day=1)
            end_date = start_date + relativedelta(months=1) - relativedelta(days=1)

            # ================= EMAIL BODY =================
            email_body = f"""
Company Letterhead

Congratulations {name} 🎉

You have been selected for the position of {selected_domain['title']}.

Internship Duration:
Start Date: {start_date.strftime('%d %B %Y')}
End Date: {end_date.strftime('%d %B %Y')}

Mode: Remote
Type: Unpaid Internship

Responsibilities:
{selected_domain['responsibilities']}

Regards,
FierceLeap Technologies
"""

            # ================= PDF GENERATION =================
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, 750, "INTERNSHIP OFFER LETTER")

            p.setFont("Helvetica", 11)
            p.drawString(100, 710, f"Candidate Name: {name}")
            p.drawString(100, 690, f"Position: {selected_domain['title']}")
            p.drawString(100, 670, f"Start Date: {start_date.strftime('%d %B %Y')}")
            p.drawString(100, 650, f"End Date: {end_date.strftime('%d %B %Y')}")

            p.drawString(100, 620, "Congratulations! We are happy to have you onboard.")

            p.showPage()
            p.save()
            buffer.seek(0)
            # ===================================================

            # ================= SCHEDULE EMAIL =================
            send_time = today + timedelta(days=15)  # ⏰ change if needed

            ScheduledEmail.objects.create(
                name=name,
                email=email,
                subject="Internship Offer Letter",
                body=email_body,
                pdf=buffer.getvalue(),
                send_at=send_time
            )
            # ===================================================

            return HttpResponse(
                "Thank you! Your internship offer letter will be emailed to you shortly."
            )

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# ================= CRON EMAIL SENDER =================
@csrf_exempt
def send_scheduled_emails(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=405)

    # 🔐 Security check
    if request.headers.get("X-CRON-TOKEN") != os.environ.get("CRON_SECRET"):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    now = timezone.now()
    emails = ScheduledEmail.objects.filter(sent=False, send_at__lte=now)

    sent_count = 0

    for e in emails:
        mail = EmailMessage(
            subject=e.subject,
            body=e.body,
            from_email="your_email@gmail.com",
            to=[e.email],
        )
        mail.attach("InternshipOfferLetter.pdf", e.pdf, "application/pdf")
        mail.send()

        e.sent = True
        e.save()
        sent_count += 1

    return JsonResponse({"sent": sent_count})
