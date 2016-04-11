#!/usr/bin/python2
# Based on: https://bbs.archlinux.org/viewtopic.php?pid=962423#p962423
# This version is modified to handle mailboxes with spaces in the names

import pyinotify
import os
from mailbox import MaildirMessage
from email.header import decode_header

maildir = os.path.join('/home/' + os.environ.get('APP_USER'), '.mail')
# Get email accounts
accounts = filter( lambda f: not f.startswith('.'), os.listdir(maildir))
notifciation_dir = os.path.join('/home/' + os.environ.get('APP_USER'), '/.notifications')
if not os.path.exists(notification_dir):
    os.makedirs(notification_dir)
fnotify = os.path.join('/home/' + os.environ.get('APP_USER'), '/.notifications/email')

pynotify.init(r'email_notifier.py')

def newfile(event):
    fd = open(event.pathname, 'r')
    mail = MaildirMessage(message=fd)
    From = "From:" + dec_header(mail['From'])
    Subject = "Subject:" + dec_header(mail['Subject'])
    fd.close()
    try:
        f = open(fnotify, 'a')
        f.write('mutt' + ' ' + From + ' ' + Subject + '\n')
        f.close
    except:
        print "Unexpected error:", sys.exc_info()[0]

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, newfile)

for account in accounts:
    boxes = os.listdir(os.path.join(maildir, account))
    for box in boxes:
        wm.add_watch(os.path.join(maildir,account,box,new), pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO)

notifier.loop()
