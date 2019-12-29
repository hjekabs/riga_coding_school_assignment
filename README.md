##### Riga coding school final project #####

Simple python script to automate some simple data manipulations from gmail attachments and sending them further to another email.

NOTE: project setup to work only for my email and only for .csv file attachments

For now the script is very simple:
- proccesses all emails and looks for attachments
- processes only .csv files
- does simple data manipulations
- sends an email with empty subjct and body, only the attachment

But can be easily adjusted to:
- look for specific e-mails (by date, subject, sender, body text, etc)
- proccess not only .csv files but also excel, etc.
- make scheduled tasks, the script checks the email at certain times or at a time interval
- instead of specifying in and out file directories, we could use temporary directories