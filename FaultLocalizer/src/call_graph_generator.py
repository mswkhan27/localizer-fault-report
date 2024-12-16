import json
import networkx as nx
import pydot
from pycg import formats
from pycg.pycg import CallGraphGenerator
from pycg.utils.constants import CALL_GRAPH_OP
import os

class CallGraphProcessor:

    def __init__(self, entry_point=None, package=None, fasten=False, product="", forge="", version="", timestamp=0, max_iter=-1, operation=CALL_GRAPH_OP, as_graph_output="your_as_graph_output.json", output="output.json", output_image_path='', scores={}):
        self.entry_point = entry_point
        self.package = package
        self.fasten = fasten
        self.product = product
        self.forge = forge
        self.version = version
        self.timestamp = timestamp
        self.max_iter = max_iter
        self.operation = operation
        self.as_graph_output = as_graph_output
        self.output = output
        self.output_image_path = output_image_path
        self.scores = scores
        self.pydot = pydot
        self.json_data=''
        self.filtered_data = {}
        self.output_file_path= 'output_file_path.json'


    def generate_simple_call_graph(self):
        try:
            print('ENTRY POINT AND PACKAGE: ',self.entry_point, self.package)
            cg = CallGraphGenerator(self.entry_point, self.package, self.max_iter, self.operation)
            cg.analyze()

            print('GRAPH: ',self.as_graph_output )

            if self.operation == CALL_GRAPH_OP:
                if self.fasten:
                    formatter = formats.Fasten(
                        cg, package, product, forge, version, timestamp
                    )
                else:
                    formatter = formats.Simple(cg)
                output_data = formatter.generate()
            else:
                output_data = cg.output_key_errs()

            as_formatter = formats.AsGraph(cg)

 

            if self.output:
                with open(self.output, "w+") as f:
                    f.write(json.dumps(output_data))
            else:
                print(json.dumps(output_data))

            if self.as_graph_output :
                with open(self.as_graph_output , "w+") as f:
                    f.write(json.dumps(as_formatter.generate()))
            self.generate_call_graph_from_json()

        except Exception as e:
            print('Error:', e)

    def filter_builtin_functions(self):
        self.filtered_data = {}
        print('DATA ITEMS: ',self.json_data.items())
        for key, value in self.json_data.items():
            if not key.startswith("<builtin"):
                filtered_value = [item for item in value if not item.startswith("<builtin")]
                self.filtered_data[key] = filtered_value

    def read_json_from_file(self):
        with open(self.output, 'r') as file:
            print('OUTPUT: ',self.output)
            self.json_data = json.load(file)
            print('HEYsss')
            return self.json_data 

    def write_json_to_file(self):
        self.output_file_path=self.output
        print('OUTPUT FILE PATH: ',self.output_file_path)
        with open(self.output_file_path, 'w') as file:
            json.dump(self.filtered_data, file, indent=2)

    def build_call_graph(self, data):
        G = nx.MultiDiGraph()
        for caller, callees in data.items():
            for callee in callees:
                G.add_edge(caller, callee)
        return G

    def generate_call_graph_from_json(self):
        try:
            self.read_json_from_file()
            self.filter_builtin_functions()
            self.write_json_to_file()
            print("Filtered JSON data updated saved to:", self.output_file_path)

        except Exception as e:
            print('There is some error in call graph generation:', e)

    def generate_annotated_call_graph(self,scores,module_hits):
        try:
            self.scores=scores
            filtered_data = self.read_json_from_file()
            call_graph = self.build_call_graph(filtered_data)
            print('Filtered_ Data: ',filtered_data, call_graph)
            pydot_graph = nx.drawing.nx_pydot.to_pydot(call_graph)
            for node in pydot_graph.get_nodes():
                node.set_shape('oval')
                node.set_penwidth(2)
            for edge in pydot_graph.get_edges():
                edge.set_style('solid')
                edge.set_color('black')
            max_score = float('-inf')
            max_node = []
            max_nodes=[]
            print('Nodessss: ',pydot_graph.get_nodes())
            print('MODULE HITS: ',module_hits)
            for node in pydot_graph.get_nodes():
                node_n = node.get_name().strip('"')
                node_name = node_n.split('.')[-1]
                print('node_name: ',node_name)
                translation_table = str.maketrans('', '', "!@#$%^&*()+=-[]{};:'\"\\|,<>?/~`")
                node_name = node_name.translate(translation_table)
                print('NEW NODE: ',node_name)
                if node_name in self.scores:
                    print('IN CG ANNOTATION SCORES: ',self.scores)
                    score = float(self.scores[node_name])
                    print('SCOREEEE: ',score)
                    if(score>0):
                        node.set_label(f"{node_n}\nMax Score: {score}")
                    if score > max_score:
                        max_score = score
                        max_nodes = [node]  # Reset max_nodes list with the new max node
                    elif score == max_score:
                        max_nodes.append(node)  # Add the node to max_nodes list if it matches max_score
                
                for module in module_hits:
                    if node_name == module['module_name']:
                        print('YESS: ')
                        node.set("xlabel",
                        "<<br></br><br></br><br></br><font color='darkorange'>{},{}</font>>".format(int(module['passed_hits']),int(module['failed_hits'])))



            if max_nodes and len(max_nodes)>0:
                for max_node in max_nodes:
                    max_node.set_color('red')  # Setting border color for the max score nodes to red

            
            
            ### Adding links to CG######################################
            for node in pydot_graph.get_nodes():
                node_n = node.get_name().strip('"')
                print('CG Node NAME: ',node_n)
                node_name = node_n.split('.')[-1]
                print('CG Node NAjjjME: ',node_name)
                node.set_URL(f'fault_report.html#{node_name}')
            ############################################################
            pydot_graph.write_svg(self.output_image_path + '.svg')
            pydot_graph.write_png(self.output_image_path + '.png')
            pydot_graph.write_pdf(self.output_image_path + '.pdf')
            # #### Adding links to Simple Report CG ######################################
            for node in pydot_graph.get_nodes():
                node_n = node.get_name().strip('"')
                print('CG Node NAME: ',node_n)
                node_name = node_n.split('.')[-1]
                print('CG Node NAjjjME: ',node_n)
                node.set_URL(f'simp_fault_report.html#{node_name}')
            # #############################################################
            print('SIMPLE CG: ',self.output_image_path + '_simp.svg')
            pydot_graph.write_svg(self.output_image_path + '_simp.svg')
            pydot_graph.write_png(self.output_image_path + '_simp.png')

        except Exception as e:
            print('There is some error in call graph generation:', e)
