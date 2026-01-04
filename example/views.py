from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from io import BytesIO
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from .forms import ContactForm
from .models import ScheduledEmail


def index_view(request):
    return render(request, 'index.html', {'form': form})


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
                    'responsibilities': 'Working with marketing campaigns, social media strategies, email marketing, and performance analysis.',
                },
                'web_development': {
                    'title': 'Web Development Intern',
                    'responsibilities': 'Developing responsive websites, improving performance, and collaborating with backend developers.',
                },
                'data_analysis': {
                    'title': 'Data Analysis Intern',
                    'responsibilities': 'Analyzing datasets, preparing reports, and creating dashboards.',
                },
            }

            selected_domain = domain_details[domain]

            today = timezone.now()
            start_date = (today + relativedelta(months=1)).replace(day=1)
            end_date = start_date + relativedelta(months=1) - relativedelta(days=1)

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

            send_time = today + timedelta(days=15)

            ScheduledEmail.objects.create(
                name=name,
                email=email,
                subject="Internship Offer Letter",
                body=email_body,
                pdf=buffer.getvalue(),
                send_at=send_time
            )

            return HttpResponse(
                "Thank you! Your internship offer letter will be emailed to you shortly."
            )
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


@csrf_exempt
def send_scheduled_emails(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if request.headers.get("X-CRON-TOKEN") != os.environ.get("CRON_SECRET"):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    now = timezone.now()
    due_emails = ScheduledEmail.objects.filter(sent=False, send_at__lte=now)

    sent_count = 0
    for email_obj in due_emails:
        try:
            mail = EmailMessage(
                subject=email_obj.subject,
                body=email_obj.body,
                from_email=settings.EMAIL_HOST_USER,
                to=[email_obj.email],
            )
            mail.attach("InternshipOfferLetter.pdf", email_obj.pdf, "application/pdf")
            mail.send(fail_silently=False)
            email_obj.sent = True
            email_obj.save()
            sent_count += 1
        except Exception:
            pass

    return JsonResponse({"status": "success", "emails_sent": sent_count})
