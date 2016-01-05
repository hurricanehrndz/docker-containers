import re
def gmail_name_trans(folder_name, account):
    new_folder_name =   re.sub(' ', '_',
                        re.sub('.*Spam$', 'spam',
                        re.sub('.*Drafts$', 'drafts',
                        re.sub('.*Sent Mail$', 'sent',
                        re.sub('.*Starred$', 'flagged',
                        re.sub('.*Trash$', 'trash',
                        re.sub('.*Important$', 'important',
                        re.sub('.*All Mail$', 'archive', folder_name))))))))
    return new_folder_name

def local_name_trans(folder_name, account):
    new_folder_name =   re.sub('spam', '[Gmail].Spam',
                        re.sub('drafts', '[Gmail].Drafts',
                        re.sub('sent', '[Gmail].Sent Mail',
                        re.sub('flagged', '[Gmail].Starred',
                        re.sub('trash', '[Gmail].Trash',
                        re.sub('important', '[Gmail].Important',
                        re.sub('archive', '[Gmail].All Mail',
                        re.sub('_', ' ', folder_name))))))))
    return new_folder_nam
