from google.appengine.api import mail


def send_welcome_email(user):
    from_address = 'contact@ctrl-class.appspotmail.com'
    subject = 'Contact from ctrl-class'
    body = 'Welcome to ctrl-class! Take control over your courses and projects.\n\
             Questions? Contact us at contact@ctrl-class.appspotmail.com. \n\n\
             -The ctrl-class team'
    mail.send_mail(from_address, user.email, subject, body)
