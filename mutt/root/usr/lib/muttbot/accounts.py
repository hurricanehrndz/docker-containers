import os
import re
from messenger import Messenger


class AccountsSetuper(object):

    def setup(self, email_accounts):
        success = True
        mbsyncrc = open(self._mbsync_config, 'a')
        mbsyncrc.write('Sync All\n')
        mbsyncrc.write('Expunge Both\n')
        mbsyncrc.close()

        # set config files for each acount
        for email_account in email_accounts:
            account_info = email_account.values()[0]
            account_name = email_account.keys()[0]
            print 'Setting up ' + account_name
            self.create_mail_dirs(account_name)
            if str(account_info['type']) == 'gmail':
                self.setup_mbsync_gmail_account(account_name, account_info)
            else:
                self.setup_mbsync_exchange_account(account_name, account_info)
            self.write_account_muttrc(account_name, account_info)
            self.write_account_signature(account_name, account_info)
            self.muttrc_append_folderhook(account_name)
            self.msmtprc_append_account(account_name, account_info)

        # setup account wide settings
        self.write_notmuch_config(email_accounts)
        self.update_kz_muttrc()

        return success

    def setup_mbsync_gmail_account(self, account_name, account_info):
        self.setup_mbsync_imap_account(account_name, account_info, 'IMAPS')
        self.setup_mbsync_channels(account_name, 'gmail')

    def setup_goobook(self, account_name, account_info):
        goobookrc = open(os.path.join(self._home_dir,'.goobookrc-' + account_name), 'w')
        goobookrc.write('[DEFAULT]\n')
        goobookrc.wrtie('email: ' + account_info['email'] + '\n')
        goobookrc.write('password: ' + account_info['pass'] + '\n')
        goobookrc.write('cache_filename: ~/.goobook_cache_' + account_name + '\n')
        goobookrc.write('cache_expiry_hours: 48\n')
        goobookrc.close()


    def setup_mbsync_exchange_account(self, account_name, account_info):
        self.setup_mbsync_imap_account(account_name, account_info, 'None')
        self.setup_mbsync_channels(account_name, 'exchange')
        # davmail setsup an internal owa to imap proxy
        self.write_davmail_config(account_name, account_info)

    def write_davmail_config(self, account_name, account_info):
        davmail_config = open(os.path.join(self._home_dir, account_name + '-davmail.properties'), 'w' )
        davmail_config.write(account_info['davmail'])
        davmail_config.close

    def setup_mbsync_imap_account(self, account_name, account_info, ssl_type):
        # setup account for mbsync
        mbsyncrc = open(self._mbsync_config, 'a')
        mbsyncrc.write('IMAPAccount ' + account_name + '\n')
        mbsyncrc.write('Host ' + account_info['imap'] + '\n')
        if 'imap_port' in account_info:
            mbsyncrc.write('Port ' + str(account_info['imap_port']) + '\n')
        mbsyncrc.write('User ' + account_info['user'] + '\n')
        mbsyncrc.write('Pass ' + account_info['pass'] + '\n')
        mbsyncrc.write('SSLType ' + ssl_type + '\n')
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
        mbsyncrc.close()

    def setup_mbsync_channels(self, account_name, account_type):
        folder_patterns_to_ignore = ''
        local_folders = getattr(self, '_' + account_type + '_local_folders')
        remote_folders = getattr(self, '_' + account_type + '_remote_folders')
        ignore_folders = getattr(self, '_' + account_type + '_ignore_folders')
        mbsyncrc = open(self._mbsync_config, 'a')
        for i in range (0, len(remote_folders)):
            mbsyncrc.write('Channel ' + account_name + '-' + local_folders[i] + '\n')
            mbsyncrc.write('Master :' + account_name + '-remote:"' + remote_folders[i] + '"\n')
            mbsyncrc.write('Slave :' + account_name + '-local:"' +  local_folders[i] + '"\n')
            mbsyncrc.write('Create Both\n')
            mbsyncrc.write('SyncState *\n')
            mbsyncrc.write('Patterns *\n')
            mbsyncrc.write('\n')
            folder_patterns_to_ignore += '!"' + remote_folders[i] + '"* '

        for i in range (0, len(ignore_folders)):
            folder_patterns_to_ignore += '!' + ignore_folders[i] + '* '

        for i in range (0, len(local_folders)):
            folder_patterns_to_ignore += '!' + local_folders[i] + '* '

        # Other folders
        mbsyncrc.write('Channel ' + account_name + '-default' + '\n')
        mbsyncrc.write('Master :' + account_name + '-remote:\n')
        mbsyncrc.write('Slave :' + account_name + '-local:\n')
        mbsyncrc.write('Create Both\n')
        mbsyncrc.write('SyncState *\n')
        mbsyncrc.write('Patterns * ' + folder_patterns_to_ignore + '\n')
        mbsyncrc.write('\n')
        mbsyncrc.write('\n')

        mbsyncrc.write('Group ' + account_name + '-group\n')
        for i in range (0, len(local_folders)):
            mbsyncrc.write('Channel ' + account_name + '-' + local_folders[i] + '\n')
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
        account_muttrc.write('set signature = ~/.mutt/' + account_name + '.sig\n')
        account_muttrc.write('set pgp_sign_as = ' + str(account_info['gpg']) + '\n')
        account_muttrc.write('my_hdr OpenPGP: id=' + str(account_info['gpg'])[2:] + ' \n')
        account_muttrc.write('set sendmail = "/usr/bin/msmtp -a ' + account_name +  '"\n')
        account_muttrc.write('set sendmail_wait = -1\n')
        account_muttrc.write('unset record\n')
        account_muttrc.write('set header_cache = ~/.mutt/cache/' + account_name +'/headers\n')
        account_muttrc.write('set message_cachedir = ~/.mutt/cache/' + account_name +'/bodies\n')
        account_muttrc.write('set certificate_file = ~/.mutt/cache/' + account_name +'/certificates\n')
        account_muttrc.write('set nm_hidden_tags = "unread,drafts,flagged,INBOX,archive,important,signed,replied,attachment,' + account_name +'"\n')
        account_muttrc.write('set my_account_tag = ' + account_name + '\n')
        account_muttrc.write('source ~/.mutt/muttrc.folder.bindings\n')
        # add goobookrc if type is gmail
        if str(account_info['type']) == 'gmail':
            if 'global_goobook' in account_info:
                if account_info['global_goobook'] == 'true':
                    kz_muttrc =  open(os.path.join(self._mutt_dir, 'muttrc.kz'), w)
                    kz_muttrc.write('set query_command="goobook -c ' + os.path.join(self._home_dir,'.goobookrc-' + account_name) + ' query \'%s\'"\n')
                    kz_muttrc.write('macro index,pager a "<pipe-message>goobook -c ' + os.path.join(self._home_dir,'.goobookrc-' + account_name) + ' add<return>" "add sender to google contacts"\n')
                    kz_muttrc.write('bind editor <Tab> complete-query\n')
                    kz_muttrc.close()
            else:
                account_muttrc.write('set query_command="goobook -c ' + os.path.join(self._home_dir,'.goobookrc-' + account_name) + ' query \'%s\'"\n')
                account_muttrc.write('macro index,pager a "<pipe-message>goobook -c ' + os.path.join(self._home_dir,'.goobookrc-' + account_name) + ' add<return>" "add sender to google contacts"\n')
                account_muttrc.write('bind editor <Tab> complete-query\n')
        account_muttrc.close

    def write_account_signature(self, account_name, account_info):
        # Save signature
        signature = open(os.path.join(self._mutt_dir, account_name + '.sig'), 'w' )
        signature.write(account_info['signature'])
        signature.close

    def create_mail_dirs(self, account_name):
        # Create required folders and files for account
        if not os.path.exists(os.path.join(self._mutt_dir, 'cache/' + account_name )):
            os.makedirs(os.path.join(self._mutt_dir, 'cache/' + account_name))
            os.makedirs(os.path.join(self._mutt_dir, 'cache/' + account_name + '/headers'))
            os.makedirs(os.path.join(self._mutt_dir, 'cache/' + account_name + '/bodies'))
            open(os.path.join(self._mutt_dir, 'cache/' + account_name + '/certificates'), 'a').close()

        if not os.path.exists(os.path.join(self._mail_dir, account_name)):
            os.makedirs(os.path.join(self._mail_dir, account_name))

    def msmtprc_append_account(self, account_name, account_info):
        # setup msmtprc for sending mail
        msmtprc = open(os.path.join(self._home_dir, ".msmtprc"), 'a')
        msmtprc.write('account ' + account_name + '\n')
        msmtprc.write('host ' + account_info['smtp'] + '\n')
        msmtprc.write('port ' + str(account_info['smtp_port']) + '\n')
        msmtprc.write('protocol smtp\n')
        if str(account_info['type']) == 'gmail':
            msmtprc.write('tls on\n')
            msmtprc.write('tls_trust_file /var/lib/ca-certificates/ca-bundle.pem\n')
            msmtprc.write('auth on\n')
        else:
            msmtprc.write('auth login\n')
        msmtprc.write('from ' + account_info['email'] + '\n')
        msmtprc.write('user ' + account_info['user'] + '\n')
        msmtprc.write('password ' + account_info['pass'] + '\n')
        msmtprc.write('logfile ~/.' + account_name + '-msmtp.log\n')
        msmtprc.write('\n')
        msmtprc.close()
        os.chmod(os.path.join(self._home_dir, ".msmtprc"), 0600)

    def muttrc_append_folderhook(self, account_name):
        # add folder hooks to muttrc
        muttrc = open(os.path.join(self._mutt_dir, 'muttrc'), 'a')
        if self._is_first_account:
            muttrc.write('source ~/.mutt/' + account_name + '"\n')
            self._is_first_account = False

        muttrc.write('folder-hook tag:"' +  account_name + '" "source ~/.mutt/' + account_name + '"\n')
        muttrc.close

    def write_notmuch_config(self, email_accounts):
        #notmuch config
        other_emails = ''
        notmuch_config = open(os.path.join(self._home_dir, '.notmuch-config'), 'w')
        notmuch_config.write('[database]\n')
        notmuch_config.write('path=' + self._mail_dir + '\n')
        notmuch_config.write('[new]\n')
        notmuch_config.write('tags=new;\n')
        notmuch_config.write('[user]\n')
        notmuch_config.write('name=' + email_accounts[0].values()[0]['name'] + '\n')
        notmuch_config.write('primary_email=' + email_accounts[0].values()[0]['email'] + '\n')
        for i in  range(0, len(email_accounts) - 1 ):
            other_emails += email_accounts[i].values()[0]['email'] + ';'

        notmuch_config.write('other_email=' + other_emails + '\n')
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

    def __init__(self):
        self._log = Messenger()
        self._gmail_remote_folders=['[Gmail]/Trash', 'INBOX', '[Gmail]/Drafts', '[Gmail]/Sent Mail', '[Gmail]/Important', '[Gmail]/Starred', '[Gmail]/All Mail', '[Gmail]/Spam']
        self._gmail_local_folders=['trash', 'INBOX', 'drafts', 'sent', 'important', 'flagged',  'archive', 'spam']
        self._gmail_ignore_folders=[]
        self._exchange_remote_folders=['Trash', 'Deleted Items', 'INBOX', 'Drafts', 'Sent', 'Junk']
        self._exchange_local_folders=['trash', 'deleted', 'INBOX', 'drafts', 'sent', 'spam']
        self._exchange_ignore_folders=['"Unsent Messages"', '"Your feeds"', '"Sync Issues*"']
        self._home_dir = os.path.expanduser('~')
        self._mail_dir = os.path.join(self._home_dir, '.mail')
        self._mutt_dir = os.path.join(self._home_dir, '.mutt/')
        self._mbsync_config = os.path.join(self._home_dir, '.mbsyncrc')
        self._msmtprc_config = os.path.join(self._home_dir, ".msmtprc")
        self._is_first_account = True

class SetupError(Exception):
    pass
