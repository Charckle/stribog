import smtplib, ssl
import imaplib
import email
from email.policy import default

import socket
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from os import environ 

import logging

from unidecode import unidecode
import re

logger = logging.getLogger(__name__)

class EmS:    
    smtp_server = None
    smtp_port = None
    smtp_sender_email = None
    smtp_password = None
    
    def __init__(self, settings_):
        self.smtp_server = settings_["smtp_server"]
        self.smtp_port = settings_["smtp_port"]
        self.smtp_sender_email = settings_["smtp_sender_email"]
        self.smtp_password = settings_["smtp_password"]            
        
    def check_conn(self):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.smtp_sender_email, self.smtp_password)
            return True, "OK"
        except Exception as e:
            # If any error occurs (e.g., connection error, authentication error), return False
            logger.critical(f"Error while testing the connection to the email server: {e}")
            return False, e
                
    
    def send_no_attach(self, receiver_email, subject, simple_text, html_text):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.smtp_sender_email
        message["To"] = receiver_email

        part1 = MIMEText(simple_text, "plain")
        part2 = MIMEText(html_text, "html")
        
        message.attach(part1)
        message.attach(part2)        
        
        # Create secure connection with server and send email
        
        success = False
        try:
            success = self.connect_smpt(receiver_email, message)
            
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected) as e:
            logger.error(f"SMTP connection error or authentication error: {e}")
        except (smtplib.SMTPAuthenticationError) as e:
            logger.error(f"SMTP connection error, timeouterror: {e}")
        except (socket.timeout) as e:
            logger.error(f"Socket connection error, timeouterror: {e}")
        except smtplib.SMTPRecipientsRefused:
            logger.warning(f"The recipient email address was refused. It may not exist.")
            success = "email_failed"
        except Exception as e:
            logger.error(f"Random error: {e}")
            
        return success
    

    def send_one_attach(self, receiver_email, subject, simple_text, html_text, attach):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.smtp_sender_email
        message["To"] = receiver_email

        part1 = MIMEText(simple_text, "plain")
        part2 = MIMEText(html_text, "html")
        
        message.attach(part1)
        message.attach(part2)
        
        attach_name = "Racun.pdf"
        part3 = MIMEBase("application", "octet-stream")
        part3.set_payload(attach)
        part3.add_header(
            "Content-Disposition",
            f"attachment; filename= {attach_name}",
        )        
        
        encoders.encode_base64(part3)
        
        message.attach(part3)
        
        # Create secure connection with server and send email

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.smtp_sender_email, self.smtp_password)
            server.sendmail(
                self.smtp_sender_email, receiver_email, message.as_string()
            )
    
    def send_multiple_attach(self, receiver_email, subject, simple_text, html_text, attachs):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.smtp_sender_email
        message["To"] = receiver_email

        part1 = MIMEText(simple_text, "plain")
        part2 = MIMEText(html_text, "html")
        
        message.attach(part1)
        message.attach(part2)

        
        for i in attachs:
            attach_name = self.get_valid_filename(i[0])
            file = i[1]
            part3 = MIMEBase("application", "octet-stream")
            part3.set_payload(file)
            part3.add_header(
                "Content-Disposition",
                f"attachment; filename={attach_name}",
            )
            encoders.encode_base64(part3)
            message.attach(part3)
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.smtp_sender_email, self.smtp_password)
            server.sendmail(
                self.smtp_sender_email, receiver_email, message.as_string()
            )
    
    def connect_smpt(self, receiver_email, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context, timeout=4) as server:
            server.login(self.smtp_sender_email, self.smtp_password)
            server.sendmail(
                self.smtp_sender_email, receiver_email, message.as_string()
            )
        return True        

    
    def connect_exchange_smpt(self, receiver_email, message):
        with smtplib.SMTP(self.exchange_smtp_server, self.exchange_port, timeout=4) as server:
            server.starttls()
            server.sendmail(
                self.smtp_sender_email, receiver_email, message.as_string()
            )            
        return True
    
    
    def get_valid_filename(self, s):
        """
        Stolen from Django, me thinks?
        Return the given string converted to a string that can be used for a clean
        filename. Remove leading and trailing spaces; convert other spaces to
        underscores; and remove anything that is not an alphanumeric, dash,
        underscore, or dot.
        >>> get_valid_filename("john's portrait in 2004.jpg")
        'johns_portrait_in_2004.jpg'
        """
    
        s = unidecode(str(s).strip().replace(' ', '_'))
    
        return re.sub(r'(?u)[^-\w.]', '', s)
    
    def check_not_delivered(self):
        # POPRAVI TO V WITH STATEMENT
        failed_recipients = []
        
        try:
            # Connect to the IMAP server
            mail = imaplib.IMAP4_SSL(self.smtp_server)
            mail.login(self.smtp_sender_email, self.smtp_password)
        
            # Select the mailbox you want to use
            mail.select("Inbox")
            
            #status, all_email_ids = mail.search(None, "ALL")
            status, bounced_email_ids = mail.search(None, 'UNSEEN OR SUBJECT "Mail delivery failed" SUBJECT "Warning: message"')

            if status != "OK":
                logger.warning(f"Status of email object after filtering undelivered in not OK")                
                return
            
            # Process each bounced email
            for email_id in bounced_email_ids[0].split():                # Fetch the email by ID
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status != "OK":
                    logger.debug(f"Failed to fetch email with ID: {email_id}")
                    continue
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        # Parse the raw email bytes
                        msg = email.message_from_bytes(response_part[1], policy=default)
                        
                        # Extract subject and other headers for debugging
                        #subject = msg["subject"]
                        #from_address = msg["from"]
                        failed_recipient = msg.get("X-Failed-Recipients", "No Failed Recipients")                        
                        #logger.debug(f"Bounce detected from {from_address}: {subject}")
                        failed_recipients.append(failed_recipient)
                        # email will be marked as READ
            
            # Logout and close the connection
            mail.logout()
            
        
        except imaplib.IMAP4.error as e:
            logger.error(f"IMAP error: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")    
            
        return failed_recipients
        