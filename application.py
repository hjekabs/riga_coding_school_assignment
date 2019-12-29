import smtplib
import imaplib
import email
from email import message_from_string
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os
import csv

##### CONSTANTS #####
MY_USERNAME = "jekabs.demo@gmail.com"
MY_PASSWORD = "iewkwzxkigdiqzcg"
SSL_PORT = 993
SSL_HOST = "imap.gmail.com"
IN_FILE_DIRECTORY = "/Users/jekabs/python-course/FINAL_PROJECT/infiles"
OUT_FILE_DIRECTORY = "/Users/jekabs/python-course/FINAL_PROJECT/outfiles"
#####################

def download_email_attachments(ssl_host, ssl_port, username, password, download_path):
    print("Checking email for attachments...")
    print("#"*30)
    # create imaplib connection
    mail = imaplib.IMAP4_SSL(ssl_host, ssl_port)
    # log in into gmail
    mail.login(username, password)
    mail.select("inbox")
    type, mails = mail.search(None, 'ALL')
    mail_ids = mails[0].decode("utf-8")
    mail_id_list = mail_ids.split()
    # RFC822 is some sort of protocol
    for mail_id in mail_id_list:
        raw_email = mail.fetch(mail_id, '(RFC822)')[1][0]
        # Convert from bytes to string and select the email content
        raw_email_string = [line.decode("utf-8") for line in raw_email][1]

        email_message = message_from_string(raw_email_string)

        for part in email_message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is None:
                continue
            # get the file name
            fileName = part.get_filename()
            
            if fileName:
                filePath = os.path.join(download_path, fileName)

                if not os.path.isfile(filePath):
                    print(f"Downloading {fileName}...")
                    print("*"*10)
                    with open(filePath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                else:
                    print(f"File {fileName} has already been downloaded")
                    print("*"*10)

def get_csv_files(file_path):
    all_files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    return all_files

def create_csv_report(infile, in_file_directory, out_file_directory):
    stock_profits = []
    with open(os.path.join(in_file_directory, infile)) as f:
        csv_file = csv.DictReader(f)
        for row in csv_file:
            buy_price = int(row["buy_price"])
            sell_price = int(row["sell_price"])
            profit = sell_price - buy_price
            stock_profits.append([row.get("name"), profit])

    with open(os.path.join(out_file_directory, f"profit_{infile}"), "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["stock_name", "profit"])
        for stock in stock_profits:
            csv_writer.writerow(stock)

def send_report_email(username, password, out_file_directory):
    csv_files = get_csv_files(out_file_directory)
    msg = MIMEMultipart()
    for csv in csv_files:
        with open(os.path.join(out_file_directory, csv)) as f:
            record = MIMEBase("application", "octet-stream")
            record.set_payload(f.read())
            encoders.encode_base64(record)
            record.add_header("Content-Disposition", "attachment", filename=csv)
        
        msg.attach(record)

    try:
        print(f"Trying to send email from {username} to {username}")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(username, username, msg.as_string())
        # ...send emails
    except Exception as ex:
        print("Failed to send email")
        print(ex)

download_email_attachments(SSL_HOST, SSL_PORT, MY_USERNAME, MY_PASSWORD, IN_FILE_DIRECTORY)

csv_file_list = get_csv_files(IN_FILE_DIRECTORY)

for csv_file in csv_file_list:
    print(f"Creating profit report for file {csv_file}")
    print("-"*10)
    create_csv_report(csv_file, IN_FILE_DIRECTORY, OUT_FILE_DIRECTORY)
    print(f"Profit report for file {csv_file} - SUCCESS")
    print("-"*10)

send_report_email(MY_USERNAME, MY_PASSWORD, OUT_FILE_DIRECTORY)





