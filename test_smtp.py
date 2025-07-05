import smtplib

# Replace with your real email for testing
recipient = 'YOUR_EMAIL@gmail.com'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login('minecrafterusergame@gmail.com', 'lukojehfetcplftj')
server.sendmail(
    'minecrafterusergame@gmail.com',
    recipient,
    'Subject: Test\n\nThis is a test email.'
)
server.quit()
print('Sent!') 