import re
import os

def instrument_python_code( temp_path, special_statements, src_filename, flag =True,  indentsize=4):
    '''
    # read one line and save it to another file. If special statements in the line, first add a counter statement
    # indentsize = 4 by default
    :param path:
    :param src_filename:
    :param indentsize:
    :param special_statements: control statements after which we add counters
    :return: instrumented file
    '''

    print("Instrumenting file: ", src_filename)
    print("working in folder: ", os.getcwd())
    print("flag is", flag)
    # some special_statements have a space after

    # detect spaces or tabs in indentation
    # read lines until we find some spaces or tabs
    tabs = False
    spaces = False

    with open(temp_path +'/'+ src_filename) as src:
        for line in src.readlines():
            if re.match(' ', line):
                spaces = True
                print(" space indentation detected")
                one_indent = ''.join(' ' for i in range(indentsize))
                break
            if re.match('\t', line):
                print(" tab indentation detected")
                tabs = True
                one_indent = '\t'
                break
    #print("detected indentation, spaces/tabs: ", spaces, tabs)
    assert spaces or tabs, "indentation not detected"
    assert not (spaces and tabs), "both indentations detected"
    print("indent:", one_indent,".", len(one_indent))

    counter_list = []
    # to be used later
    line_number = 0
    code2lines = {}
    method_content=''
    method_name=''
    counter_list_per_module={}

    with open(temp_path + '/'+src_filename) as src, open(temp_path + "/i_"+src_filename, 'w') as dst:
        for line in src.readlines():
            if 'def' in line:
                if method_content:
                    # if line contains special statements add counters statements and add 'one' to indentation
                    adding_counters(method_content,method_name,line_number,one_indent,spaces,tabs,special_statements,flag, counter_list, code2lines,dst,counter_list_per_module)
                    method_content=''   
                method_name = line.split("def ")[1].split("(")[0].strip()
                counter_list_per_module[method_name]=[]
            method_content+=line       
        if method_content:
            adding_counters(method_content,method_name,line_number,one_indent,spaces,tabs,special_statements,flag, counter_list, code2lines,dst,counter_list_per_module)
    
    counters_after_defs(temp_path, src_filename, counter_list_per_module, one_indent,spaces, tabs, counter_list)
    return "i_"+src_filename, counter_list, counter_list_per_module



def adding_counters(method_content,method_name,line_number,one_indent,spaces,tabs,special_statements,flag, counter_list, code2lines,dst,counter_list_per_module):
    method_content_lines = method_content.splitlines()
    print(method_content)
    for method_line in method_content_lines:
        print('Method inner: ',method_line)
        line_number += 1
        #line text saved in dictionary at line nuber
        code2lines[line_number] = method_line
        dst.write(method_line+'\n')
        words_in_method_line = method_line.strip().strip(':').split()
        print('Words in method line: ',words_in_method_line)

        if any(word in special_statements for word in words_in_method_line) and not method_line.strip().strip(':').startswith('#'):    
            print("special statement found: ", method_line)
            # print("indent: ", len(re.findall("^ *", line)[0]))

            # check current indentation and add one more
            if spaces:
                crt_indent = re.findall("^ *", method_line)[0]
                new_indent = crt_indent + one_indent
            if tabs:
                crt_indent = re.findall("^\t*", method_line)[0]
                new_indent = crt_indent + one_indent

            counter_list.append(0)


            str_to_write = new_indent + "c[" + str(len(counter_list)) + "] += 1\n"

            dst.write(str_to_write)


            pattern = r'c\[\d+]'
            match = re.search(pattern, str_to_write)  # Search for the pattern in the line
            counter_name=''
            if match: 
                counter_name=str(match.group())

            counter_list_per_module[method_name].append({'name':len(counter_list),'value':0})
    


def counters_after_defs(temp_path, src_filename, counter_list_per_module, one_indent,spaces, tabs, counter_list):
        # Read the file content
        with open(temp_path + "/i_"+src_filename, 'r') as file:
            lines = file.readlines()
            # Edit the file content to add c[1] += 1 after every def
        with open(temp_path + "/i_"+src_filename, 'w') as file:
            for line in lines:
                file.write(line)
                if line.strip().startswith("def "):
                    method_name = line.split("def ")[1].split("(")[0].strip()
                    if spaces:
                        crt_indent = re.findall("^ *", line)[0]
                        new_indent = crt_indent + one_indent
                    if tabs:
                        crt_indent = re.findall("^\t*", line)[0]
                        new_indent = crt_indent + one_indent

                    counter_list.append(0)
                    str_to_write = new_indent + "c[" + str(len(counter_list)) + "] += 1\n"
                    file.write(str_to_write)
                    counter_list_per_module[method_name].append({'name':len(counter_list),'value':0})

        