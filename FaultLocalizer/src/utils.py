import json
import re
import math
import itertools
import copy
import importlib
import sys
import os
import glob
import datetime
import textwrap
import re
import inspect
import shutil
import ast

class Count:
    counter ={} # counters for all tests
    icounter ={} # individual counters, reset after each test
    icounter_final ={}

    def incC(ci):
        for key, value in Count.counter.items():
            for item in value:
                if item["name"] == ci:
                    item["value"] += 1
                    return 
        #print("C ", Count.counter)

    def reset(cnt_list):
        new_cnt_list = copy.deepcopy(cnt_list)
        Count.counter = new_cnt_list
        print("Count.counter", Count.counter)

    def ireset(icnt_list):
        new_icnt_list = copy.deepcopy(icnt_list)
        Count.icounter = new_icnt_list
        #print("Count.icounter", Count.icounter)

    def run(fn, *args, **kwargs):
        #print("running", fn.__name__, *args)
        fn(*args, **kwargs)

def convert_to_count(path, filename):
    # adds Counter import
    # replaces c[i] += 1 with Counter.inc(i)
    # creates c_filename.py
    pattern = r'c\[\d+\]'

    with open(path+filename, 'r') as src, open(path+"c_"+filename, 'w') as dst:
        dst.write("from src.utils import Count \n\n")

        for line in src.readlines():
            if re.search(pattern, line):
                #Updated the code from if flag to match the regex c[integer val]
                newline = re.sub("c\[(\d)*\] \+= 1\n", "Count.incC(", line) +\
                          line.split('[')[1].split(']')[0] + ')' + '\n'
                dst.write(newline)
            else:
                dst.write(line)

    print("file " + path+"c_"+filename + " created!")
    return "c_"+filename


def add_numbers_to_nodes_python(graph):
    '''
    sdasd
    :param graph:
    :return:
    '''
    print("Adding numbers to nodes...")#, graph)
    #print("DOT graph", dot_graph.get_node_list(), '\n nodes: ', dot_graph.get_nodes())

    # the CFG of the method is always the 1 subgraph in the code when one method only
    subgraph = graph.get_subgraphs()[0]

    for node in subgraph.get_node_list():
        # we ignore nodes like 'graph' and "\n"
        if node.get_name().isnumeric():
            # merge name and label, removing "" from label, and adding new ones
            node.set("label", '"' + node.get_name() + ". " + node.get_label()[1:-1] +'"')
            # print(node.get_attributes())
            # print("NEW: ", node.get_label())
    print("...done")
    return graph

def simplify_instrumented(path, src_filename):
    '''
    removes function declaration and 1st level indentation
    to be processable by structured graph algorithm

    todo: remove also return statement?
    :param path:
    :param filename:
    :return:
    '''

    dst_filename = "s_" + src_filename
    with open(path+src_filename, 'r') as src, open(path+dst_filename, 'w') as dst:
        for line in src.readlines():
            if "def " in line:
                print("remove and skip definition")
                continue
            if line.startswith("    "):
                dst.write(line[4:])

    print("simplification done")
    return dst_filename

def run_tests_and_create_counter(path, src_file, func_name, counter_l, continue_on_no_ftests, test_file):
    '''
    run tests on function and calculate statistics
    '''

    print("******* Running tests ******")
    print("path: ", path)
    print("src_file: ", src_file)
    print("function: ", '')

    # load tests from file
    with open(test_file, 'r') as tf:
        passed_tests = json.loads(tf.readline())
        failed_tests = json.loads(tf.readline())

    print("passed_tests: ", len(passed_tests))
    print("failed_tests: ", len(failed_tests))

    #Failed Test Check Commented
    # if len(failed_tests) == 0 and continue_on_no_ftests == False:
    #     print("No failed tests! Aborting...")
    #     return



    # remove path characters, eg ../examples/trityp.
    # TODO this code is repeated in meta_tester. Pull it out into an import_module method which returns a function reference
    d = path.split('/')
    print(d, len(d))
    if '.' in d[0]:
        d.pop(0)
    print("D: ", d)
    folderp = '.'.join(d)[:-1]
    print("FOLDER: ", folderp)

    m = __import__(folderp + '.' + src_file.split(".")[0], globals(), locals(), [func_name])

    f = getattr(m, func_name)
    print("f: ", f)
       # dynamic import

    # print("passed:", passed)
    test_no = min(len(passed_tests), len(failed_tests))
    print("number of tests: ", test_no)

    # running passed
    Count.reset(counter_l)
    Count.icounter_final["passed"] = {}
    Count.icounter_final["failed"] = {}


    # for pt in passed:
    for i in range(test_no):
        # print("Test #", i+1, "f arguments:", passed_tests[i])
        Count.ireset(counter_l) # before each test

        Count.run(f, *passed_tests[i])

        Count.icounter_final["passed"][str(i + 1)] ={}
        Count.icounter_final["passed"][str(i + 1)]["inp"] = passed_tests[i]
        Count.icounter_final["passed"][str(i + 1)]["icnt"] = Count.icounter
    tp = Count.counter
    print('TP: ',tp)

    # print("xxx counter_list", counter_l)

    # running failed
    Count.reset(counter_l)
    for i in range(test_no):
        # print("Test #", i+1, "f arguments:", failed_tests[i])
        Count.ireset(counter_l)  # before each test

        Count.run(f, *failed_tests[i])

        Count.icounter_final["failed"][str(i + 1)] = {}
        Count.icounter_final["failed"][str(i + 1)]["inp"] = failed_tests[i]
        Count.icounter_final["failed"][str(i + 1)]["icnt"] = Count.icounter
    tf = Count.counter
    
    print('TF: ',tf)

    # create a file to dump individual test coverage
    with open(path + "cov_dump.json", 'w') as cdump:
        json.dump(Count.icounter_final, cdump)

    print("tpc:{}\ntfc: {}".format(tp, tf))
    # print("XXX: ", Count.icounter_final)

    # at the moment we use the same number of tests ofr no_pt and no_ft
    no_pt = test_no
    no_ft = test_no

    counter_info = {}
    counter_info_with_name = {}
    for key, value in tp.items():
        tp_values = [item['value'] for item in value]
        tf_values = [item['value'] for item in tf[key]]
        counter_info[key] = {"tp": tp_values, "tf": tf_values}

    for key, value in tp.items():
        tp_values = [{'name': item['name'], 'value': item['value']} for item in value]
        tf_values = [{'name': item['name'], 'value': item['value']} for item in tf[key]]
        counter_info_with_name[key] = {"tp": tp_values, "tf": tf_values}
    print('Counter with NAME: ',counter_info_with_name)
    return counter_info,counter_info_with_name, no_pt, no_ft


def run_tests(path, src_file, func_name, counter_l, continue_on_no_ftests,test_file):
    '''
    run tests on function and calculate statistics
        '''

    print("******* Running tests ******")
    print("path: ", path)
    print("src_file: ", src_file)
    print("function: ", func_name)

    # load tests from file
    with open(test_file, 'r') as tf:
        passed_tests = json.loads(tf.readline())
        failed_tests = json.loads(tf.readline())

    print("passed_tests: ", len(passed_tests))
    print("failed_tests: ", len(failed_tests))

    #Failed Test Check Commented
    # if len(failed_tests) == 0 and continue_on_no_ftests == False:
    #     print("No failed tests! Aborting...")
    #     return



    # remove path characters, eg ../examples/trityp.
    # TODO this code is repeated in meta_tester. Pull it out into an import_module method which returns a function reference
    d = path.split('/')
    print(d, len(d))
    if '.' in d[0]:
        d.pop(0)
    print("D: ", d)
    folderp = '.'.join(d)[:-1]
    print("FOLDER: ", folderp)

    m = __import__(folderp + '.' + src_file.split(".")[0], globals(), locals(), [func_name])

    f = getattr(m, func_name)
    print("f: ", f)
       # dynamic import

    # print("passed:", passed)
    test_no = min(len(passed_tests), len(failed_tests))
    print("number of tests: ", test_no)

    # running passed
    Count.reset(counter_l)
    Count.icounter_final["passed"] = {}
    Count.icounter_final["failed"] = {}


    # for pt in passed:
    for i in range(test_no):
        # print("Test #", i+1, "f arguments:", passed_tests[i])
        Count.ireset(counter_l) # before each test

        Count.run(f, *passed_tests[i])

        Count.icounter_final["passed"][str(i + 1)] ={}
        Count.icounter_final["passed"][str(i + 1)]["inp"] = passed_tests[i]
        Count.icounter_final["passed"][str(i + 1)]["icnt"] = Count.icounter
    tp = Count.counter

    # print("xxx counter_list", counter_l)

    # running failed
    Count.reset(counter_l)
    for i in range(test_no):
        # print("Test #", i+1, "f arguments:", failed_tests[i])
        Count.ireset(counter_l)  # before each test

        Count.run(f, *failed_tests[i])

        Count.icounter_final["failed"][str(i + 1)] = {}
        Count.icounter_final["failed"][str(i + 1)]["inp"] = failed_tests[i]
        Count.icounter_final["failed"][str(i + 1)]["icnt"] = Count.icounter
    tf = Count.counter

    # create a file to dump individual test coverage
    with open(path + "cov_dump.json", 'w') as cdump:
        json.dump(Count.icounter_final, cdump)

    print("tpc:{}\ntfc: {}".format(tp, tf))
    # print("XXX: ", Count.icounter_final)

    # at the moment we use the same number of tests ofr no_pt and no_ft
    no_pt = test_no
    no_ft = test_no
    return tp, tf, no_pt, no_ft


def calculate_suspiciousness(tp_counters, tf_counters):
    print("******* Calculating suspiciousness ******")
    tp = tp_counters
    tf = tf_counters
    ss = []

    if not tp_counters or not tf_counters:
        print("ERROR not enough tests")
        return

    number_of_tests = len(tp) + len(tf)
    print("using no tests: ", number_of_tests)

    for i in range(len(tp)):
        # if (tp[i] < tf[i]) or (tp[i] > 0 and tf[i] > 0) :
        # if tp[i] > 0 and tf[i] > 0:
        if tf[i] > 0:
            ep = tp[i]
            ef = tf[i]
            nf = number_of_tests - ef
            np = number_of_tests - ep
            oc_score = round(ef / (math.sqrt((ef + nf) * (ef + ep))), 2)
            tr_score = round((ef / (ef + nf)) / ((ef / (ef + nf)) + (ep / (ep + np))), 2)
            jc_score = round((ef / (ef + nf + ep)), 2)
            avg_score = round((oc_score+tr_score+jc_score)/3, 2)
            ss.append(avg_score)
        else:
            ss.append(0)

    print("suspicious scores: ", ss)
    return ss

def extract_susp_statements(path, src_filename, tf, ss):
    code = ""
    with open(path+src_filename) as src:
        code = src.read()

    #print("CODE: ", src_filename, code)

    module_name = src_filename.split('.')[0]
    susp_vars_module = []
    susp_statements_module =  []

    if sum(tf) > 0:
        print("sum(tf) ", len(tf))
        for i in range(len(tf)):
            # if (tp[i] < tf[i]) or (tp[i] > 0 and tf[i] > 0) :
            # if tp[i] > 0 and tf[i] > 0:
            if tf[i] > 0:
                susp_statement_numbers, susp_statements, susp_variables = get_block_level_susp_statements(code, i + 1)
                suspicious_variables = list(set(itertools.chain(*susp_variables)))
                susp_vars_module.append(suspicious_variables)
                susp_statements_module.append(list(itertools.chain(*susp_statements)))

                """
                for var in suspicious_variables:
                    if var not in ('i', 'j'): # todo why?
                        print("Susp variable to process", var)
                        def_statements, use_statements = get_def_use_statements(var, code)
                       
                        dict6 = {module_name: {
                            var: {"Block IDs": susp_block_id,
                                  "Definitions": def_statements,
                                  "Usages": use_statements}
                        }}
                        
                        json_object = json.dumps(dict6, indent=2)
                        with open(path + "Module_Def_Use_report.json", "a") as outjsfile:
                            outjsfile.write(json_object)
                """

        print("SS: ", ss)
        print("Suspicious block statements: ")
        for block in susp_statements_module:
            print("  Node: {} Statement: {}".format(block[2], block[3]))

        print("Suspicious variables: ")
        [print("  ", x) for x in set([x[0] for x in susp_variables])]

def get_block_level_susp_statements(module_code, counter_id, top_no = 3):
    pattern = r'c\[\d+\]'
    susp_statement_numbers, susp_statements, susp_variables = ([] for i in range(top_no))
    flag_cntr = 0
    flag_match_index = 0
    split_stmnt_list = list(module_code.split('\n'))
    for statement in split_stmnt_list:
        if re.search(pattern, statement):
            flag_cntr += 1
            if flag_cntr == counter_id:
                flag_match_index = split_stmnt_list.index(statement)
                susp_statement = split_stmnt_list[flag_match_index - 1].replace('\t', '')
                susp_statements.append((flag_match_index, susp_statement))
                susp_statement_numbers.append(flag_match_index)
                susp_vars = get_susp_variables(susp_statement)
                if susp_vars:
                    susp_variables.append(susp_vars)
            if flag_cntr == (counter_id + 1):
                next_flag_index = split_stmnt_list.index(statement)
                break
    try:
        next_flag_index
    except:
        next_flag_index = len(split_stmnt_list) + 1
    stop_list = ["END_IF", "ELSIF"]
    for i in range(flag_match_index + 1, next_flag_index - 1):
        if any(ss in split_stmnt_list[i] for ss in stop_list):
            break
        else:
            susp_statement = split_stmnt_list[i].replace('\t', '')
            statement = re.sub(r'^[\n\t\ ]+', '', susp_statement)
            if re.search(r"^[;(*]|^[(*]", statement) is None:
                susp_statements.append((i + 1, susp_statement))
                susp_statement_numbers.append(i + 1)
                susp_vars = get_susp_variables(susp_statement)
                if susp_vars:
                    susp_variables.append(susp_vars)

    return susp_statement_numbers, susp_statements, susp_variables


def get_susp_variables(susp_statement):
    susp_vars = []
    kw_list = ["IF", "(*", "*)", "ELSE", "ELSIF", "THEN", ">", ":=", ">=", "<", "<=", "AND", "OR", "TRUE",
               "FALSE", "+", "=", "return", "else:"]
    patterns = [r"[(]", r"[)]", r"[;]"]
    pattern = "|".join(patterns)
    statement = re.sub(r'^[\n\t\ ]+', '', susp_statement)
    if re.search(r"^[;(*]|^[(*]", statement) is None:
        statement_split_list = susp_statement.split(' ')
        for item in statement_split_list:
            if item != '':
                if any(kw in item for kw in kw_list):
                    pass
                else:
                    if re.search(r'^[0-9]', item) is None:
                        if re.findall(pattern, item):
                            if re.sub(pattern, "", item) != '':
                                susp_vars.append(re.sub(pattern, "", item))
                        else:
                            susp_vars.append(item)
        return susp_vars

def clear_folders(folder_path):
    # includes project folder + temp folder
    print("clearing " + folder_path)
    try:
        for f in glob.glob(folder_path + "*.*"):
            os.remove(f)
            print(f)
    except Exception as e:
        print("Error while clearing files:", str(e))

def delete_folders(folder_path):
    # includes project folder + temp folder
    print("clearing " + folder_path)
    try:
        shutil.rmtree(folder_path)
    except Exception as e:
        print("Error while deleting folders:", str(e))




def calculate_heatmap():
    import plotly.express as px

    susp_block_id =  [1,3,7]# provide list here
    susp_block_id_str = map(str, susp_block_id)
    # susp_block_id_str= ['1','3','7', '9', '11', '15', '19', '21']
    score_list =  [[1],[3],[4]]# provide list of scores here
    fig = px.imshow(score_list, zmin=0, zmax=1, aspect='equal', width=360,
                    labels=dict(x="Suspiciousness Metric formula", y="Block_ID w.r.t var_in_a_sub)",
                                color="Suspiciousness score"),
                    x=['Average_score'],
                    y=list(susp_block_id_str),
                    text_auto=True)
    fig.update_traces(xgap=3, selector=dict(type='heatmap'))
    fig.update_traces(ygap=3, selector=dict(type='heatmap'))
    fig.write_image( "RESULT" + "_hm.svg")



def generate_html_report(path,temp_folder,output_file,test_file,src):
    try:
        print("Generating Report ....")
        html = "<html>\n" \
               "<head>\n" \
               "<meta charset='UTF-8'>\n" \
               "<title> Localizer Report </title>\n" \
               "<style>\n" \
               "table, td, tr {{\n" \
               "   border: black solid 1px\n" \
               "}}\n" \
               "</style>\n" \
               "</head>\n" \
               "<body><div id='top'></div\n" \
               "<p>Generated: {}</p>".format(datetime.datetime.now())

        # load tests from file
        with open(test_file, 'r') as tf:
            passed_tests = json.loads(tf.readline())
            failed_tests = json.loads(tf.readline())
        
        html+="<h1><strong>{}</strong></h1><hr/>\n".format( str(src))
        html+="<h2><strong>Tests Inputs</strong></h2>\n"
        html+="<p>Passed: {}</p>\n".format( str(passed_tests))
        html+="<p>Failed: {}</p>\n".format( str(failed_tests))
        # todo add program name
        # todo use svg instead of png
        # html += "<h1>PRG</h1>" \
        #         "<object type='image/svg+xml' data='CG.svg' id='0'></object>\n" \
        #         "<hr>\n"
        #html+= "<h1>PRG</h1>" \
        resources_folder=path+"resources/"
        images_folder=resources_folder+"images/"
        
        print("CG Path: ",images_folder+"CG.svg",)
        svg_content=''
        with open(images_folder+"CG.svg", "r") as svg_file:
            # Read the content of the SVG file into a string
            svg_content = svg_file.read()


        # Find the index of the first occurrence of "<svg"
        start_index = svg_content.find("<svg")

        # If "<svg" is found, extract the substring starting from that index
        if start_index != -1:
            svg_content = svg_content[start_index:]

        html+= svg_content
        print('HTML: ',html )

        html+="<hr>\n"




        # print("passed_tests: ", len(passed_tests))
        # print("failed_tests: ", len(failed_tests))

        # collecting files from the local folder
        toc_list = ""
        img_list = ""
        print("Resources file: ",resources_folder,os.listdir(resources_folder))
        for file in os.listdir(images_folder):
            print("GENERATE HTML File: ",file)
            if "_cfg.svg" in file.split()[0] and not "simp" in file.split()[0]:
                print(file.split()[0])
                module_name = file.split()[0][:-8]
                toc_list += "<li><a href='#{}'>{}</a></li>\n".format(module_name, module_name)
                img_list += "<div id={}>\n" \
                            "<hr>\n" \
                            "<h2>{}</h2>\n" \
                            "<div style='display: flex;flex-wrap: wrap;justify-content: flex-start;align-items: flex-start;max-width: 100%;overflow-x: hidden;'>\n" \
                            "<div style='flex: 1 1 auto;margin: 5px;overflow: hidden'>\n" \
                            "<object type='image/svg+xml' data={} ></object>\n" \
                            "</div>\n" \
                            "<div style='flex: 8;'>\n" \
                            "<object type='image/svg+xml' data={} style=' max-width: 100%;height: auto;'></object>\n" \
                            "</div></div>\n" \
                            "<a href={} target='_blank''>View CFG</a><br>\n" \
                            "<a href='#top'>Back</a>\n" \
                            "<hr>\n" \
                            "</div>\n".format(module_name,module_name,"resources/images/"+module_name + "_hm.svg","resources/images/"+file.split()[0],"resources/images/"+file.split()[0])



                            

        toc_list += "<li><a href='#table'>Susp table</a></li>"
        html += toc_list
        html += img_list

        #
        old_path =path
        # new_folder_name = "cclLps_temp/"

        # # Get the index of the last occurrence of '/'
        # directory = os.path.dirname(os.path.dirname(old_path))

        # # Replace the last folder name with the new one
        # new_directory = os.path.join(directory, new_folder_name)
        # print ("OLD PATH ",directory)
        # print ("FAULT INFO JSON: ",new_directory+output_file)
        # #

        # todo refactor when fault susp is generated automatically
        html += json_to_html_table(path=temp_folder, json_file=output_file,resources_folder=resources_folder)

        with open(path + "fault_report.html", 'w') as rfile:
            rfile.write(html)

    except Exception as e:
        print(f"Error generating HTML report: {e}")
        # You can choose to exit the script or handle the error in another way here

def generate_simp_html_report(path,temp_folder,output_file,test_file,src):
    try:
        print("Generating Simple Report ....")
        html = "<html>\n" \
               "<head>\n" \
               "<meta charset='UTF-8'>\n" \
               "<title> Localizer Simplified Report </title>\n" \
               "<style>\n" \
               "table, td, tr {{\n" \
               "   border: black solid 1px\n" \
               "}}\n" \
               "</style>\n" \
               "</head>\n" \
               "<body><div id='top'></div\n" \
               "<p>Generated: {}</p>".format(datetime.datetime.now())

        resources_folder=path+"resources/"
        images_folder=resources_folder+"images/"
        html+="<h1><strong>{}</strong></h1><hr/>\n".format( str(src))

                # load tests from file
        with open(test_file, 'r') as tf:
            passed_tests = json.loads(tf.readline())
            failed_tests = json.loads(tf.readline())

        html+="<h2><strong>Tests Inputs</strong></h2>\n"
        html+="<p>Passed: {}</p>\n".format( str(passed_tests)[1:-1])
        html+="<p>Failed: {}</p>\n".format( str(failed_tests)[1:-1])

        svg_content=''
        with open(images_folder+"CG_simp.svg", "r") as svg_file:
            # Read the content of the SVG file into a string
            svg_content = svg_file.read()

        # Find the index of the first occurrence of "<svg"
        start_index = svg_content.find("<svg")

        # If "<svg" is found, extract the substring starting from that index
        if start_index != -1:
            svg_content = svg_content[start_index:]


        html+= svg_content

        html+="<hr>\n"

        # collecting files from the local folder
        toc_list = ""
        img_list = ""
        for file in os.listdir(images_folder):
            print("File: ",file)
            if "_cfg.svg" in file and "simp" in file.split()[0]:
                print(file.split()[0])
                module_name = file.split()[0][:-8] 
                hm_name = module_name[5:] 

                toc_list += "<li><a href='#{}'>{}</a></li>\n".format(hm_name, hm_name)
                img_list += "<div id={}>\n" \
                            "<hr>\n" \
                            "<h2>{}</h2>\n" \
                            "<div style='display: flex;flex-wrap: wrap;justify-content: flex-start;align-items: flex-start;max-width: 100%;overflow-x: hidden;'>\n" \
                            "<div style='flex: 1 1 auto;margin: 5px;overflow: hidden'>\n" \
                            "<object type='image/svg+xml' data={} ></object>\n" \
                            "</div>\n" \
                            "<div style='flex: 8;'>\n" \
                            "<object type='image/svg+xml' data={} style=' max-width: 100%;height: auto;'></object>\n" \
                            "</div></div>\n" \
                            "<a href={} target='_blank''>View CFG</a><br>\n" \
                            "<a href='#top'>Back</a>\n" \
                            "<hr>\n" \
                            "</div>\n".format(hm_name,hm_name,"resources/images/"+hm_name + "_hm.svg","resources/images/"+file.split()[0],"resources/images/"+file.split()[0])

        toc_list += "<li><a href='#table'>Susp table</a></li>"
        html += toc_list
        html += img_list


        old_path =  path
        # new_folder_name = "cclLps_temp/"
        # # Get the index of the last occurrence of '/'
        # directory = os.path.dirname(os.path.dirname(old_path))

        # # Replace the last folder name with the new one
        # new_directory = os.path.join(directory, new_folder_name)
        # print ("OLD PATH ",directory)
        # print ("FAULT INFO JSON: ",new_directory+output_file)
        #

        # todo refactor when fault susp is generated automatically
        html += json_to_html_table(path=temp_folder, json_file=output_file,resources_folder=resources_folder)
        html += "</body>\n</html>"

        with open(path + "simp_fault_report.html", 'w') as rfile:
            rfile.write(html)

    except Exception as e:
        print(f"Error generating HTML report: {e}")
        # You can choose to exit the script or handle the error in another way here

def json_to_html_table(path, json_file,resources_folder,threshold=0.5):
    result = "<style>\n" \
             "table {\n" \
             "    border-collapse: collapse;\n" \
             "    border: 1px solid black;\n" \
             "    margin: 0;\n" \
             "    padding: 0;\n" \
             "}\n" \
             "th, td {\n" \
             "    border: none;\n" \
             "    border-right: 1px solid;\n" \
             "    text-align: left;\n" \
             "    vertical-align: top; /* Align content to the top vertically */\n" \
             "}\n" \
             "td:first-child {\n" \
             "    word-wrap: nowrap;\n"  \
             "}\n" \
             "tr {\n" \
             "    border: none;\n" \
             "}\n" \
             ".grey-background {\n" \
             "    background-color: transparent;\n" \
             "    border: none;\n" \
             "}\n" \
             "</style>\n"

    result += "<div>\n" \
              "\t<label for='threshold'>Threshold:</label>\n" \
              "\t<input type='number' id='threshold' name='threshold' step='0.01' value='0.57'>\n" \
              "\t<button onclick='updateTable()'>Update the Table</button>\n" \
              "</div>\n"

    result += "<h2>Suspiciousness Score per basic blocks per the above threshold</h2><table id='table'>\n"\

    result += "<tr>\n" \
              "\t<th style='border:1px solid black'>Module Name</th>\n" \
              "\t<th style='border:1px solid black'>Max Score</th>\n" \
              "\t<th style='border:1px solid black'>Susp. Score</th>\n" \
              "\t<th style='border:1px solid black'>Block ID</th>\n" \
              "\t<th style='border:1px solid black'>Statements</th>\n" \
              "</tr>\n"

    with open(path + json_file, 'r') as src:
        jdata = json.load(src)

        print('SUMMARY JSON DATA. ',jdata)

        prev_module_name = None
        prev_max_score = None
        prev_score = None
        i = 0
        for entry in jdata:
            module_name = entry.get('Module_name', '')
            max_score = entry.get('Max_score', '')
            block_info = entry.get('Block_Info', [])
            print('MOD: ',module_name,max_score,block_info)
            prev_block_id = None
            j = 0
            if len(block_info) > 0:

                for block in block_info:

                    block_id = block.get('Block ID', '')
                    susp_score = block.get('Susp. score', 0.0)
                    statements_info = block.get('Statements_info', [])

                    for statement in statements_info:
                        line_number = statement.get('line_number', '')
                        statement_text = statement.get('statement', '')

                        print('STATEMENTSSSSS: ',statement)

                        # Check if the current module name is equal to the previous one
                        module_td = "<td style='width:300px'> <a href='#{}'>{}</a><span><a href='{}' target='_blank'> <i>(View Code)</i></a></span></td>".format(module_name,module_name,'resources/code_files/'+module_name+".py")
                        max_score_td ="<td>{}</td>".format(max_score)
                        susp_score_td =  "<td>{}</td>".format(susp_score)
                        block_id_td = "<td>{}</td>".format(block_id)
                        result += "<tr>\n" \
                                    "\t{}" \
                                    "\t{}" \
                                    "\t{}" \
                                    "\t{}\n" \
                                    "\t<td>{}</td>\n" \
                                    "</tr>\n".format(module_td, max_score_td, susp_score_td, block_id_td, statement_text)
                        
                        print('RESULT: ',result)
                        # Update the previous module name
                        prev_module_name = module_name
                        prev_max_score = max_score
                        prev_score = susp_score
                        prev_block_id = block_id

                    result += "<tr class='empty-row' style='height:30px'>\n" \
                                "\t<td colspan='1'></td>\n" \
                                "\t<td colspan='1'></td>\n" \
                                "\t<td colspan='1'></td>\n" \
                                "\t<td colspan='1'></td>\n" \
                                "\t<td colspan='1'></td>\n" \
                                "</tr>\n"
            else:
                result += "<tr>\n" \
                          "\t<td><a href='#{}'>{}</a></td>\n" \
                          "\t<td>-</td>\n" \
                          "\t<td>-</td>\n" \
                          "\t<td>-</td>\n" \
                          "\t<td>-</td>\n" \
                          "</tr>\n".format(module_name, module_name)

            # Add the row with transparent background
            result += "<tr class='grey-background'>\n" \
                      "\t<td></td>\n" \
                      "\t<td></td>\n" \
                      "\t<td></td>\n" \
                      "\t<td></td>\n" \
                      "\t<td></td>\n" \
                      "</tr>\n"

            i += 1

    result += '''
    <script>
    // Define global variables to store previous values

    function updateTable() {
        var threshold = parseFloat(document.getElementById('threshold').value);
        var rows = document.getElementById('table').getElementsByTagName('tr');
        for (var i = 1; i < rows.length; i++) {
            var moduleCell = rows[i].getElementsByTagName('td')[0];
            var maxScoreCell = rows[i].getElementsByTagName('td')[1];
            var suspScoreCell = rows[i].getElementsByTagName('td')[2];
            var blockIdCell = rows[i].getElementsByTagName('td')[3];
            var moduleName = rows[i].getElementsByTagName('td')[0].getElementsByTagName('a')[0]?.textContent;
            rows[i].style.display = 'none';
            var suspScore = parseFloat(suspScoreCell.innerText);
        }
        
        var prevModuleName = null;
        var prevMaxScore = null;
        var prevScore = null;
        var prevBlockId = null;
        
        for (var i = 1; i < rows.length; i++) {
            var moduleCell = rows[i].getElementsByTagName('td')[0];
            var maxScoreCell = rows[i].getElementsByTagName('td')[1];
            var suspScoreCell = rows[i].getElementsByTagName('td')[2];
            var blockIdCell = rows[i].getElementsByTagName('td')[3];
            var moduleName = rows[i].getElementsByTagName('td')[0].getElementsByTagName('a')[0]?.textContent;

            var suspScore = parseFloat(suspScoreCell.innerText);


            if (suspScore > threshold && suspScore) {
                rows[i].style.display = 'table-row';
                var maxScore = parseFloat(maxScoreCell.innerText); 
                var suspScore = parseFloat(suspScoreCell.innerText); 
                var blockId = blockIdCell.innerText;
                
                console.log("Module Name: ",moduleName);
                if(moduleName == prevModuleName){
                moduleCell.getElementsByTagName('a')[0].style.color="white"
                moduleCell.getElementsByTagName('a')[1].style.color="white"
                moduleCell.style.borderLeft="black"
                moduleCell.style.borderRight="black"
                }
                else{
                moduleCell.getElementsByTagName('a')[0].style.color="black"
                moduleCell.getElementsByTagName('a')[1].style.color="black"
                moduleCell.style.borderLeft="black"
                moduleCell.style.borderRight="black"
                }
                
                if( prevMaxScore === maxScore){
                maxScoreCell.style.color="white"
                maxScoreCell.style.borderLeft="1px solid black"
                maxScoreCell.style.borderRight="1px solid black"
                }
                else{
                maxScoreCell.style.color="black"
                maxScoreCell.style.borderLeft="1px solid black"
                maxScoreCell.style.borderRight="1px solid black"
                }
                
                if( prevScore === suspScore){
                suspScoreCell.style.color="white"
                suspScoreCell.style.borderLeft="1px solid black"
                suspScoreCell.style.borderRight="1px solid black"
                }
                else{
                suspScoreCell.style.color="black"
                suspScoreCell.style.borderLeft="1px solid black"
                suspScoreCell.style.borderRight="1px solid black"
                }
                
                if( prevBlockId === blockId){
                blockIdCell.style.color="white"
                blockIdCell.style.borderLeft="1px solid black"
                blockIdCell.style.borderRight="1px solid black"
                }
                
                else{
                blockIdCell.style.color="black"
                blockIdCell.style.borderLeft="1px solid black"
                blockIdCell.style.borderRight="1px solid black"
                }
                

                
                prevModuleName = moduleName; 
                prevMaxScore = maxScore; 
                prevScore = suspScore;
                prevBlockId = blockId; 
            }
        }
    
		prevModuleName = null;
		prevMaxScore = null;
		prevScore = null;
		prevBlockId = null;
		for (var i = 1; i < rows.length; i++) {
			var moduleCell = rows[i].getElementsByTagName('td')[0];
			var maxScoreCell = rows[i].getElementsByTagName('td')[1];
			var suspScoreCell = rows[i].getElementsByTagName('td')[2];
			var blockIdCell = rows[i].getElementsByTagName('td')[3];
			var moduleName = rows[i].getElementsByTagName('td')[0].getElementsByTagName('a')[0]?.textContent;
			
			var maxScore = parseFloat(maxScoreCell.innerText); 
			var suspScore = parseFloat(suspScoreCell.innerText); 
			var blockId = blockIdCell.innerText;
			var isEmptyNextRow = rows[i + 1] && rows[i + 1].classList.contains('empty-row');
			var isDisplay=rows[i].style.display==='table-row'
			
			
			if(blockId===prevBlockId && prevScore === suspScore && isEmptyNextRow && isDisplay){
				rows[i+1].style.display = 'table-row';
			}
			
			
			
			 prevModuleName = moduleName; 
			 prevMaxScore = maxScore; 
			 prevScore = suspScore;
			 prevBlockId = blockId; 
		

		}
	
	}
	


    window.onload = function() {
        updateTable();
    }
    </script>
    '''



    result += "</table>\n"

    return result

def extract_name_without_extension(file):
    return file.split('.')[0]


def is_class_based(filepath):
    try:
        with open(filepath, 'r') as file:
            code = file.read()
        module_ast = ast.parse(code)
    except (SyntaxError, FileNotFoundError, IOError) as e:
        print(f"Error reading or parsing file: {e}")
        return False
    
    # Check for class definition
    for node in ast.walk(module_ast):
        if isinstance(node, ast.ClassDef):
            return True



class ClassToFunctionTransformer(ast.NodeTransformer):
    def visit_ClassDef(self, node):
        new_functions = []
        
        # Iterate through each function definition in the class
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                # Convert each method into a standalone function
                new_function = self.convert_method_to_function(stmt)
                new_functions.extend(new_function)
        
        # Return the list of new function definitions to replace the class
        return new_functions
    
    def convert_method_to_function(self, func_node):
        # Remove 'self' parameter if present in method
        if func_node.args.args and func_node.args.args[0].arg == 'self':
            func_node.args.args.pop(0)
        
        # Convert the method body to a standalone function body
        return [func_node]

class ClassToFunctionTransformer(ast.NodeTransformer):
    def visit_ClassDef(self, node):
        new_functions = []
        
        # Iterate through each function definition in the class
        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                # Convert each method into a standalone function
                new_function = self.convert_method_to_function(stmt)
                new_functions.extend(new_function)
        
        # Return the list of new function definitions to replace the class
        return new_functions
    
    def convert_method_to_function(self, func_node):
        # Remove 'self' parameter if present in method
        if func_node.args.args and func_node.args.args[0].arg == 'self':
            func_node.args.args.pop(0)
        
        # Remove any decorators (like staticmethod)
        func_node.decorator_list = []

        return [func_node]

def remove_self_references(tree):
    # Function to remove 'self.' references from the AST
    class SelfReferenceRemover(ast.NodeTransformer):
        def visit_Attribute(self, node):
            if isinstance(node.value, ast.Name) and node.value.id == 'self':
                return ast.copy_location(ast.Name(id=node.attr, ctx=node.ctx), node)
            return node
    
    # Apply the SelfReferenceRemover to the entire AST
    transformer = SelfReferenceRemover()
    transformed_tree = transformer.visit(tree)
    return transformed_tree

def convert_to_function_based(file_path):
    # Read the content of the original file
    with open(file_path, 'r') as file:
        code = file.read()

    # Parse the code into an Abstract Syntax Tree (AST)
    tree = ast.parse(code)

    # Transformer to convert class-based code to function-based code
    class_to_function = ClassToFunctionTransformer()
    transformed_tree = class_to_function.visit(tree)

    # Remove 'self.' references from the transformed AST
    cleaned_tree = remove_self_references(transformed_tree)

    # Generate Python code from the cleaned AST
    transformed_code = ast.unparse(cleaned_tree)

    # Overwrite the original file with the transformed code
    with open(file_path, 'w') as file:
        file.write(transformed_code)

    print(f"Conversion complete. '{file_path}' has been updated.")
def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        print(f"File {os.path.basename(src)} successfully copied to {dst}")
    except FileNotFoundError:
        print(f"Source file {src} not found.")
    except PermissionError:
        print(f"Permission denied when trying to copy to {dst}")
    except Exception as e:
        print(f"An error occurred: {e}")


def remove_c_increments(code: str) -> str:
    """
    Remove all instances of 'c[]+=1' from the given code string.
    
    :param code: The input code as a string.
    :return: The modified code as a string.
    """
    # Define the pattern to find 'c[] += 1'
    pattern = r'c\[\d+\] \+= 1\s*'
    
    # Remove all matches of the pattern from the code
    modified_code = re.sub(pattern, '', code)
    
    return modified_code