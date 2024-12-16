import os
import sys
import glob

from src.graph import MGraph
from src import utils
from src import instrumenter
from src import graph
import pydot
import math
import json
import re
import itertools
import copy
import importlib

import pandas as pd
import seaborn as sns
import networkx as nx
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
import matplotlib
import fnmatch

from src.call_graph_generator import CallGraphProcessor
import shutil
matplotlib.use('Agg')

class Localizer:
    def __init__(self,
                 project_path,
                 file_n,
                 control_statements=None,
                 clear_folders=True,
                 continue_on_no_ftests=False,
                 test_file="",
                 debug =True,
                 outputFile='',
                 entry_point='',
                 metric=''
                 ):

        self.test_file = test_file
        self.no_tf = None
        self.no_tp = None
        self.tf_counters = None
        self.tp_counters = None
        self.simplified_instrumented_py_src_fn = None
        self.mgraph = None
        self.instrumented_py_src_fn = None
        self.counter_list = None
        self.counter_instrumented_py_src_fn = None
        if control_statements is None:
            self.control_statements = {'for', 'if', 'else', 'elif', 'while'}

        self.continue_on_no_ftests = continue_on_no_ftests

        self.project_path = project_path
        self.module_name = ''
        self.file_n = file_n
        self.src_file_name=file_n.split('.')[0]
        self.temp_folder = project_path + self.src_file_name+ "_temp/"
        self.debug_folder = project_path + self.src_file_name + "_debug/"
        self.function = entry_point
        self.DEBUG = debug
        self.outputFile=outputFile
        self.summary_info=[]
        self.report_folder = self.project_path + "reports/"
        self.resource_folder = self.report_folder+"resources/"
        self.images_folder = self.resource_folder+"images/"
        self.code_folder= self.resource_folder+"code_files/"
        #
        self.module_hits=[]
        self.module_names=[]
        self.scores={}
        self.src =file_n
        self.call_graph_processor= None
        self.counters=[]
        self.splitted_instrumented_src=[]
        self.counter_list_per_module=[]
        self.counters_info_per_module=[]
        self.counters_info_per_module_with_name={}
        self.suspicious_score_metric=metric
        #
        print(f"working config: "
              f"\n File name: {self.module_name}"
              f"\n Project path: {self.project_path}"
              f"\n Temp folder: {self.temp_folder} "
              f"\n Debug folder: {self.debug_folder}"
              f"\n DEBUG: {self.DEBUG}")

        # create temp folder
        self.__create_temp__(self.temp_folder, clear_folders)

        if self.DEBUG:
            # create debug folder
            self.__create_debug__(self.debug_folder, clear_folders)
                # create temp folder

        #create report folder
        self.__create_report__(self.report_folder, clear_folders)

        #create resource folder
        self.__create_resource__(self.resource_folder, clear_folders)

        self.__create_images_folder__(self.images_folder, clear_folders)
        self.__create_code_folder__(self.code_folder, clear_folders)

        self.call_graph_processor= CallGraphProcessor(
        entry_point=[self.project_path + self.src],
        package=self.project_path,
        as_graph_output=self.temp_folder + "your_as_graph_output.json",
        output=self.temp_folder + "output.json",
        output_image_path=self.temp_folder + 'CG'
        )
        print('TEMP FOLDER: ',self.temp_folder )

    def __create_temp__(self, folder, clear):
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
            else:
                print("temp folder exists")
                if clear:
                    utils.clear_folders(folder)
            print("Temp folder created")
        except Exception as e:
            print(e)

    def __create_debug__(self, folder, clear):
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
            else:
                print("debug folder exists")
                if clear:
                    utils.clear_folders(self.debug_folder)
            print("debug folder created")
        except Exception as e:
            print(e)

    def __create_report__(self, folder, clear):
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
                self.__create_resource__(self.resource_folder, clear)
            else:
                print("report folder exists")
                if clear:
                    utils.clear_folders(self.report_folder)
            print("report folder created")
        except Exception as e:
            print(e)
    # creating resource folder
    def __create_resource__(self, folder, clear):
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
            else:
                print("resource folder exists")
                if clear:
                    utils.clear_folders(self.resource_folder)
            print("resource folder created")
        except Exception as e:
            print(e)

        # creating resource folder
    def __create_code_folder__(self, folder, clear):
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
            else:
                print("resource folder exists")
                if clear:
                    utils.clear_folders(self.code_folder)
            print("resource folder created")
        except Exception as e:
            print(e)
    def __create_images_folder__(self, folder, clear):
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
            else:
                print("resource folder exists")
                if clear:
                    utils.clear_folders(self.images_folder)
            print("resource folder created")
        except Exception as e:
            print(e)
    
    def instrument_python(self):
        # instrument code, result in i_...py
        # TODO make generic
        yield "Instrumenting "+self.file_n+'...'

        self.instrumented_py_src_fn, self.counter_list,self.counter_list_per_module = instrumenter.instrument_python_code(
            temp_path=self.temp_folder,
            src_filename=self.file_n,
            special_statements=self.control_statements
            )

        print('Counter List Per Module: ',self.counter_list_per_module)
        print('Counter List: ',self.counter_list)
        yield "Simplifying "+self.file_n+'...'
        self.simplified_instrumented_py_src_fn = utils.simplify_instrumented(path=self.temp_folder, src_filename=self.instrumented_py_src_fn)

    def create_cfg(self):
        try:
            print("Building initial graph...")
            print('SIMPLIFIED INSTRUMENT: ', self.simplified_instrumented_py_src_fn)
            
            # Create initial cfg using staticfg
            crt_graph = graph.build_cfg(self.temp_folder, self.simplified_instrumented_py_src_fn, formats=['dot'], calls=False)

            # Create graph from DOT file using pydot for manipulation
            dot_graph = pydot.graph_from_dot_file(self.temp_folder + self.simplified_instrumented_py_src_fn.split('.')[0] + ".dot")[0]
            
            # Set attributes to reduce edge label overlap


            if self.DEBUG:
                dot_graph.write_png(self.debug_folder + self.module_name + "_1.png")

            self.mgraph = MGraph(dot_graph)

            self.mgraph.add_numbers_to_node()
            
            if self.DEBUG:
                self.mgraph.write2png(self.debug_folder + self.module_name + "_2.png")

            self.mgraph.remove_counter_elements_from_nodes_and_adding_to_edges()
            
            if self.DEBUG:
                self.mgraph.write2png(self.debug_folder + self.module_name + "_3.png")

            # Convert i_..py to Count format, output is "c_i_example.Program.py"
            self.counter_instrumented_py_src_fn = utils.convert_to_count(path=self.temp_folder, filename=self.instrumented_py_src_fn)
            
            print("p: create CFG done.")
        except Exception as e:
            print('Error: ', e)
            
    def execute_tests(self):
        yield "Executing tests..."
        # check if tests exist
        if self.test_file is None:
            return
            # using default
            # if not os.path.exists(self.temp_folder+"meta_tests.txt"):
            #     print(f"ERROR: tests not found! in {self.temp_folder} meta_tests.txt")
            #     return
        else:
            if not os.path.exists(self.test_file):
                yield "ERROR: tests not found! in "+ self.test_file
                return
        yield f"using file {self.test_file}"
              
        # convert i_..py to Count format, output is "c_i_example.Program.py"
        self.counter_instrumented_py_src_fn = utils.convert_to_count(path=self.temp_folder,
                                                                    filename=self.instrumented_py_src_fn)
        self.counters_info_per_module,self.counters_info_per_module_with_name,self.no_tp, self.no_tf=utils.run_tests_and_create_counter(self.temp_folder,
                                                            self.counter_instrumented_py_src_fn,
                                                            self.function,
                                                            self.counter_list_per_module,
                                                            self.continue_on_no_ftests,
                                                            self.test_file)
        

        print("execution done")
        yield "Execution done"

    def get_block_level_susp_statements(self, module_code, counter_id, top_no=3):
        susp_statement_numbers, susp_statements, susp_variables = ([] for i in range(top_no))
        statementsinfo = []
        flag_cntr = 0
        flag_match_index = 0
        split_stmnt_list = list(module_code.split('\n'))
        pattern = r'c\[\d+\]'
        for statement in split_stmnt_list:
            if re.search(pattern, statement):
                print('COUNTER NAME: ',statement)
                flag_cntr += 1
                if flag_cntr == counter_id:
                    flag_match_index = split_stmnt_list.index(statement)
                    susp_statement = split_stmnt_list[flag_match_index - 1].replace('\t', '')
                    susp_statements.append(susp_statement)
                    susp_statement_numbers.append(flag_match_index)
                    susp_vars = self.get_susp_variables(susp_statement)
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
        match_patterns = [r'\(\*', r'\;\(\*', r'^\s*$']
        match_pattern = "|".join(match_patterns)
        for i in range(flag_match_index + 1, next_flag_index - 1):
            if any(ss in split_stmnt_list[i] for ss in stop_list):
                break
            else:
                susp_statement = split_stmnt_list[i].replace('\t', '')
                statement = re.sub(r'^[\n\t]+', '', susp_statement)
                if re.search(match_pattern, statement) is None:
                    susp_statements.append(susp_statement)
                    susp_statement_numbers.append(i + 1)
                    susp_vars = self.get_susp_variables(susp_statement)
                    if susp_vars:
                        susp_variables.append(susp_vars)
        for line_no, statement in zip(susp_statement_numbers, susp_statements):
            record = {'line_number': line_no, 'statement': statement}
            statementsinfo.append(record)

        return statementsinfo, susp_variables

    def get_block_level_statements(self, module_code, edge, top_no=3):
        statementsinfo = []
        split_stmnt_list = list(module_code.split('\n'))
        print('STATEMENT LIST: ',split_stmnt_list)
        record = {'line_number': edge_no, 'statement': statement}
        node=self.mgraph.find_node(edge_no)
        
        statementsinfo.append(record)

        return statementsinfo

    def calculate_suspiciousness(self,module_name):
        print("******* Calculating suspiciousness ******")
        susp_block_id, susp_vars_module, susp_score, susp_statements_module, def_use_statements_module, block_info \
            = ([] for i in range(6))
        tp = self.counters_info_per_module_with_name[module_name]['tp']
        tf = self.counters_info_per_module_with_name[module_name]['tf']

        print('Calculating S')
        print('Module Name: ',module_name,' Test Passed: ',tp,' Test Failed: ',tf)
        ss = []
        ss_with_name = []
        if not self.tp_counters or not self.tf_counters:
            print("not enough tests")
            return ss, ss_with_name, block_info

        if self.no_tp == self.no_tf:
            number_of_tests = self.no_tf
        else:
            number_of_tests = min(self.no_tf, self.no_tp)
        print("using no tests: ", number_of_tests)

        for i in range(len(tp)):
            if tf[i]['value'] > 0:
                ep = tp[i]['value']
                ef = tf[i]['value']
                nf = number_of_tests - ef
                np = number_of_tests - ep
                oc_score = round(ef / (math.sqrt((ef + nf) * (ef + ep))), 2)
                tr_score = round((ef / (ef + nf)) / ((ef / (ef + nf)) + (ep / (ep + np))), 2)
                jc_score = round((ef / (ef + nf + ep)), 2)
                avg_score = round((oc_score + tr_score + jc_score) / 3, 2)
                print('tf[i][VALUE]',tp[i]['name'],tp[i]['value'],avg_score)
                ss.append(avg_score)
                ss_with_name.append({'name': tp[i]['name'],'value':avg_score})
                print('SIMPLIFIED: ',self.simplified_instrumented_py_src_fn)

                module_code=self.get_simplified_module_code(self.temp_folder,self.instrumented_py_src_fn)
                statementsinfo, susp_variables = self.get_block_level_susp_statements(module_code, i + 1)
                susp_block_id.append(i + 1)
                suspicious_variables = list(set(itertools.chain(*susp_variables)))
                susp_vars_module.append(suspicious_variables)
                susp_block_dict = {
                    "Block ID": i + 1,
                    "Susp. score": avg_score,
                    "Statements_info": statementsinfo,
                }
                block_info.append(susp_block_dict)

                #For Separating Code Folder in a Report
                self.write_code_to_file(module_code,self.module_name)
            else:
                ss.append(0)
                ss_with_name.append({'name': tp[i]['name'],'value':0})
        return ss, ss_with_name, block_info

    def calculate_and_add_suspiciousness(self,module_name,idx):
        yield "Calculating normalized suspiciousness..."
        # calculate suspiciousness scores
        # susp_scores = utils.calculate_suspiciousness(self.tp_counters, self.tf_counters)

        # print("susp scores: ", susp_scores)
        print('COUNTERS: ',self.counter_list)
        print('COUNTERS PER MODULE: ',self.counter_list_per_module)
        print('Mod')
        self.tp_counters = self.counters_info_per_module[module_name]["tp"]
        self.tf_counters = self.counters_info_per_module[module_name]["tf"]

        susp_scores,susp_scores_with_name, block_info = self.calculate_suspiciousness(module_name)
        if (susp_scores and len(susp_scores)>0):
            max_score = max(susp_scores)
        else:
            max_score = 0
        summary_dict = {"Module_name": self.module_name,
                        "Max_score": max_score,
                        "Block_Info": block_info
                        }
        self.summary_info.append(summary_dict)

        if (self.tp_counters and self.tf_counters):
            # create counters structure for compatibility purposes
            counters = {self.module_name: {}}
            counters[self.module_name]["tp"], counters[self.module_name]["tf"],  = self.counters_info_per_module_with_name[module_name]["tp"], self.counters_info_per_module_with_name[module_name]["tf"]
            counters[self.module_name]["ss"] = susp_scores_with_name

            print('COUNTERS: ',)
            susp_scores_nonzero = [i for i in susp_scores if i != 0]
            if susp_scores_nonzero:
                susp_scores_nonzero_idx = ["c[" + str(sus_obj['name']) + "]"
                                        for sus_obj in susp_scores_with_name if sus_obj['value'] != 0]
                df = pd.DataFrame({"Scores": susp_scores_nonzero},
                                index=susp_scores_nonzero_idx)
                fig, ax = plt.subplots(figsize=(len(df.columns) * 0.6, len(df.index) * 0.6))
                sns.heatmap(df, annot=True, fmt="g", cmap='YlOrRd', ax=ax)
                plt.ylabel('Counter ID')
                plt.yticks(rotation=0)

                #Saving Heatmap
                plt.savefig(self.temp_folder+ self.module_name + "_hm.svg", bbox_inches='tight')
                plt.savefig(self.images_folder+ self.module_name + "_hm.svg", bbox_inches='tight')

            
            for e in self.mgraph.get_edge_list():
                print('Edge: ',e)
        
            '''
            example format
            counters = {"multiply": {
                            "tp": [1,2],
                            "tf": [2,1],
                            "ss": [0.8, 0.4]
                            }
                        }
            '''
            dict2 = {"ss": susp_scores_with_name,
                    "max_score": max_score}
            counters[self.module_name].update(dict2)

            yield "adding execution info on CFG..."
            if(len(self.mgraph.get_edge_list())>0):
                print('COUNTER FOR MODULE: ',self.module_name,counters[self.module_name])

                self.mgraph.add_suspiciousness_information(counters[self.module_name], self.module_name)
                if self.DEBUG: self.mgraph.write2png(self.debug_folder + self.module_name + "_4.png")

                # graph = graph.propagate_edge_color(dot_graph)
                #mgraph.add_counters_everywhere_using_queues(tp_counters, tf_counters, no_tp, no_tf)
                print('TP_COUNTERS: ',self.tp_counters)
                print('TF_COUNTERS: ',self.tf_counters)
                print('no_tp: ',self.no_tp)
                print('no_tf: ',self.no_tf)
                print('Passed and Failed: ', self.no_tp)

                self.mgraph.add_counters_everywhere(counters[self.module_name]["tp"], counters[self.module_name]["tf"], no_passed_increments_per_module, no_failed_increments_per_module)
                self.mgraph.write2png(self.temp_folder + self.module_name + "_cfgCOLOR.png")
                self.mgraph.write2dot(self.temp_folder + self.module_name + "_cfgCOLOR.dot")

        yield "generating final CFG..."
        # generating final CFG
        self.mgraph.write2png(self.temp_folder + self.module_name + "_cfg.png")
        self.mgraph.write2svg(self.images_folder + self.module_name + "_cfg.svg")
        self.mgraph.write2pdf(self.images_folder + self.module_name + "_cfg.pdf")
        self.mgraph.write2pdf(self.temp_folder + self.module_name + "_cfg.pdf")
        
        yield "generating simplified CFG..."
        # generating simplified graph
        self.mgraph.create_simplified_graph()
        self.mgraph.write2png(self.temp_folder+  "simp_" + self.module_name + "_cfg.png")
        self.mgraph.write2svg(self.images_folder+  "simp_" + self.module_name + "_cfg.svg")
        self.mgraph.write2pdf(self.images_folder+  "simp_" + self.module_name + "_cfg.pdf")
        # mgraph.display_graph_info()


        self.mgraph.no_overlap()

        if self.DEBUG: self.mgraph.write2png(self.debug_folder + self.module_name + "_5.png")
        # if DEBUG: dot_graph.write_pdf(debug_folder + module_name + "_5.pdf")
        # if DEBUG: dot_graph.write_svg(debug_folder + module_name + "_5.svg")

        #susp_statements = extract_susp_statements(temp_folder, simplified_instrumented_py_src_fn, tf_counters, susp_scores)

    def calculate_and_add_suspiciousness_in_every_edge(self,module_name,idx):

        yield f"Calculating suspiciousness... for..{module_name}"
        self.tp_counters = self.counters_info_per_module[module_name]["tp"]
        self.tf_counters = self.counters_info_per_module[module_name]["tf"]
        print('Module Namjjjje: ',module_name,'TP: ',self.tp_counters, 'Test Failed COunters: ',self.tf_counters)
        if ( self.tp_counters and self.tf_counters):
            # create counters structure for compatibility purposes
            counters = {self.module_name: {}}
            counters[self.module_name]["tp"], counters[self.module_name]["tf"] = self.counters_info_per_module_with_name[module_name]["tp"], self.counters_info_per_module_with_name[module_name]["tf"]
            yield f"adding execution info on CFG... for..{module_name}"
            no_passed_increments_per_module= max(counters[self.module_name]["tp"], key=lambda x: x['name'])['value']
            no_failed_increments_per_module= max(counters[self.module_name]["tf"], key=lambda x: x['name'])['value']

            print('Module NAMEEESSS: ',self.module_name,'( ',no_passed_increments_per_module,',',no_failed_increments_per_module,')')
            self.module_hits.append({'module_name':self.module_name,'passed_hits':no_passed_increments_per_module,'failed_hits':no_failed_increments_per_module})
            self.mgraph.add_counters_everywhere(counters[self.module_name]["tp"], counters[self.module_name]["tf"], no_passed_increments_per_module, no_failed_increments_per_module,len(self.mgraph.get_edge_list()))
            if(len(self.mgraph.get_edge_list())>0):
                
                self.mgraph.write2png(self.temp_folder + self.module_name + "_cfgCOLOR.png")
                self.mgraph.write2dot(self.temp_folder + self.module_name + "_cfgCOLOR.dot")

                ############## Calculating Suspicious Information to every edge in CFG###################
                print('APPP')
                susp_scores,tf,tp, block_info, ss_with_edge_name = self.calculate_suspiciousness_for_all_edges()
                ############## Adding Suspicious Information to every edge in CFG########################
                counters[self.module_name]["ss"]=ss_with_edge_name
               
                #SUSPICIOUS INFORMATION IS AGAIN ADDED TO COUNTERS and NOT ALL EDGES
                self.mgraph.add_suspiciousness_information(counters[self.module_name], self.module_name)
                # self.mgraph.add_suspicious_scores_everywhere(susp_scores)
                self.mgraph.no_overlap()
                summary_dict={}
                print('Susp. Score: ',susp_scores)
                if (susp_scores and len(susp_scores)>0):
                    max_score = max(susp_scores)
                summary_dict = {"Module_name": self.module_name,
                "Max_score": max_score,
                "Block_Info": block_info
                }
                print('SUMMARY DICT: ',summary_dict)
                self.summary_info.append(summary_dict)
                
                if self.DEBUG: self.mgraph.write2png(self.debug_folder + self.module_name + "_4.png")

                # Creating Heat map for S. Score########################################################
                # Extracting scores and edge names
                data = {'edge_name': [], 'score': []}
                for e in self.mgraph.get_edge_list():
                    if(e.get_label()):
                        print('Edge Label: ',e.get_label())
                        label = e.get_label().split('\n')[-1].strip()
                        if label.startswith('Score') and float(label.split()[-1])!=0:
                            data['edge_name'].append(e.get_name())
                            data['score'].append(float(label.split()[-1]))

                # Creating DataFrame and heatmap
                df = pd.DataFrame(data).set_index('edge_name')
                if not df.empty:
                    fig, ax = plt.subplots(figsize=(len(df.columns) * 0.6, len(df.index) * 0.6))
                    sns.heatmap(df, annot=True, fmt="g", cmap='YlOrRd', ax=ax)
                    # plt.ylabel('Counter ID')
                    plt.yticks(rotation=0)

                    #Saving Heatmap
                    plt.savefig(self.temp_folder+ self.module_name + "_hm.svg", bbox_inches='tight')
                    plt.savefig(self.images_folder+ self.module_name + "_hm.svg", bbox_inches='tight')

                    #Saving Heatmap in PDF
                    plt.savefig(self.temp_folder+ self.module_name + "_hm.pdf", bbox_inches='tight')
                    plt.savefig(self.images_folder+ self.module_name + "_hm.pdf", bbox_inches='tight')
                #########################################################################################

        yield f"generating final annotated CFG...for..{module_name}"
        # generating final CFG
        
        self.mgraph.write2png(self.temp_folder + self.module_name + "_cfg.png")
        self.mgraph.write2svg(self.images_folder + self.module_name + "_cfg.svg")
        self.mgraph.write2pdf(self.temp_folder + self.module_name + "_cfg.pdf")
        
        yield f"generating simplified CFG..for...{module_name}"
        # generating simplified graph
        self.mgraph.create_simplified_graph()
        self.mgraph.write2png(self.temp_folder+  "simp_" + self.module_name + "_cfg.png")
        self.mgraph.write2svg(self.images_folder+  "simp_" + self.module_name + "_cfg.svg")
        self.mgraph.write2pdf(self.images_folder+  "simp_" + self.module_name + "_cfg.pdf")

        if self.DEBUG: self.mgraph.write2png(self.debug_folder + self.module_name + "_5.png")

    
    def append_to_file(self,file_path, content):
        try:
            # Open the file in append mode ('a')
            with open(file_path, 'a') as file:
                # Write the content to the file
                file.write(content + '\n')  # Adding a newline after each append
            print("Content successfully appended to the file.")
        except Exception as e:
            print(f"An error occurred: {e}")

    
    def calculate_suspiciousness_for_all_edges(self):
        print("******* Calculating loop handling normalized suspiciousness ******")


        graph=self.mgraph
        edges=graph.get_edge_list()
        ss_with_edge_name=[]

        tp=[]
        tf=[]
        for e in edges:
            passed_test=str(re.sub(r'<[^>]*>', '', e.get('xlabel')))[:-1].split(',')[0]
            failed_test=str(re.sub(r'<[^>]*>', '', e.get('xlabel')))[:-1].split(',')[1]
            tp.append(int(passed_test))
            tf.append(int(failed_test))
    
        if self.no_tp == self.no_tf:
            number_of_tests = self.no_tf
        else:
            number_of_tests = min(self.no_tf, self.no_tp)
        ss=[]
        block_info=[]
        line_number=2
        c=0
        for i,e in enumerate(edges):
            pattern = r'c\[\d+\]'
            if e.get('label') and re.search(pattern, e.get('label')):
                print('HELLOss COUNTER:: ',e.get('label'))


                         
            if(tf[i] ==0 and tp[i] ==0 ):
                ss.append(0)
                ss_with_edge_name.append({'edge_name': str(e.name),'value':0})
            else:
                if e.get_source():
                    source_node=self.mgraph.find_node_by_name(e.get_source())
                    dest_node=self.mgraph.find_node_by_name(e.get_destination())
                    source_node_passed_test=int(str(re.sub(r'<[^>]*>', '', source_node.get('xlabel')))[:-1].split(',')[0])
                    source_node_failed_test=int(str(re.sub(r'<[^>]*>', '', source_node.get('xlabel')))[:-1].split(',')[1])
                    ef  =  tf[i]
                    ep  =  tp[i]
                   
                    ef=self.normalize_value(ef, 0, source_node_failed_test, 0, number_of_tests)
                    ep=self.normalize_value(ep, 0, source_node_passed_test, 0, number_of_tests)
                   
                    nf  =  number_of_tests-ef
                    np  =  number_of_tests-ep
          
                    pattern = r'c\[\d+\]'
                    if e.get('label') and re.search(pattern, e.get('label')):
                        print('counter name: ',e.get('label'),'no. of tests: ',number_of_tests,'ep: ',ep,' - ef: ',ef,'- np: ',np,'nf: ',nf,'\n')
                        
                        if (ep==0 and np ==0):
                            ss.append(1)
                            avg_score=1

                        elif (ef==0 and nf==0):
                            ss.append(0)
                            avg_score=0
                        elif (ep>=ef):
                            ss.append(0)
                            avg_score=0
                        else:
                            
                            oc_score = round(ef / (math.sqrt((ef + nf) * (ef + ep))), 2)
                            print('oc_score: ',oc_score,'\n')
                            tr_score = round((ef / (ef + nf)) / ((ef / (ef + nf)) + (ep / (ep + np))), 2)
                            print('tr_score: ',tr_score,'\n')
                            jc_score = round((ef / (ef + nf + ep)), 2)
                            print('jc_score: ',jc_score,'\n')


                            if(self.suspicious_score_metric=='savg'):
                                avg_score = round((oc_score + tr_score + jc_score) / 3, 2)
                            elif(self.suspicious_score_metric=='Ochiai'):
                                avg_score=oc_score
                            elif(self.suspicious_score_metric=='Tarantula'):
                                avg_score=tr_score
                            elif(self.suspicious_score_metric=='Jaccard'):
                                avg_score=jc_score
                            elif(self.suspicious_score_metric=='Goodman'):
                                ds_score = round(((ef*2-nf-ep) / (2*ef + nf + ep)), 2)
                                print('ds_score: ',ef,ep,ds_score,'\n')
                                avg_score=ds_score
                                   
                            else:
                                avg_score = round((oc_score + tr_score + jc_score) / 3, 2)
                            print('avg_score: ',avg_score,'\n')
                            print('---------------','\n')
                            ss.append(avg_score)
                        
                        ss_with_edge_name.append({'edge_name': str(e.name),'value':avg_score})
                        #module_code=utils.remove_c_increments(self.get_simplified_module_code(self.temp_folder,self.instrumented_py_src_fn))
                        source_block_code=source_node.get_label()[4:-2]+source_node.get_label()[-2].strip().strip('')
                        dest_block_code=dest_node.get_label()[4:-2]+dest_node.get_label()[-2].strip().strip('')
                        source_block_id=int(e.get_source())
                        dest_block_id=int(e.get_destination())

                        print('Suspicious Score: ',avg_score)

                        module_code=self.get_simplified_module_code(self.temp_folder,self.instrumented_py_src_fn)
                        statementsinfo, susp_variables = self.get_block_level_susp_statements(module_code, c + 1)
                        susp_source_block_dict = {
                            "Block ID": source_block_id,
                            "Susp. score": avg_score,
                            "Statements_info": [{"statement": i} for i in source_block_code.split('\n')] ,
                        }
                        block_info.append(susp_source_block_dict)
                        susp_dest_block_dict = {
                            "Block ID": dest_block_id,
                            "Susp. score": avg_score,
                            "Statements_info":[{"statement": i} for i in dest_block_code.split('\n')] ,
                        }
                        block_info.append(susp_dest_block_dict)
                        self.write_code_to_file(module_code,self.module_name)
                        c+=1
        return ss,tf,tp,block_info,ss_with_edge_name
    
    def create_heatmap(self):
        yield "Creating heatmap"
        #calculate_heatmap()

    def pre_localizer(self):
        dest=self.temp_folder +'/'+ self.file_n
        src=self.project_path +'/'+ self.file_n
        utils.copy_file(src,dest)
        is_class=utils.is_class_based(dest)
        print('Class Based_ ',is_class)
        if(is_class):
             utils.convert_to_function_based(dest)

    def localize_python(self):
        functions = [
            self.instrument_python,
            self.execute_tests,
            self.extract_module_names,
            ]
        for fun in functions:
            for msg in fun():
                yield msg
                print(msg)
                if "ERROR" in msg:
                    print("ERROR")
                    break
                else:
                    continue

                
    def normalize_with_tests(self,val,total):
        if(val>total):
            return total
        else:
            return val
        
    def normalize_value(self,value, old_min, old_max, new_min, new_max):
        # Normalize the value to the range [0, 1]
        if (value==0):
            return 0
        print('NORMALIZED: ',value, old_min, old_max, new_min, new_max)
        normalized_value = (value - old_min) / (old_max - old_min)
        
        # Scale to the new range [new_min, new_max]
        scaled_value = normalized_value * (new_max - new_min) + new_min
        
        return scaled_value

    def creating_cfgs_and_calculating_suspiciousness(self):
        i=0
        for file in self.splitted_instrumented_src:
            self.make_this_current_file(file)
            print('Creating cfg for : ',file)
            yield f'Creating cfg for : {file}'
            self.create_cfg()
            for msg in self.calculate_and_add_suspiciousness_in_every_edge(self.module_name,i): 
                yield msg
                print(msg)
            i+=1

    def save_max_scores_per_module(self):
        output_path = os.path.join(self.temp_folder, self.outputFile)
        print('TEMP. ',output_path)
        with open(output_path, 'r') as outjsfile:
            data = json.load(outjsfile)
        # Initialize dictionary to store max scores for each module
        max_scores = {}
        # Iterate through each module's data
        
        for module_data in data:
            module_name = module_data["Module_name"]
            max_score = module_data["Max_score"]
            # If the module name is not already in the dictionary or if the max score is greater than the existing one
            if module_name not in self.scores or max_score > max_scores[module_name]:
                self.scores[module_name] = max_score
        print('SELF SCORE: ',self.scores)
        
        return self.scores

    def create_fault_summary(self):
        json_object = json.dumps(self.summary_info, indent=2)
        
        # Check if the folder exists, if not, create it
        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)
        
        # Join the folder and filename
        output_path = os.path.join(self.temp_folder, self.outputFile)
        
        # Write to the file
        with open(output_path, "w") as outjsfile:
            outjsfile.write(json_object)

        self.save_max_scores_per_module()
        yield "generating fault summary"

    def get_susp_variables(self, susp_statement):
        susp_vars = []
        kw_list = ["IF", "(*", "*)", "ELSE", "ELSIF", "THEN", ">", ":=", ">=", "<", "<=", "AND", "OR", "TRUE",
                   "FALSE", "+", "-", "/", "*", "=", "NOT", "return", "else:", "RETURN"]
        patterns = [r"[(]", r"[)]", r"[;]"]
        pattern = "|".join(patterns)
        statement = re.sub(r'^[\n\t]+', '', susp_statement)
        if re.search(r"^[;(*]|^[(*]", statement) is None:
            statement_split_list = susp_statement.split(' ')
            for item in statement_split_list:
                if item != '':
                    if any(kw in item for kw in kw_list):
                        pass
                    else:
                        if re.search(r'^-?[0-9]', item) is None:
                            if re.findall(pattern, item):
                                if re.sub(pattern, "", item) != '':
                                    susp_vars.append(re.sub(pattern, "", item))
                            else:
                                susp_vars.append(item)
            return susp_vars

    def get_simplified_module_code(self,path,src_filename):
        code = ""
        with open(path + src_filename) as src:
            code = src.read()
        return code

    def write_code_to_file(self,code,module_name):
        copy_dst_file=self.code_folder + module_name + '.py'
        with open(copy_dst_file, 'w') as dst:
            dst.write(code)

    def generating_reports(self):
        yield 'Generating Reports...'
        utils.generate_html_report(self.report_folder,self.temp_folder, self.outputFile, self.test_file, self.src_file_name)
        utils.generate_simp_html_report(self.report_folder,self.temp_folder, self.outputFile,self.test_file,self.src_file_name)
        yield 'Reports Generated Done.. '

    def generate_call_graph(self):
        yield 'Creating Call Graph...'
        print('CG CREATION HERE: ')
        self.call_graph_processor.generate_simple_call_graph()
        
        yield 'Created Simple Call Graph...'

    def annotate_call_graph(self):
        yield 'Annotating Call Graph...'
        self.call_graph_processor.generate_annotated_call_graph(self.scores,self.module_hits)
        shutil.copyfile(self.temp_folder+'CG.svg', self.images_folder+'CG.svg')
        shutil.copyfile(self.temp_folder+'CG.png', self.images_folder+'CG.png')
        shutil.copyfile(self.temp_folder+'CG_simp.svg', self.images_folder+'CG_simp.svg')
        shutil.copyfile(self.temp_folder+'CG_simp.png', self.images_folder+'CG_simp.png')
        yield 'Annotated Call Graph...'

    def save_max_scores_per_module(self):
        output_path = os.path.join(self.temp_folder, self.outputFile)
        print('TEMP. ',output_path)
        with open(output_path, 'r') as outjsfile:
            data = json.load(outjsfile)
        # Initialize dictionary to store max scores for each module
        max_scores = {}
        # Iterate through each module's data
        
        for module_data in data:
            module_name = module_data["Module_name"]
            max_score = module_data["Max_score"]
            # If the module name is not already in the dictionary or if the max score is greater than the existing one
            if module_name not in self.scores or max_score > self.scores[module_name]:
                self.scores[module_name] = max_score
        print('SELF SCORE: ',self.scores)
        
        return self.scores

    def extract_module_names(self):
        with open(os.path.join(self.temp_folder, self.instrumented_py_src_fn), 'r') as src:
            method_content = ""  # To store the content of each method
            method_name = None  # To store the name of the current method
            file_names=[]
            for line in src.readlines():
                if line.startswith("def "):
                    # Append line to method_content
                    # If method_content has content, write it to a file
                    if method_content:
                        self.write_method_to_file(method_name, method_content)
                        method_content = ""  # Reset method_content
                    method_name = line.split("def ")[1].split("(")[0].strip()+'_split.py'  # Extract method name
                    self.splitted_instrumented_src.append(method_name)
                    file_names.append(method_name)         
                if(not line.strip().startswith("import ") and not line.strip().startswith("from ") and line.strip() != ""):
                    method_content += line
            if method_content:
                self.write_method_to_file(method_name, method_content)
            print("multiple module files creation done")
            yield 'Module Extraction Done'
            return file_names

    def write_method_to_file(self, method_file_name, content):
        file_name = method_file_name  # Filename will be the method name with .py extension
        print('FILE NAME: ',file_name)
        with open(os.path.join(self.temp_folder, file_name), 'w') as method_file:
            method_file.write(content)
        print(f"Method '{method_file_name}' saved to '{file_name}'")

    def make_this_current_file(self,filename):
        self.file_n=filename
        self.instrumented_py_src_fn=filename
        self.simplified_instrumented_py_src_fn=utils.simplify_instrumented(path=self.temp_folder, src_filename=filename)
        self.module_name=filename.split('_split')[0].split('.')[0]
        print('Module Name: ',self.module_name)
        self.function=self.module_name

def run_localizer(loc):
    try:
        message = ''
        for msg in loc.generate_call_graph():
            message += msg + '\n'

        loc.pre_localizer() #Check if a class based or structured based. Converts to Structured based in case of class based.
        for msg in loc.localize_python(): 
            
            message += msg + '\n'

        for msg in loc.creating_cfgs_and_calculating_suspiciousness():
            
            #   Main Inputs: Tests (Passed and Failed), Source Code
            #   Create Call Graph
            #   Do three things, Code instrumentation() which add thes counters after function definition, and branchind conditions. After that we execute tests by trimming the passed and failed tests to minimum of both and gather execution traces using spectrum analysis.
            #   If there are multiple functions we separate the functions into separate files i.e. split function()
            #   We create the CFG of each function and annotate the execution count gathered on each node and edges. Node represents block statements and edge is there for branching conditions if,else, loops. Also create simplified CFG where only passed and failed executed edges and are shown not others.
            #   Based on that We calculate the suspicious score and I have described above. (Explain this detaily)
            #   After that, Annotate the CFG with suspicious score where failed execution count more than passed ones.
            #   Annotate call graph with max score like annotate Call Graph with max scores on each node.
            #   Generate Suspicious Statement Table to trace the Block level suspicious score.
            #   Generate Fault Report
            #   Generate Simplified to show simplified cfgs.


            message += msg + '\n'

        f = [loc.create_fault_summary, loc.annotate_call_graph, loc.generating_reports]
        for fun in f:
            for msg in fun():
                message += msg + '\n'

        return True

    except Exception as e:
        print("Error: ", e)
        return False