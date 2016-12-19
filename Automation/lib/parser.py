#/automation/lib/
import os
import re
import csv
import ConfigParser


class Parser:
    def readconfig(self):
        """"This method searches the run.ini file in test suites directory and gets the testcases that will be ran."""
        ts_folder = "data"
        inifile   = "run.ini"
        rtc       = "run_testcases"
        tc        = "testcases"
        rtc_all   = False
        tc_is     = ""
        t_is      = ""
        tests_dir = {}
        tests     = {}

        cwd       = os.path.abspath(".")
        config    = ConfigParser.ConfigParser()
        path_     = os.path.join(cwd, ts_folder)
        if os.path.exists(path_):
            for root, dirs, files in os.walk(path_):
                break
            for dir in dirs:
                if " " in dir:
                    key_ts = str(dir)
                    key_ts = key_ts.replace(" ", "_")
                else:
                    key_ts = str(dir)
                path  = os.path.join(path_, dir)
                file_ = os.path.join(path, inifile)
                if inifile in os.listdir(path):
                    if os.path.getsize(file_) > 0:
                        config.read(file_)
                        sections = config.sections()
                        for section in sections:
                            #Gets the run_testcases section, its option and its value
                            if rtc == section:
                                for option in config.options(section):
                                    if option == rtc:
                                        value = config.get(section, option).lower()
                                        if value == "all":
                                            tc_is = "all"
                                            rtc_all = True
                                            tests_dir[key_ts] = path
                                            break
                                        else:
                                            tc_is = "nall"
                                    else:
                                        tc_is = "nall"
                            # Gets the testcases section, its option and its value
                            elif tc  == section and tc_is == "nall":
                                for option in config.options(section):
                                    if option == tc:
                                        value = config.get(section, option)
                                        values = re.split(',', value)
                                        tc_list = []
                                        for val in values:
                                            val = val.strip()
                                            val = val + ".csv"
                                            if os.path.exists(os.path.join(path, val)):
                                                v = os.path.join(path, val)
                                                tc_list.append(v)
                                        tests[key_ts] = tc_list
                                        #Gets all the testcases if testcases option is empty or no testcases listed
                                        if len(tc_list) == 0:
                                            rtc_all = True
                                            tests_dir[key_ts] = path
                                        break
                                    else:
                                        print "no option for testcases = %s... run everything = %s" %(option, path)
                                        rtc_all = True
                                        tests_dir[key_ts] = path

                    else:
                        print "empty ini file in this path = %s... run everything" % path
                        rtc_all = True
                        tests_dir[key_ts] = path
                else:
                    print "no ini file found in this path = %s... run everything" % path
                    rtc_all = True
                    tests_dir[key_ts] = path

            if rtc_all:
                for tc in tests_dir:
                    p = tests_dir.get(tc)
                    tcs = []
                    for t in os.listdir(p):
                        t = str(t)
                        if t.endswith(".csv"):
                            tcs.append(os.path.join(p, t))
                    tests[tc] = tcs
            for test in tests:
                print str(test) + " " + str(tests.get(test))

        else:
            print "data folder does not exist"
            print cwd
            print path_

        return tests

    def read_csvfiles(self):
        """This method reads the contents of the csv files and save it in a datadict dictionary."""
        tests    = self.readconfig()
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


    def get_datadict(self):
        """This method calls the read_csvfiles method."""
        data   = self.read_csvfiles()
        # print data
        return data


# if __name__ == '__main__':
#     #print "main"
#     obj = Parser()
#     obj.get_datadict()
