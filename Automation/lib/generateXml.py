#/Automation/lib
import os
import re
from xml.dom.minidom import Document

class TestDict(object):
    def __init__(self):
        self.dict_ = {}
        self.count = 0

    @property
    def testDict(self):
        """Getter: I'm the 'testDict' property."""
        return self.dict_

    @testDict.setter
    def testDict(self, data):
        """Setter: I'm the 'testDict' setter."""
        ts = data["testsuite"]
        tc = data["testcase"]
        keys = self.dict_.keys()
        keys.sort()

        if ts in keys:
            self.value_dict_ = {}
            self.value_dict_["passed"]   = data["passed"]
            self.value_dict_["failed"]   = data["failed"]
            self.value_dict_["duration"] = data["duration"]
            self.value_dict_["os"]       = data["os"]
            self.value_dict_["browser"]  = data["browser"]
            self.value_dict_["screenshot"]    = data["screenshot"]
            self.value_dict_["log"]      = data["log"]
            self.value_dict_["elog"]     = data["elog"]
            self.tc_dict[tc] = self.value_dict_
            self.tc_list     = self.tc_dict
            self.dict_[ts]   = self.tc_list
            self.count += 1
        else:
            self.tc_dict = {}
            self.value_dict = {}
            self.value_dict["passed"]   = data["passed"]
            self.value_dict["failed"]   = data["failed"]
            self.value_dict["duration"] = data["duration"]
            self.value_dict["os"]       = data["os"]
            self.value_dict["browser"]  = data["browser"]
            self.value_dict["screenshot"]    = data["screenshot"]
            self.value_dict["log"]      = data["log"]
            self.value_dict["elog"]     = data["elog"]
            self.tc_dict[tc] = self.value_dict
            self.tc_list     = self.tc_dict
            self.dict_[ts]   = self.tc_list

        self.dict_

    def create_xml_report(self, tc_dict):
        """
        This method will create an xml file.
        """
        doc        = Document()
        total_time = 0
        total_pass = 0
        total_fail = 0

        #add the root tag for the dom object
        summary = doc.appendChild(doc.createElement('test_result'))

        #environment node
        envnode = summary.appendChild(doc.createElement("environment"))
        envnode.appendChild(doc.createElement("timestart")).appendChild(doc.createTextNode("tbd: yyyy-mm-dd_hh.mm.ss"))
        envnode.appendChild(doc.createElement("timestopped")).appendChild(doc.createTextNode("tbd: yyyy-mm-dd_hh.mm.ss"))
        envnode.appendChild(doc.createElement("computername")).appendChild(doc.createTextNode("tbd: computer_name"))
        envnode.appendChild(doc.createElement("ipaddress")).appendChild(doc.createTextNode("tbd: x.x.x.x"))

        tc_keys = tc_dict.keys()
        tc_keys.sort()

        for tc_key in tc_keys:
            tc_subdict = tc_dict.get(tc_key)
            tsNode = summary.appendChild(doc.createElement("testcase"))
            tsNode.setAttribute("name", tc_key)
            tsNode.setAttribute("pass", tc_subdict.get("passed"))
            tsNode.setAttribute("fail", tc_subdict.get("failed"))
            tsNode.setAttribute("duration", "%.3f" % float(tc_subdict.get("duration")))
            tsNode.setAttribute("os", tc_subdict.get("os"))
            tsNode.setAttribute("browser", tc_subdict.get("browser"))
            tsNode.setAttribute("screenshot", tc_subdict.get("screenshot"))
            tsNode.setAttribute("log", tc_subdict.get("log"))
            tsNode.setAttribute("elog", tc_subdict.get("elog"))
            total_pass = total_pass + int(tc_subdict.get("passed"))
            total_fail = total_fail + int(tc_subdict.get("failed"))
            total_time = total_time + float(tc_subdict.get("duration"))
        #endfor

        total_time = format(total_time, ".3f")
        summaryNode = summary.appendChild(doc.createElement("test_summary"))
        summaryNode.appendChild(doc.createElement("totaltest")).appendChild(doc.createTextNode(str(total_pass + total_fail)))
        summaryNode.appendChild(doc.createElement("passed")).appendChild(doc.createTextNode(str(total_pass)))
        summaryNode.appendChild(doc.createElement("failed")).appendChild(doc.createTextNode(str(total_fail)))
        summaryNode.appendChild(doc.createElement("totaltime")).appendChild(doc.createTextNode(str(total_time)))

        #This is to fix the spacing issue of prettyxml
        result = doc.toprettyxml(indent='  ')
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
        clean_xml = text_re.sub('>\g<1></', result)
        clean_xml = unicode(clean_xml)
        return clean_xml

    def create_xml(self, report_dict):
        """This method will create a report folder if it's not yet created and calls the create_xml_report method
        to create xml file/s for each testsuites or groups.
        """
        ts_keys = report_dict.keys()
        ts_keys.sort()

        cwd = os.getcwd()
        tr_folder = "report"
        tr_dir = os.path.join(cwd, tr_folder)
        if not os.path.exists(tr_dir):
            os.makedirs(tr_dir)

        for ts_key in ts_keys:
            tc_dict = report_dict.get(ts_key)
            with open(os.path.join(tr_dir, (ts_key + ".xml")), "w") as f:
                f.write(self.create_xml_report(tc_dict))
            f.close()
        return tr_dir


# if __name__ == '__main__':
#     test = TestDict()
#     print test.testDict
#     test.testDict = {"testsuite":"regression", "testcase":"testcase7", "passed":"1", "failed":"0", "duration":"77.894999980926514", "browser":"ie"}
#     print test.testDict
#     test.testDict = {"testsuite":"regression", "testcase":"testcase8", "passed":"0", "failed":"1", "duration":"88.743000030517578", "browser":"chrome"}
#     print test.testDict
#     test.testDict = {"testsuite":"regression", "testcase":"testcase9", "passed":"1", "failed":"0", "duration":"99.743000030517578", "browser":"safari"}
#     print test.testDict
#     test.testDict = {"testsuite":"endtoend", "testcase":"testcase11", "passed":"0", "failed":"1", "duration":"111.894999980926514", "browser":"firefox"}
#     print test.testDict
#     test.create_xml(test.testDict)
    # test.grab_all_results()