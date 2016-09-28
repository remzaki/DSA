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

    def get_link(self, typ):
        email_add = config.email_add
        SCOPES = config.SCOPES
        store = file.Storage(config.storage_file)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(config.client_secret, SCOPES)
            creds = tools.run_flow(flow, store)
        service = discovery.build(config.mail, config.m_version, http=creds.authorize(Http()))

        if typ.lower() == "customized quote":
            q = config.q_sub_cq
            regex = ['=3D"(.*?)\=\r', '(.*?)\=\r', '(.*?)\"\>here']

        elif typ.lower() == "self-service quote":
            q = config.q_sub_ssq
            regex = ['ef=3D"(.*?)\=\r', '(.*?)\"\>start']

        messages = None
        while not messages:
            messages = self.ListMessagesMatchingQuery(service, email_add, query=q)
        id_ = []
        for list in messages:
            for key in list:
                if key == 'id':
                    id_.append(list[key])

        links = []
        stop = len(regex)
        for id in id_:  # Gets the MIMEMessage for each message id
            getmimemessage = self.GetMimeMessage(service, email_add, id)
            file_ = "body.txt"
            body = self.get_mail_body(getmimemessage)
            # Open new data file
            f = open(file_, "w")
            f.write(body)  # str() converts to string
            f.close()
            f = open(file_, "r")
            strlist = []
            index = 0
            for line in f:
                matches = re.search(regex[index], line)
                if matches:
                    if ">here" in line:  # exclusively added for customized quote testcase
                        if not index >= stop - 1:
                            index += 1
                        matches = re.search(regex[index], line)
                        strlist.append(matches.group(1))
                    else:
                        strlist.append(matches.group(1))
                    index += 1
                if index >= stop:
                    break
            f.close()
            link = ''.join(strlist)
            if "=3D" in link:
                link = link.replace("=3D", "=")
            if "&amp;" in link:
                link = link.replace("&amp;", "&")
            print(link)
            links.append(link)
            os.remove(file_)
            i_d = id
            break

        if links:
            # Message move to trash
            self.TrashMessage(service, email_add, i_d)
            link = links[0]
        else:
            link = None
        return link

        # if __name__ == '__main__':
        #     mail = CheckEmail()
        #     mail.get_link("Customized Quote")
