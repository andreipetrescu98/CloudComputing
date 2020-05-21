from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from models.Advert import Advert

import os


def send_email(to, username, advert: Advert):
    subject = 'Advert assigned to your account'
    body = f"Hello {username},<br><br>You have selected the following advert:<br><br><b>{advert.description}</b><br>Date: " \
           f"{advert.start_date} - {advert.end_date}<br>Price: {advert.price} RON<br><br>" \
           f"Don't forget your appointment,<br><br>Best regards,<br>Cloud Computing Team"

    message = Mail(
        from_email='CloudComputingTeam@fii-cc.com',
        to_emails=to,
        subject=subject,
        html_content=body)
    try:
        with open(os.path.join(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'configs/sendgrid_key.txt'))) as f:
            api_key = f.read()
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    send_email('alin_c2007@yahoo.com', "Alin", Advert(description="ciobanesc german nu latra", start_date="12.01.2020", price=12))
