import os
import re
import time
import PyPDF2
from _winreg import *
from StringIO import StringIO
from urllib2 import Request, urlopen


class CheckPDF(object):
    def part_number(self, pdf_file):
        """Retrieving the part number"""
        if 'http' in pdf_file:  # for Brochure
            try:
                file_ = urlopen(Request(pdf_file)).read()
                pdfFileObj = StringIO(file_)
                regex = '(\w{7})-G-(\w{4})'  # 42674C1-G-0816
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
            regex = '(\w{4})-G-(\w{4})'  # 348E-G-0816
            if os.path.exists(file_):
                pdfFileObj = open(file_, 'rb')
            else:
                return None, None

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        numPage = pdfReader.numPages
        for i in range(0, numPage):
            pageObj = pdfReader.getPage(i)
            page_content = pageObj.extractText()
            pdf_content = StringIO(page_content.encode("ascii", "ignore"))
            brk = None
            for line in pdf_content:
                # print line
                matches = re.search(regex, line)
                if matches:
                    part_number = matches.group(0)
                    # print part_number
                    # print 'it matched!'
                    brk = 1
                    break
            if brk:
                break
        pdfFileObj.close()
        time.sleep(1)
        return part_number, file_

    def contents(self, pdf_file):
        """Analyzing pdf contents"""
        # TODO: for future reading of pdf contents
        print pdf_file

# c = CheckPDF()
# pn, file_ = c.part_number('Application_VISION.pdf')
# pn, file_ = c.part_number('https://model.uhone.com/FileHandler.ashx?FileName=42674C1-G201608.pdf')