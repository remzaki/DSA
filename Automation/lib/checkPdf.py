import os
import re
import time
import PyPDF2
from _winreg import *
from StringIO import StringIO
from urllib2 import Request, urlopen
from config import config
from remote import Remote


class CheckPDF(object):
    def part_number(self, pdf_file, part_number):
        """Retrieving the part number"""
        if 'http' in pdf_file:  # for Brochure
            try:
                file_ = urlopen(Request(pdf_file)).read()
                pdfFileObj = StringIO(file_)
                # regexes = ['(\w{7})-G-(\w{4})', '(\w{5})-G-(\w{4})', '(\w{5})-UHA-(\w{4})']  #42674C1-G-0816, discount_card:42695-UHA-0816, dental:39738-G-0516
                # writer = PyPDF2.PdfFileWriter()
                # outputStream = open("output.pdf", "wb")
                # writer.write(outputStream)
                # outputStream.close()
            except Exception, exc:
                print 'ERROR: %s' % exc
                return None, None
        else:   # For Application
            with OpenKey(HKEY_CURRENT_USER,
                         'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
                Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
            file_ = os.path.join(Downloads, pdf_file)
            stop_time = time.time() + 10
            while not os.path.exists(file_) and time.time() < stop_time:
                continue
            if os.path.exists(file_):
                pdfFileObj = open(file_, 'rb')
            else:
                return None, None
            # regexes = ['(\w{4})-G-(\w{4})', '(\w{4})-UHA-(\w{4})']  # 348E-G-0816, 230F-UHA-0816:for discount card

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        if pdfReader.isEncrypted:
            pdfReader.decrypt(password='')
        numPage = pdfReader.numPages
        print 'numpage = %s' % numPage
        brk = None
        try:
            for i in range(0, numPage):
                print 'i = %s' % i
                pageObj = pdfReader.getPage(i)
                page_content = pageObj.extractText()
                pdf_content = StringIO(page_content.encode("ascii", "ignore"))
                for line in pdf_content:
                    if part_number in line:
                        print 'part number found: %s', part_number
                        print 'it matched!'
                        brk = 1
                        break
                if brk:
                    break
        except Exception, exc:
            print 'ERROR: %s' % exc
            return None, None
        pdfFileObj.close()
        time.sleep(3)
        if not brk:
            part_number = None
        return part_number, file_

    def contents(self, pdf_file):
        """Analyzing pdf contents"""
        # TODO: for future reading of pdf contents
        print pdf_file

# c = CheckPDF()
# pn, file_ = c.part_number('Application_VISION.pdf')
# pn, file_ = c.part_number('https://model.uhone.com/FileHandler.ashx?FileName=42674C1-G201608.pdf')