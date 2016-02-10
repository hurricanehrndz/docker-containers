import os
import re
from messenger import Messenger

gmail_remote_folders=['[Gmail]/Trash', 'INBOX', '[Gmail]/Drafts', '[Gmail]/Sent Mail', '[Gmail]/Important', '[Gmail]/Starred', '[Gmail]/All Mail', '[Gmail]/Spam']
gmail_local_folders=['trash', 'INBOX', 'drafts', 'sent', 'important', 'flagged',  'archive', 'spam']
exchange_folders=['Trash', 'Inbox', 'Drafts', 'Sent', 'Junk']
exchange_local_folders=['trash', 'INBOX', 'drafts', 'sent', 'spam']
exchange_ignore_folders=['"Unsent Messages"', '"Your feeds"', '"Sent Issues"']

class AccountsSetuper(object):
    def __init__(self):
        self._log = Messenger()
        self._home_dir = os.path.expanduser('~')
        self._mail_dir = os.path.join(home_dir, '.mail')
        self._mutt_dir = os.path.join(home_dir, '.mutt/')
        self._mbsync_config = os.path.join(home_dir, '.mbsyncrc')
        self._msmtprc_config = os.path.join(home_dir, ".msmtprc")
        self._other_emails = ''

    def setup_gmail(self, account_name, account_info):
        print 'Setting up ' + account_name
        # setup account for mbsync
        mbsyncrc = open(self._mbsync_config, 'a')
        mbsyncrc.write('IMAPAccount ' + account_name + '\n')
        mbsyncrc.write('Host ' + account_info['imap'] + '\n')
        mbsyncrc.write('User ' + account_info['user'] + '\n')
        mbsyncrc.write('Pass ' + account_info['pass'] + '\n')
        mbsyncrc.write('SSLType IMAPS\n')
        mbsyncrc.write('AuthMechs LOGIN\n')
        mbsyncrc.write('CertificateFile /var/lib/ca-certificates/ca-bundle.pem\n')
        mbsyncrc.write('\n')
        mbsyncrc.write('IMAPStore ' + account_name + '-remote\n')
        mbsyncrc.write('Account ' + account_name + '\n')
        mbsyncrc.write('\n')
        mbsyncrc.write('MaildirStore ' + account_name + '-local\n')
        mbsyncrc.write('Path ~/.mail/' + account_name + '/\n')
        mbsyncrc.write('Inbox ~/.mail/' + account_name + '/INBOX\n')
        mbsyncrc.write('Flatten .\n')
        mbsyncrc.write('\n')
        mbsyncrc.write('\n')

        add_patterns = ''
        for i in range (0, len(gmail_folders)):
            mbsyncrc.write('Channel ' + account_name + '-' + local_folders[i] + '\n')
            mbsyncrc.write('Master :' + account_name + '-remote:"' + gmail_folders[i] + '"\n')
            mbsyncrc.write('Slave :' + account_name + '-local:"' +  local_folders[i] + '"\n')
            mbsyncrc.write('Create Both\n')
            mbsyncrc.write('SyncState *\n')
            mbsyncrc.write('\n')
            add_patterns += '!' + gmail_local_folders[i] + '* '

        # Other folders
        mbsyncrc.write('Channel ' + account_name + '-default' + '\n')
        mbsyncrc.write('Master :' + account_name + '-remote:\n')
        mbsyncrc.write('Slave :' + account_name + '-local:\n')
        mbsyncrc.write('Create Both\n')
        mbsyncrc.write('SyncState *\n')
        mbsyncrc.write('Patterns * ![Gmail]* ' + add_patterns + '\n')
        mbsyncrc.write('\n')
        mbsyncrc.write('\n')

        mbsyncrc.write('Group ' + account_name + '-group\n')
        for i in range (0, len(gmail_remote_folders)):
            mbsyncrc.write('Channel ' + account_name + '-' + gmail_local_folders[i] + '\n')
        mbsyncrc.write('Channel ' + account_name + '-default' + '\n')
        mbsyncrc.write('\n')
        mbsyncrc.write('\n')
        mbsyncrc.close()

    def write_account_muttrc(self, account_name, account_info):
        # Write mutt acount file that will be source
        account_muttrc = open(os.path.join(self._mutt_dir, account_name), 'w')
        account_muttrc.write('set from = "' + account_info['email'] + '"\n')
        account_muttrc.write('set realname = "' + account_info['name'] + '"\n')
        account_muttrc.write('set spoolfile = "+' + account_name + '/INBOX"\n')
        account_muttrc.write('set mbox = "+' + account_name + '/archive"\n')
        account_muttrc.write('set postponed = "+' + account_name + '/drafts"\n')
        account_muttrc.write('set signature = ' + account_name + '.sig\n')
        account_muttrc.write('set pgp_sign_as = ' + str(account_info['gpg']) + '\n')
        account_muttrc.write('my_hdr OpenPGP: id=' + str(account_info['gpg'])[2:] + ' \n')
        account_muttrc.write('set sendmail = "/usr/bin/msmtp -a ' + account_name +  '"\n')
        account_muttrc.write('set sendmail_wait = -1\n')
        account_muttrc.write('unset record\n')
        account_muttrc.write('set header_cache = ~/.mutt/cache/' + account_name +'/headers\n')
        account_muttrc.write('set message_cachedir = ~/.mutt/cache/' + account_name +'/bodies\n')
        account_muttrc.write('set certificate_file = ~/.mutt/cache/' + account_name +'/certificates\n')
        account_muttrc.write('set nm_hidden_tags = "unread,drafts,flagged,INBOX,archive,important,' + account_name +'"\n')
        account_muttrc.write('set my_account_tag = ' + account_name + '\n')
        account_muttrc.write('source ~/.mutt/muttrc.folder.bindings\n')
        account_muttrc.close

    def write_signature(self, account_name, account_info):
        # Save signature
        signature = open(os.path.join(self._mutt_dir, account_name + '.sig'), 'w' )
        signature.write(account_info['signature'])
        signature.close

    def create_mail_dirs(self, account_name):
        # Create required folders and files for account
        if not os.path.exists(os.path.join(self._mutt_dir, 'cache/')):
            os.makedirs(os.path.join(mutt_dir, 'cache/' + account_name + '/headers'))
            os.makedirs(os.path.join(mutt_dir, 'cache/' + account_name + '/bodies'))
            open(os.path.join(mutt_dir, 'cache/' + account_name + '/certificates'), 'a').close()

        if not os.path.exists(os.path.join(self._mail_dir, account_name)):
            os.makedirs(os.path.join(self._mail_dir, account_name))

    def append_sync_cmd(self, account_name):
        # sync cmds
        sync_cmds = open(os.path.join(self._home_dir, 'sync_cmds'), 'a')
        sync_cmds.write('/usr/lib/mutt/maildir-notmuch-sync ' + os.path.join(self._mail_dir, account_name) + '\n')
        sync_cmds.close()

    def append_msmtprc_config(self, account_name, account_info):
        # setup msmtprc for sending mail
        msmtprc = open(os.path.join(self._home_dir, ".msmtprc"), 'a')
        msmtprc.write('account ' + account_name + '\n')
        msmtprc.write('host ' + account_info['smtp'] + '\n')
        msmtprc.write('protocol smtp\n')
        msmtprc.write('auth on\n')
        msmtprc.write('from ' + account_info['email'] + '\n')
        msmtprc.write('user ' + account_info['user'] + '\n')
        msmtprc.write('password ' + account_info['pass'] + '\n')
        msmtprc.write('tls on\n')
        msmtprc.write('tls_trust_file /var/lib/ca-certificates/ca-bundle.pem\n')
        msmtprc.write('\n')
        msmtprc.close()

    def append_folderhooks_to_muttrc(self, email_account, email_accounts):
        # add folder hooks to muttrc
        muttrc = open(os.path.join(self._mutt_dir, 'muttrc'), 'a')
        if email_account == email_accounts[0]:
            muttrc.write('source ~/.mutt/' + account_name + '"\n')
        else:
            self._other_emails += account_info['email'] + ';'

        muttrc.write('folder-hook tag:"' +  account_name + '" "source ~/.mutt/' + account_name + '"\n')
        muttrc.close

    def write_notmuch_config(self, email_accounts):
        #notmuch config
        notmuch_config = open(os.path.join(self._home_dir, '.notmuch-config'), 'w')
        notmuch_config.write('[database]\n')
        notmuch_config.write('path=' + self._mail_dir + '\n')
        notmuch_config.write('[new]\n')
        notmuch_config.write('tags=new;\n')
        notmuch_config.write('[user]\n')
        notmuch_config.write('name=' + email_accounts[0].values()[0]['name'] + '\n')
        notmuch_config.write('primary_email=' + email_accounts[0].values()[0]['email'] + '\n')
        notmuch_config.write('other_email=' + self._other_emails + '\n')
        notmuch_config.write('[maildir]\n')
        notmuch_config.write('synchronize_flags=true\n')
        notmuch_config.close()

    def update_kz_muttrc(self):
        # update maildir in muttrc.kz
        kz_muttrc =  os.path.join(self._mutt_dir, 'muttrc.kz')
        with open(kz_muttrc, "r") as kz:
            lines = kz.readlines()
        with open(kz_muttrc, "w") as kz:
            for line in lines:
                kz.write(re.sub(r'/home/user_name/.mail',self._mail_dir, line))

    def setup(self, email_accounts):
        other_emails = ''
        success = True
        mbsyncrc = open(self._mbsync_config, 'a')
        mbsyncrc.write('Sync All\n')
        mbsyncrc.write('Expunge Both\n')
        mbsyncrc.close()

        # set up mbsyncrc
        for email_account in email_accounts:
            account_info = email_account.values()[0]
            account_name = email_account.keys()[0]

        return success

class SetupError(Exception):
    pass
