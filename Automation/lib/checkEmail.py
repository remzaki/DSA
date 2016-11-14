"""Get a list of Threads from the user's mailbox.
"""
from __future__ import print_function
from apiclient import errors
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from lib.config import config
import base64
import email
import re
import os
import shutil


class CheckEmail(object):
    def ListMessagesMatchingQuery(self, service, user_id, query=''):
        """List all Messages of the user's mailbox matching the query.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

      Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
      """
        try:
            response = service.users().messages().list(userId=user_id,
                                                       q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user_id, q=query,
                                                           pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError, error:
            print('An error occurred in ListMessagesMatchingQuery: %s' % error)
            return None

    def GetMimeMessage(self, service, user_id, msg_id):
        """Get a Message and use it to create a MIME Message.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

      Returns:
        A MIME Message, consisting of data from Message.
      """
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id,
                                                     format='raw').execute()

            # print ('Message snippet: %s' % message['snippet'])

            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

            mime_msg = email.message_from_string(msg_str)

            return mime_msg
        except errors.HttpError, error:
            print('An error occurred in GetMimeMessage: %s' % error)

    def TrashMessage(self, service, user_id, msg_id):
        """Get a Thread.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        thread_id: The ID of the Thread required.

      Returns:
        Thread with matching ID.
      """
        try:
            # thread = service.users().threads().get(userId=user_id, id=thread_id).execute()
            thread = service.users().messages().trash(userId=user_id, id=msg_id).execute()
            print(('message id: %s - is successfully moved to trash!') % (msg_id))
            return thread
        except errors.HttpError, error:
            print('An error occurred in TrashMessage: %s' % error)

    def get_mpart(self, mail):
        maintype = mail.get_content_maintype()
        if maintype == 'multipart':
            for part in mail.get_payload():
                # This includes mail body AND text file attachments.
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
            # No text at all. This is also happens
            return ""
        elif maintype == 'text':
            return mail.get_payload()

    def get_mail_body(self, mail):
        """
        There is no 'body' tag in mail, so separate function.
        :param mail: Message object
        :return: Body content
        """
        body = ""
        if mail.is_multipart():
            # This does not work.
            # for part in mail.get_payload():
            #    body += part.get_payload()
            body = self.get_mpart(mail)
        else:
            body = mail.get_payload()
        return body

    def get_auth(self):
        email_add = config.email_add
        SCOPES = config.SCOPES
        store = file.Storage(config.storage_file)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(config.client_secret, SCOPES)
            creds = tools.run_flow(flow, store)
        service = discovery.build(config.mail, config.m_version, http=creds.authorize(Http()))
        return email_add, service

    def get_email(self, typ, email_file):
        email_add, service = self.get_auth()
        if typ.lower() == "customized quote":
            q = config.q_sub_cq
        elif typ.lower() == "self-service quote":
            q = config.q_sub_ssq
        elif typ.lower() == "baa":
            q = config.q_sub_baa

        messages = None
        while not messages:
            messages = self.ListMessagesMatchingQuery(service, email_add, query=q)
        id_ = []
        for list in messages:
            for key in list:
                if key == 'id':
                    id_.append(list[key])

        for id in id_:  # Gets the MIMEMessage for each message id
            getmimemessage = self.GetMimeMessage(service, email_add, id)
            body_txt = "body.txt"
            body = self.get_mail_body(getmimemessage)
            # Open new data file
            f = open(body_txt, "w")
            f.write(body)  # str() converts to string
            f.close()
            file_txt = open(body_txt, 'r')
            file_html = open(email_file, 'w')
            strlist = []
            for f in file_txt:
                if f == '\n':
                    continue
                elif '=\r\n' in f:
                    f = f.replace('=\r\n', '')
                    strlist.append(f)
                else:
                    if '\r' in f:
                        f = f.replace('\r', '')
                    line = ''.join(strlist)
                    line = line + f
                    if "=3D" in line:
                        line = line.replace("=3D", "=")
                    if "&amp;" in line:
                        line = line.replace("&amp;", "&")
                    file_html.write(line)
                    strlist = []
            file_txt.close()
            file_html.close()

            file_html = open(email_file, 'r')
            regex = ['<title>(.*?)</title>', 'href=\"(.*?)\">']
            index = 0
            stop = len(regex)
            list_ = []
            for line in file_html:
                matches = re.search(regex[index], line)
                if matches:
                    list_.append(matches.group(1))
                    index += 1
                if index >= stop:
                    break
            os.remove(body_txt)
            i_d = id
            file_html.close()
            break
        uid = None
        if list_:
            # Message move to trash
            self.TrashMessage(service, email_add, i_d)
            email_folder = "emails"
            email_dir = os.path.join(os.getcwd(), email_folder)
            if not os.path.exists(email_dir):
                os.makedirs(email_dir)
            e_file = os.path.join(os.getcwd(), email_file)
            if os.path.exists(os.path.join(email_dir, email_file)):
                os.remove(os.path.join(email_dir, email_file))
            shutil.move(e_file, email_dir)

            if config.exec_mode == 'local':
                exp_title = list_[0]
                url = os.path.join(email_dir, email_file)
            else:
                url = list_[1]
                exp_title = 'UHOne'
            regex = 'ID=(.*?)$'    #Extracting Unique ID from link
            matches = re.search(regex, list_[1])
            if matches:
                uid = matches.group(1)
        else:
            exp_title = None
        print ('URL = ', url, 'Title = ', exp_title)
        return url, exp_title, uid

    def clear_emails(self):
        email_add, service = self.get_auth()
        q = 'label:UNREAD'
        messages = self.ListMessagesMatchingQuery(service, email_add, query=q)
        id_ = []
        for list in messages:
            for key in list:
                if key == 'id':
                    id_.append(list[key])
        for id in id_:  #Deletes all unread messages
            self.TrashMessage(service, email_add, id)

# if __name__ == '__main__':
#     mail = CheckEmail()
#     mail.get_link("Customized Quote")
