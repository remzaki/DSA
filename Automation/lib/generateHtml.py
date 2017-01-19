#/Automation/lib
import sys
import xml.etree.ElementTree as ET
import os
import re
from xml.dom.minidom import Document

class HTMLClass(object):
    def create_table_entry(self,i, elog, screenshot, browser, OS, duration, failed, passed, name, log):
        """
        This method creates a table entry with a list of browser, exec time, fail/pass status, test name, and then
        returns the tableresult.
        """
        if passed == "": #this row data here is for regression test name
            OS = str(OS).replace(' ', '_')
            browser = str(browser).replace(' ', '_')
            id_name = OS + '-' + browser
            if i == 0:
                tableresult = """   <tr data-toggle="collapse" data-target=#%s class="accordion-toggle">
                                     <td colspan="7" id='td3'><button class="btn btn-default btn-xs"></button><strong>&nbsp;%s</strong></td>
                                    </tr>
                                    <tr>
                                     <td colspan="12" id="hiddenRow" class="hiddenRow">
                                     <div class="accordian-body collapse" id=%s>
                                    <table id="tableTestResults" class="table table-borderless">
                                    """ % (id_name, name, id_name)
            else:
                tableresult = """
                                        </table>
            			                </div>
          			                    </td>
                                    </tr>
                                    <tr data-toggle="collapse" data-target=#%s class="accordion-toggle">
                                     <td colspan="7" id='td3'><button class="btn btn-default btn-xs"></button><strong>&nbsp;%s</strong></td>
                                    </tr>
                                    <tr>
                                     <td colspan="12" id="hiddenRow" class="hiddenRow">
                                     <div class="accordian-body collapse" id=%s>
              			            <table id="tableTestResults" class="table table-borderless">
                                    """ % (id_name, name, id_name)

        elif passed == "1": #this row data here is for passed test
            tableresult = """
                                      <tr>
                                        <td class="col-md-3 col-sm-3 col-xs-3" id='td2'>%s</td>
                                        <td class="col-md-1 col-sm-1 col-xs-1" id='td2'><a href="%s" class="btn btn-success btn-xs" role="button" target="_blank">Pass</a></td>
                                        <td class="col-md-2 col-sm-2 col-xs-2" id='td2'>%s</td>
                                        <td class="col-md-2 col-sm-2 col-xs-2" id='td2'>%s</td>
                                        <td class="col-md-2 col-sm-2 col-xs-2" id='td2'>%s</td>
                                        <td class="col-md-1 col-sm-1 col-xs-1" id='td2'><a href="%s" class="btn btn-info btn-xs" role="button" target="_blank">View</a></td>
                                        <td class="col-md-1 col-sm-1 col-xs-1" id='td2'>%s</td>
                                      </tr>
              			""" % (name, screenshot, duration, OS, browser, log, elog)

        else: #this row data here is for failed test
			tableresult = """
                                      <tr>
                                        <td class="col-md-3 col-sm-3 col-xs-3" id='td2'>%s</td>
                                        <td class="col-md-1 col-sm-1 col-xs-1" id='td2'><a href="%s" class="btn btn-danger btn-xs" role="button" target="_blank">Fail</a>
                                        <td class="col-md-2 col-sm-2 col-xs-2" id='td2'>%s</td>
                                        <td class="col-md-2 col-sm-2 col-xs-2" id='td2'>%s</td>
                                        <td class="col-md-2 col-sm-2 col-xs-2" id='td2'>%s</td>
                                        <td class="col-md-1 col-sm-1 col-xs-1" id='td2'><a href="%s" class="btn btn-info btn-xs" role="button" target="_blank">View</a>
                                        <td class="col-md-1 col-sm-1 col-xs-1" id='td2'><a href="#elog_%s" class="btn btn-info btn-xs" data-toggle="collapse">View</a>
                                            <div id="elog_%s" class="collapse">
                                            %s
                                            </div>
                                        </td>
                                      </tr>
              			""" % (name, screenshot, duration, OS, browser, log, i, i, elog)
        return tableresult

    def process_xml(self, XMLFile, outputdir, act_durationtime):
        """This method processes an xmlfile and convert it into an html file."""
        HTMLTempalteFile = "HTML.html.template"
        outputname = "report.html"
        XMLFile = os.path.join(outputdir, XMLFile)
        cwd = os.getcwd()
        HTMLTempalteFile = os.path.join(cwd, HTMLTempalteFile)
        if not os.path.isfile(XMLFile):
            print "Error! file '%s' not found." % (XMLFile)
            sys.exit(1)
        # endif

        if not os.path.isfile(HTMLTempalteFile):
            print "Error! file '%s' not found." % (HTMLTempalteFile)
            sys.exit(1)
        # endif

        if not os.path.exists(outputdir):
            print "Error! directory '%s' not found." % (outputdir)
            sys.exit(1)
        # endif

        # Read HTML Template
        with open(HTMLTempalteFile, 'r') as f:
            HTMLData = f.read()
        f.closed

        # Read and Gather the XML Test result
        tree = ET.parse(XMLFile)
        root = tree.getroot()

        # get tests results
        tsuite = ""
        i = 0
        for ts in root.iter('testcase'):
            if not tsuite:
                tsuite = self.create_table_entry(i, ts.attrib.get('elog'), ts.attrib.get('screenshot'), ts.attrib.get('browser'),
                                                ts.attrib.get('os'), ts.attrib.get('duration'), ts.attrib.get('fail'),
                                                ts.attrib.get('pass'), ts.attrib.get('name'), ts.attrib.get('log'))
            else:
                tsuite = tsuite + "\n%s" % self.create_table_entry(i, ts.attrib.get('elog'), ts.attrib.get('screenshot'),
                                                ts.attrib.get('browser'), ts.attrib.get('os'), ts.attrib.get('duration'),
                                                ts.attrib.get('fail'), ts.attrib.get('pass'), ts.attrib.get('name'), ts.attrib.get('log'))
                i += 1
            # endif
        # endfor

        HTMLData = HTMLData.replace("@@tableentry@@", tsuite)

        # get Test Summary
        for testsumm in root.iter('test_summary'):
            total_tests = testsumm.find('totaltest').text
            total_pass = testsumm.find('passed').text
            total_fail = testsumm.find('failed').text
            total_time = testsumm.find('totaltime').text
        # endfor
        # total_time = self.sec2time(float(total_time)) # commented out: use to get the sum of all test cases duration time of execution
        total_time = self.sec2time(float(act_durationtime))

        HTMLData = HTMLData.replace("@@totaltc@@", total_tests)
        HTMLData = HTMLData.replace("@@pass@@", total_pass)
        HTMLData = HTMLData.replace("@@fail@@", total_fail)
        HTMLData = HTMLData.replace("@@duration@@", total_time)

        # print HTMLData
        ofile = open(os.path.join(outputdir, outputname), 'w')
        ofile.write(HTMLData)
        ofile.close()
        os.remove(os.path.join(outputdir, XMLFile))

    def merge_xmls(self, outdir):
        """This method merges all the test generated xml files into one and returns the merged xml file."""
        resultdict = {}
        for xmlfile in os.listdir(outdir):
            if not xmlfile.endswith(".xml"): continue
            resultdict = self.read_result(outdir, xmlfile, resultdict)
        xml = "report.xml"
        with open(os.path.join(outdir, xml), "w") as f:
            f.write(self.create_xml_report(resultdict))
        f.close()
        return xml

    def read_result(self, outdir, xmlfile, resultdict):
        """This method will read each of the xml files, get its contents and returns a dictionary."""
        tree  = ET.parse(os.path.join(outdir, xmlfile))
        root  = tree.getroot()
        file_ = xmlfile.split(".")
        file_ = file_[0]
        x = 1
        for ts in root.iter('testcase'):
            result = ts.attrib
            resultdict[file_ + str(x)] = result
            x += 1
        os_ = ts.attrib.get('os')
        browser = ts.attrib.get('browser')
        resultdict[file_] = {"duration": None, "fail": None, "browser": browser, "name": file_, "pass": None, "os": os_,
                             "screenshot": None, "log": None, "elog": None}
        return resultdict

    def create_xml_report(self, tc_dict):
        """This method will create an xml file."""
        doc        = Document()
        total_time = 0
        total_pass = 0
        total_fail = 0

        #add the root tag for the dom object
        summary = doc.appendChild(doc.createElement('test_result'))

        tc_keys = tc_dict.keys()
        tc_keys.sort()

        for tc_key in tc_keys:
            tc_subdict = tc_dict.get(tc_key)
            tsNode = summary.appendChild(doc.createElement("testcase"))
            tsNode.setAttribute("name", tc_subdict.get("name"))
            tsNode.setAttribute("pass", tc_subdict.get("pass"))
            tsNode.setAttribute("fail", tc_subdict.get("fail"))
            tsNode.setAttribute("os", tc_subdict.get("os"))
            tsNode.setAttribute("browser", tc_subdict.get("browser"))
            tsNode.setAttribute("screenshot", tc_subdict.get("screenshot"))
            tsNode.setAttribute("log", tc_subdict.get("log"))
            tsNode.setAttribute("elog", tc_subdict.get("elog"))
            if not tc_subdict.get("pass") == None:
                total_pass = total_pass + int(tc_subdict.get("pass"))
            if not tc_subdict.get("fail") == None:
                total_fail = total_fail + int(tc_subdict.get("fail"))
            if not tc_subdict.get("duration") == None:
                total_time = total_time + float(tc_subdict.get("duration"))
                tsNode.setAttribute("duration", "%.3fs" % float(tc_subdict.get("duration")))
            if tc_subdict.get("duration") == None:
                tsNode.setAttribute("duration", tc_subdict.get("duration"))
        #endfor

        total_time  = format(total_time, ".3f")
        summaryNode = summary.appendChild(doc.createElement("test_summary"))
        summaryNode.appendChild(doc.createElement("totaltest")).appendChild(doc.createTextNode(str(total_pass + total_fail)))
        summaryNode.appendChild(doc.createElement("passed")).appendChild(doc.createTextNode(str(total_pass)))
        summaryNode.appendChild(doc.createElement("failed")).appendChild(doc.createTextNode(str(total_fail)))
        # summaryNode.appendChild(doc.createElement("totaltime")).appendChild(doc.createTextNode(str(total_time)+"s"))
        summaryNode.appendChild(doc.createElement("totaltime")).appendChild(doc.createTextNode(str(total_time)))

        #This is to fix the spacing issue of prettyxml
        result    = doc.toprettyxml(indent='  ')
        text_re   = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
        clean_xml = text_re.sub('>\g<1></', result)
        clean_xml = unicode(clean_xml)
        return clean_xml

    def sec2time(self, sec, n_msec=0):
        ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
        if hasattr(sec, '__len__'):
            return [self.sec2time(s) for s in sec]
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if n_msec > 0:
            pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec + 3, n_msec)
        else:
            pattern = r'%02d:%02d:%02d'
        if d == 0:
            return pattern % (h, m, s)
        return ('%d days, ' + pattern) % (d, h, m, s)

    def create_html(self, outputdir, act_durationtime):
        """This method will call the merge_xmls and process_xml methods to create an html file."""
        xml = self.merge_xmls(outputdir)
        self.process_xml(xml, outputdir, act_durationtime)


# if __name__ == "__main__":
#     hreport = HTMLClass()
#     outputdir = "D:\\Automation\\Automation\\report"
#     hreport.create_html(outputdir)