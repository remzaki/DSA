#/automation/func/
import os
import re
import csv


class Parser:

    def get_csvpath(self):
        """This method searches and returns the path where the csv testcases are saved."""
        ext   = "Automation\\data\\regression"
        # ext   = "D:\\Automation\\Automation\\data\\regression\\"
        cwd   = os.path.abspath("..")
        path_ = os.path.join(cwd, ext)
        return path_

    def get_csvfiles(self):
        """This method gets the testcases/files with csv extension and saved it in a files_ variable list."""
        dir_   = self.get_csvpath()
        files_ = []
        for root, dirs, files in os.walk(dir_):
            for file in files:
                if file.endswith(".csv"):
                    files_.append(os.path.join(root, file))
        return files_

    def read_csvfiles(self):
        """This method reads the contents of the csv files and saved it in a datadict dictionary."""
        files_ = self.get_csvfiles()
        datadict = {}
        num = 1
        for file in files_:
            list_ = []
            no_tc = True
            count = 1
            # checks if csv file is empty
            if os.path.getsize(file) > 0:
                f = open(file, 'rb')
                n = int(sum(1 for r in csv.reader(f)))
                f.close()
                f = open(file, 'rb')
                try:
                    reader = csv.reader(f)
                    for row in reader:
                        row_len = len(row)
                        for x in range(0, row_len):
                            row[x] = row[x].strip()
                        if no_tc:
                            ro = str(row).lower()
                            if "testname" in ro:
                                sp  = re.split(',', ro)
                                key = sp[1]
                                if "'" in key:
                                    key = re.sub('[\']', '', key)
                                key   = key.strip()
                                no_tc = False
                            if count == n:
                                key = "testcase_noname_%s" %str(num)
                                num = int(num)
                                num += 1
                            count += 1
                        list_.append(row)
                    datadict[key] = list_
                finally:
                    f.close()
        return datadict

    def get_setup_cfg(self, obj):
        print "get setup configuration"


    def get_datadict(self):
        """This method calls the read_csvfiles method."""
        # print "get data dictionary"
        data = self.read_csvfiles()
        # print data
        return data


#if __name__ == '__main__':
#    print "main"
