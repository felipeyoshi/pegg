import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(smtp_recipient, smtp_title, smtp_body, smtp_credentials, pdf_stream=None):

    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = smtp_title
    msg['From'] = smtp_credentials['SMTP_SENDER']
    msg['To'] = smtp_recipient

    # Add the HTML part
    html_part = MIMEText(smtp_body, 'html')
    msg.attach(html_part)

    # Attach the PDF if provided
    if pdf_stream:
        # Create a MIMEBase object and set the appropriate headers
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(pdf_stream.getvalue())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment; filename=report.pdf')
        msg.attach(attachment)

    s = smtplib.SMTP(smtp_credentials['SMTP_SERVER'], int(smtp_credentials['SMTP_PORT']))
    s.set_debuglevel(0)
    s.login(smtp_credentials['SMTP_USER'], smtp_credentials['SMTP_PASSWORD'])
    response = s.sendmail(smtp_credentials['SMTP_SENDER'], smtp_recipient, msg.as_string())
    if not response:
        print("Email was accepted for delivery.")
    else:
        print("There was an issue:", response)
    s.quit()

    return True