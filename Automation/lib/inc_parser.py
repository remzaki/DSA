#/automation/func/
import os
import re
import csv
import ConfigParser


class Parser:
    def get_testsuites(self):
        """This method gets the testsuites path where the testcases are saved."""
        ts_folder  = "data"
        testsuites = {}
        cwd        = os.path.abspath("..")
        for root, dirs, files in os.walk(cwd):
            if ts_folder in dirs:
                path_ = os.path.join(root, ts_folder)
                break
        for root, dirs, files in os.walk(path_):
            break
        for ts in dirs:
            if " " in ts:
                key_ts  = str(ts)
                key_ts  = key_ts.replace(" ", "_")
                testsuites[key_ts] = os.path.join(path_, ts)
            else:
                testsuites[ts] = os.path.join(path_, ts)
            print "testsuites = %s" %ts
        print dirs
        print testsuites
        return testsuites

    def get_csvfiles(self):
        """This method gets the testcases/files with csv extension and saved it in a files_ variable list."""
        testsuites = self.get_testsuites()
        tests      = {}
        tcs        = []
        for ts in testsuites:
            path_ = testsuites.get(ts)
            for tc in os.listdir(path_):
                tc = str(tc)
                if tc.endswith(".csv"):
                    tcs.append(os.path.join(path_, tc))
            tests[ts] = tcs
        return tests

    def read_csvfiles(self):
        """This method reads the contents of the csv files and saved it in a datadict dictionary."""
        tests    = self.get_csvfiles()
        datadict = {}
        for test in tests:
            tsdict = {}
            num    = 1
            files_ = tests.get(test)
            for file in files_:
                list_ = []
                no_tc = True
                count = 1
                #checks if csv file is empty
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
                        tsdict[key] = list_
                    finally:
                        f.close()
            datadict[test] = tsdict
        return datadict

    def get_setup_cfg(self, obj):
        print "get setup configuration"


    def get_datadict(self):
        """This method calls the read_csvfiles method."""
        data   = self.read_csvfiles()
        print data
        return data


if __name__ == '__main__':
    #print "main"
    obj = Parser()
    obj.get_datadict()
