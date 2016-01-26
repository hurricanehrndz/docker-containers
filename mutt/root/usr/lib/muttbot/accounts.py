import os
import re
from messenger import Messenger

gmail_folders=['[Gmail]/Trash', 'INBOX', '[Gmail]/Drafts', '[Gmail]/Sent Mail', '[Gmail]/Important', '[Gmail]/Starred', '[Gmail]/All Mail', '[Gmail]/Spam']
local_folders=['trash', 'INBOX', 'drafts', 'sent', 'important', 'flagged',  'archive', 'spam']

class AccountsSetuper(object):
    def __init__(self):
        self._log = Messenger()

    def setup(self, email_accounts):
        accounts = ''
        other_emails = ''
        success = True
        home_dir = os.path.expanduser('~')
        mail_dir = os.path.join(home_dir, '.mail')
        mutt_dir = os.path.join(home_dir, '.mutt/')
        mbsync_config = os.path.join(home_dir, '.mbsyncrc')
        mbsync_writer = open(mbsync_config, 'a')
        mbsync_writer.write('Sync All\n')
        mbsync_writer.write('Expunge Both\n')
        mbsync_writer.close()

        # set up mbsyncrc
        for email_account in email_accounts:
            account_info = email_account.values()[0]
            account_name = email_account.keys()[0]
            accounts += ',' + account_name
            print 'Setting up ' + account_name
            # setup account for mbsync
            mbsync_writer = open(mbsync_config, 'a')
            mbsync_writer.write('IMAPAccount ' + account_name + '\n')
            mbsync_writer.write('Host ' + account_info['imap'] + '\n')
            mbsync_writer.write('User ' + account_info['user'] + '\n')
            mbsync_writer.write('Pass ' + account_info['pass'] + '\n')
            mbsync_writer.write('SSLType IMAPS\n')
            mbsync_writer.write('AuthMechs LOGIN\n')
            mbsync_writer.write('CertificateFile /var/lib/ca-certificates/ca-bundle.pem\n')
            mbsync_writer.write('\n')
            mbsync_writer.write('IMAPStore ' + account_name + '-remote\n')
            mbsync_writer.write('Account ' + account_name + '\n')
            mbsync_writer.write('\n')
            mbsync_writer.write('MaildirStore ' + account_name + '-local\n')
            mbsync_writer.write('Path ~/.mail/' + account_name + '/\n')
            mbsync_writer.write('Inbox ~/.mail/' + account_name + '/INBOX\n')
            mbsync_writer.write('Flatten .\n')
            mbsync_writer.write('\n')
            mbsync_writer.write('\n')

            add_patterns = ''
            for i in range (0, len(gmail_folders)):
                mbsync_writer.write('Channel ' + account_name + '-' + local_folders[i] + '\n')
                mbsync_writer.write('Master :' + account_name + '-remote:"' + gmail_folders[i] + '"\n')
                mbsync_writer.write('Slave :' + account_name + '-local:"' +  local_folders[i] + '"\n')
                mbsync_writer.write('Create Both\n')
                mbsync_writer.write('SyncState *\n')
                mbsync_writer.write('\n')
                add_patterns += '!' + local_folders[i] + '* '

            # Other folders
            mbsync_writer.write('Channel ' + account_name + '-default' + '\n')
            mbsync_writer.write('Master :' + account_name + '-remote:\n')
            mbsync_writer.write('Slave :' + account_name + '-local:\n')
            mbsync_writer.write('Create Both\n')
            mbsync_writer.write('SyncState *\n')
            mbsync_writer.write('Patterns * ![Gmail]* ' + add_patterns + '\n')
            mbsync_writer.write('\n')
            mbsync_writer.write('\n')



            mbsync_writer.write('Group ' + account_name + '-group\n')
            for i in range (0, len(gmail_folders)):
                mbsync_writer.write('Channel ' + account_name + '-' + local_folders[i] + '\n')
            mbsync_writer.write('Channel ' + account_name + '-default' + '\n')
            mbsync_writer.write('\n')
            mbsync_writer.write('\n')
            mbsync_writer.close()

            # Write mutt acount file that will be source
            muttacc_file= os.path.join(mutt_dir, account_name)
            f = open(muttacc_file, 'w')
            f.write('set from = "' + account_info['user'] + '"\n')
            f.write('set realname = "' + account_info['name'] + '"\n')
            f.write('set spoolfile = "+' + account_name + '/INBOX"\n')
            f.write('set mbox = "+' + account_name + '/archive"\n')
            f.write('set postponed = "+' + account_name + '/drafts"\n')
            f.write('set signature = ' + account_name + '.sig\n')
            f.write('set pgp_sign_as = ' + str(account_info['gpg']) + '\n')
            f.write('set sendmail = "/usr/bin/msmtp -a ' + account_name +  '"\n')
            f.write('set sendmail_wait = -1\n')
            f.write('unset record\n')
            f.write('set header_cache = ~/.mutt/cache/' + account_name +'/headers\n')
            f.write('set message_cachedir = ~/.mutt/cache/' + account_name +'/bodies\n')
            f.write('set certificate_file = ~/.mutt/cache/' + account_name +'/certificates\n')
            f.write('set nm_hidden_tags = "unread,drafts,flagged,INBOX,archive,important,' + account_name +'"\n')
            f.write('set my_account_tag = ' + account_name + '\n')
            f.write('source ~/.mutt/muttrc.folder.bindings\n')
            f.close

            # Create required folders and files for account
            if not os.path.exists(os.path.join(mutt_dir, 'cache/')):
                os.makedirs(os.path.join(mutt_dir, 'cache/' + account_name + '/headers'))
                os.makedirs(os.path.join(mutt_dir, 'cache/' + account_name + '/bodies'))
                open(os.path.join(mutt_dir, 'cache/' + account_name + '/certificates'), 'a').close()

            if not os.path.exists(os.path.join(mail_dir, account_name)):
                os.makedirs(os.path.join(mail_dir, account_name))

            # Save signature
            sigfile = os.path.join(mutt_dir, account_name + '.sig')
            f = open(sigfile, 'w' )
            f.write(account_info['signature'])
            f.close

            # add folder hooks to muttrc
            muttrc = os.path.join(mutt_dir, 'muttrc')
            f = open(muttrc, 'a')
            if email_account == email_accounts[0]:
                f.write('source ~/.mutt/' + account_name + '"\n')
            else:
                other_emails += account_info['user'] + ';'

            f.write('folder-hook tag:"' +  account_name + '" "source ~/.mutt/' + account_name + '"\n')
            f.close


            # setup msmtprc for sending mail
            msmtprc_file = os.path.join(home_dir, ".msmtprc")
            msmtprc = open(msmtprc_file, 'a')
            msmtprc.write('account ' + account_name + '\n')
            msmtprc.write('host ' + account_info['smtp'] + '\n')
            msmtprc.write('protocol smtp\n')
            msmtprc.write('auth on\n')
            msmtprc.write('from ' + account_info['user'] + '\n')
            msmtprc.write('user ' + account_info['user'] + '\n')
            msmtprc.write('password ' + account_info['pass'] + '\n')
            msmtprc.write('tls on\n')
            msmtprc.write('tls_trust_file /var/lib/ca-certificates/ca-bundle.pem\n')
            msmtprc.write('\n')
            msmtprc.close()

        #notmuch config
        notmuch_writer = open(os.path.join(home_dir, '.notmuch-config'), 'w')
        notmuch_writer.write('[database]\n')
        notmuch_writer.write('path=' + mail_dir + '\n')
        notmuch_writer.write('[new]\n')
        notmuch_writer.write('tags=new;\n')
        notmuch_writer.write('[user]\n')
        notmuch_writer.write('name=' + email_accounts[0].values()[0]['name'] + '\n')
        notmuch_writer.write('primary_email=' + email_accounts[0].values()[0]['user'] + '\n')
        notmuch_writer.write('other_email=' + other_emails + '\n')
        notmuch_writer.write('[maildir]\n')
        notmuch_writer.write('synchronize_flags=true\n')
        notmuch_writer.close()

        # edit kz.muttrc
        kz_muttrc =  os.path.join(home_dir, '.mutt/muttrc.kz')
        with open(kz_muttrc, "r") as kz:
            lines = kz.readlines()
        with open(kz_muttrc, "w") as kz:
            for line in lines:
                kz.write(re.sub(r'/home/user_name/.mail',mail_dir, line))
        return success

class SetupError(Exception):
    pass
