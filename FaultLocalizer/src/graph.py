# __graph processing stuff
import sys

import pydot
import re
import os
from staticfg import CFGBuilder


def build_cfg(path, file, calls=True, show=False, formats=['dot']):
    '''
    create __graph and  generates the files. it returns the __graph
    :param path:
    :param file:
    :param calls:
    :param show:
    :param formats:
    :param simplify:
    :return:
    '''
    print("************ Creating CFG for ", file)
    filename = os.path.splitext(file)[0]
    #print("file path ", path)
    #print("file name ", filename)
    cfg = CFGBuilder().build_from_file(filename.split('_split')[0].removeprefix("s_"), path + file)

    for f in formats:
        output_file = path + filename
        cfg.build_visual(output_file, f, calls=calls, show=show)

    print('...done')
    return cfg

class MGraph:
    def __init__(self, pydot_graph):
        self.__graph = pydot_graph


        self.__remove_isolated_node()
        self.__node_list = pydot_graph.get_node_list()
        self.__edge_list = pydot_graph.get_edge_list()
        self.__set_top_node()
        self.__top_node_name = self.top_node.get_name()
        self.__tpc = []
        self.__tfc = []
        self.__no_passed = -1
        self.__no_failed = -1


        self.__extend_Node()
        self.__extend_Edge()
        self.__set_edge_labels_bgcolor()
    
    def no_overlap(self):
            self.__graph.set_overlap('false')
            self.__graph.set_splines('true')
            for edge in self.__graph.get_edges():
                edge.set_labeldistance(15)  # Increase distance of the label from the edge
                edge.set_fontsize(8)  # Adjust font size for better readability
                edge.set_label
                print('EDGE: ',edge)
            for node in self.__graph.get_nodes():
                node.set_fontsize(10)  # Adjust font size for better readability
                print('EDGE: ',edge)


    def __remove_isolated_node(self):
        for node in self.__graph.get_node_list():
            #print("NODE: ", node.get_name())
            if node.get_name() == '\"\\n\"':
                print("***** removing isolated node")
                self.__graph.del_node(node.get_name())

    def __set_edge_labels_bgcolor(self):
        for edge in self.__edge_list:
            edge.set('label_bgcolor', 'white')
    def write2png(self, str):
        self.__graph.write_png(str)
    def write2dot(self, str):
        self.__graph.write_dot(str)
    def write2svg(self, str):
        self.__graph.write_svg(str)
    def write2pdf(self, str):
        self.__graph.write_pdf(str)

    def __set_top_node(self):
        print(" *********** set_top_node ")
        # print("searching for top_node: ", "in ", sgraph.get_name())

        # find node with no incoming transitions
        node_list = set([n.get_name() for n in self.__graph.get_nodes() if n.get_name().isnumeric()])
        dest_list = set([e.get_destination() for e in self.__graph.get_edges()])
        # print("nodes:", __node_list)
        # print("destination nodes: ", dest_list)
        diff = node_list - dest_list
        # print("diff:",  diff)
        # print("difference: ", diff)
        if len(diff) != 1:
            assert "unique top node not found"
            self.top_node = None
        else:
            tn = self.__get_node_by_name(diff.pop())
            # print("top node found: ", tn.get_name())
            self.top_node = tn

    def __calculate_completeness(self):
        # calculates percentage of solved edges and nodes
        n_idx = 0
        for node in self.__node_list:
            if node.is_solved():
                n_idx = n_idx + 1
        e_idx = 0
        for edge in self.__edge_list:
            if edge.is_solved():
                e_idx = e_idx + 1

        print('NODE LIST: ',self.__node_list,'EDGE LIST: ',self.__edge_list)

        print("Completeness : \t node: {:.2f}  \t edge: {:.2f}".format(n_idx / len(self.__node_list), e_idx / len(self.__edge_list)))
        return n_idx / len(self.__node_list), e_idx / len(self.__edge_list)

    def __collect_node_info(self):
        print(" *************** collect_node_info ")
        # collecting known info for nodes
        for node in self.__node_list:
            node.name = node.get_name()
            node.label = node.get_label()
            node.i_edges = self.__get_i_edges(node.name, self.__edge_list)
            node.o_edges = self.__get_o_edges(node.name, self.__edge_list)
            node.set_tests(-1, -1)
            #print(node.name, " ", node.i_edges)

    def __collect_edge_info(self):
        print(" *************** collect_edge_info ")
        # collecting known values for edges from counters
        edge_idx = 0
        for edge in self.__edge_list:
            edge.id = edge_idx
            edge_idx = edge_idx + 1
            edge.label = edge.get_label()
            #print("edge label: ", edge.get_label())

            edge.set_name(edge.get_source(), edge.get_destination())

            # collecting known counters
            if edge.label and "c[" in edge.label:
                #print("Counter found for", edge.name)
                # extract test coverage from Counters
                c_idx = self.__get_idx(edge.label)
                #print("Counter: ", c_idx, " values", self.__tpc[c_idx - 1], self.__tfc[c_idx - 1])
                edge.set_tests(self.get_test_val(self.__tpc,c_idx), self.get_test_val(self.__tfc,c_idx))
            else:
                edge.set_tests(-1, -1)

    def display_graph_info(self):
        print("__graph: ", self.__graph.get_name())
        print(self.__graph.get_subgraphs())
        print(self.__graph.get_attributes())
        print(self.__graph.get_name())
        print(self.__graph.get_subgraph_list())
        #print(self.__graph.get_node_list())
        #print(self.__graph.get_edge_list())
        print(" NODES: ", [n.get_label() for n in self.__node_list])
        print(" EDGES: ", [e.get_label() for e in self.__edge_list])


    def __get_node_by_name_list(self, name):
        for node in self.__node_list:
            # print("inspecting node:_", node.get_name(), "_")
            # apparently node names have spaces around
            if node.get_name() and node.get_name() == name:
                # print("node found: ", node.get_name(), node.get_label())
                return node
        # print("node NOT found: ")
        return None

    def __solve_remaining_edges(self):
        print(" *************** solve_remaining_edges ")
        for e in self.__edge_list:
            #print(e.name)

            if not e.is_solved():
                #print("CALCULATION needed: ", e.name)

                if e.get_source():
                    snode = [x for x in self.__node_list if x.name == e.get_source()][0]
                    #print("snode: ", snode.name, snode.passed_tests, snode.failed_tests)
                    # if source source node is solved
                    if snode.is_solved():
                        out_deg = len(snode.o_edges)
                        # calculate if n-1 out edges have values
                        n = 0
                        sum_p = 0  # of known values
                        sum_f = 0  # of known values
                        for e1 in snode.o_edges:
                            if e1.is_solved():
                                n = n + 1
                                sum_p = sum_p + e1.passed_tests
                                sum_f = sum_f + e1.failed_tests
                        #print("n2: ", n, sum_p, sum_f, snode.passed_tests, snode.failed_tests)
                        if (out_deg - n) == 1:  # we can calculate
                            e.set_tests(snode.passed_tests - sum_p, snode.failed_tests - sum_f)

    def __update_edge_color(self):
        print("Updating edge color: ")
        # eventually this should be moved to another function
        for edge in self.__edge_list:
            #print(edge.get_name())
            tp = edge.passed_tests
            tf = edge.failed_tests

            if tp > 0 and tf > 0:
                edge.set_color("blue")
            if tp > 0 and tf == 0:
                edge.set_color("#429E6A")
            if tp == 0 and tf > 0:
                edge.set_color("red")

    # def add_counters_everywhere_using_queues(self, tpc, tfc, ntp, ntf):
    #     """
    #     calculates visiting information on edges without counters
    #     adds corresponding color to edges
    #     :param pydot_graph:
    #     :param tpc: counter values for passed
    #     :param __tpc: counter values for failed
    #     :param __no_passed number of passed tests used
    #     :param __no_failed number of failed tests used
    #     :return:
    #     """
    #     import queue
    #     unsolved_nodes = queue.Queue()
    #     last_unsolved_node = None

    #     self.__tpc = tpc
    #     self.__tfc = tfc
    #     self.__no_passed = ntp
    #     self.__no_failed = ntf

    #     print("\n ********************* add colors everywhere - queue")
    #     print("TPC: ", tpc)
    #     print("TFC: ", tfc)

    #     self.__collect_edge_info()
    #     self.__collect_node_info()

    #     for node in self.__node_list:
    #         # skipping unconnected nodes
    #         if node.name not in ['graph', 'node', '\n']:
    #             if node.name == self.__top_node_name:
    #                 node.set_tests(self.__no_passed, self.__no_failed)
    #             unsolved_nodes.put(node)

    #     special_mode = 0 # if ww get stuck and need to advance the queue
    #     while not unsolved_nodes.empty():
    #         #print("QUEUE: ", [n.name for n in unsolved_nodes.queue])
    #         u_node = unsolved_nodes.get()
    #         is_node_solved = False
    #         #print(f"Current node: {u_node.name}")

    #         # processing input edges to set the node value
    #         if u_node.passed_tests == -1 or u_node.failed_tests == -1:
    #             unsolved_i_edges = False
    #             i_edge_sum = [0, 0]
    #             for ie in u_node.i_edges:
    #                 if ie.passed_tests == -1:
    #                     # We cannot calculate the node value because
    #                     # an unsolved incoming edge detected; therefore aborting
    #                     #print("- unsolved input edge ", ie)
    #                     unsolved_i_edges = True
    #                     break
    #                 else:
    #                     i_edge_sum[0] += ie.passed_tests
    #                     i_edge_sum[1] += ie.failed_tests

    #             # If no unsolved incoming edge is found,
    #             # then calculate the node value and mark it solved
    #             if not unsolved_i_edges:
    #                 print(f"{u_node.name}, incoming {i_edge_sum}")
    #                 u_node.set_tests(*i_edge_sum)
    #                 is_node_solved = True
    #         else:
    #             is_node_solved = True

    #         # If the node is solved then put it back at the end of the unsolved queue
    #         # and move on to the next node in the queue
    #         if not is_node_solved:
    #             # To check if we arrive to same unsolved node which we postponed last time

    #             if last_unsolved_node and last_unsolved_node.name == u_node.name:
    #                 print(f"We could not solve nodes: {u_node.name} and {[n.name for n in unsolved_nodes.queue]}")
    #                 special_mode += 1
    #                 if special_mode > 5: return

    #             if not last_unsolved_node:
    #                 last_unsolved_node = u_node

    #             unsolved_nodes.put(u_node)
    #             continue

    #         # processing outgoing edges of the solved node
    #         unsolved_o_edge = None
    #         o_edge_sum = [0, 0]
    #         too_many_unsolved_edges = False

    #         for oe in u_node.o_edges:
    #             if oe.passed_tests == -1:
    #                 if unsolved_o_edge is None:
    #                     unsolved_o_edge = oe
    #                 else:
    #                     # If we found more than one unsolved outgoing edge
    #                     # then we cannot solve them, and we skip the node for now
    #                     too_many_unsolved_edges = True
    #                     break
    #             else:
    #                 o_edge_sum[0] += oe.passed_tests
    #                 o_edge_sum[1] += oe.failed_tests

    #         # solve the one outgoing edge
    #         if unsolved_o_edge and not too_many_unsolved_edges:
    #             unsolved_o_edge.set_tests(u_node.passed_tests - o_edge_sum[0], u_node.failed_tests - o_edge_sum[1])

    #     self.__update_edge_color()

    def add_counters_everywhere(self, tpc, tfc, ntp, ntf,edges_length):
        """
        calculates visiting information on edges without counters
        adds corresponding color to edges
        :param pydot_graph:
        :param tpc: counter values for passed
        :param __tpc: counter values for failed
        :param __no_passed number of passed tests used
        :param __no_failed number of failed tests used
        :return:
        """

        self.__tpc = tpc
        self.__tfc = tfc
        self.__no_passed = ntp
        self.__no_failed = ntf

        print("\n ********************* add colors everywhere")
        print("TPC: ", tpc)
        print("TFC: ", tfc)

        self.__collect_edge_info()
        self.__collect_node_info()

        completeness_initial = 0
        completeness_final = 1
        iter_no = 1

        if(edges_length==0):
            for node in self.__node_list:
                    print('HI____ node: ',node)
                    node.set_tests(ntp,ntf)
        else:
            while (completeness_initial < completeness_final):
                print (" ### LOOP {} ###".format(iter_no))
                iter_no += 1
                # we apply the following as long as completeness keeps increasing

                # Collect tests from counters when only one input or one output edge with counter on it
                
                self.__solve_one_input_node()
                self.__solve_one_output_node()
                self.__solve_multiple_inputs_node()
                self.__solve_multiple_outputs_node()
                self.__solve_remaining_edges()

                cn, ce = self.__calculate_completeness()
                completeness_initial = completeness_final
                completeness_final = cn + ce
                print("completeness: {:.2f}->{:.2f}".format(completeness_initial, completeness_final))

            # __node_list = solve_higher_level_inputs(__node_list) # extra checks are needed here

        self.__update_edge_color()

    def __solve_one_input_node(self):
        # solving level 1
        print("******* solving level 1 inputs")
        for node in self.__node_list:

            #print("Current node: ", node.name)
            # skipping unconnected nodes
            if node.name in ['__graph', 'node', '\n']:
                continue

            if node.name == self.__top_node_name:
                #print("working with top node")
                node.set_tests(self.__no_passed, self.__no_failed)

            # processing input edges
            #print("input edges:", len(node.i_edges))
            if len(node.i_edges) == 1:
                the_i_edge = node.i_edges[0]

                if the_i_edge.is_solved():
                    # propagate tests down to node
                    node.set_tests(the_i_edge.passed_tests, the_i_edge.failed_tests)
                if node.is_solved():
                    # propagate tests to input edge
                    the_i_edge.set_tests(node.passed_tests, node.failed_tests)

    def __solve_one_output_node(self):
        print(" ******* solving level 1 outputs")
        for node in self.__node_list:
            node_name = node.get_name()
            node_label = node.get_label()

            # skipping unconnected nodes
            if node_name in ['__graph', 'node', '\n']:
                continue

            # processing output edges
            #print("Output edges:", node.o_edges)

            if len(node.o_edges) == 1:
                o_edge = node.o_edges[0]

                #print("o_edge is solved ", o_edge.is_solved()  )

                if node.is_solved() and not o_edge.is_solved():
                    #node is solved and  output edge is not, proagate node tests down
                    #print("node solved, o_edge not solved ", node.passed_tests, node.failed_tests)
                    o_edge.set_tests(node.passed_tests, node.failed_tests)
                if not node.is_solved() and o_edge.is_solved():
                    # node is not solved and output edge solved, propagate note tests up
                    node.set_tests(o_edge.passed_tests, o_edge.failed_tests)
                    print("Solving node {} with output edge {} {}".format(node_name, o_edge.passed_tests, o_edge.failed_tests))

    def __solve_node_with_one_input_one_output(self):
        # if for a node with one input and one output we know one of them
        print(" ******* solving node with one input and one output we know one of them")

        for node in self.__node_list:
            if not node.is_solved ():
                node_name = node.get_name()
                node_label = node.get_label()
                # print("Current node: ", node_name, node.passed_tests, node.failed_tests)

                # skipping unconnected nodes
                if node_name in ['__graph', 'node', '\n']:
                    continue

                # processing output edges
                # print("Output edges:", node.o_edges)

                #if len(node.o_edges) == 1 and len(node.o_edges) == 1 and (node.o_edges[0].is_solved() or node.i_edges[0].is_solved()):

    def __solve_multiple_inputs_node(self):
        print(" ******* solving input level >1 ")
        for node in self.__node_list:
            node_name = node.get_name()
            node_label = node.get_label()
            #print("Current node: ", node_name)

            # skipping unconnected nodes
            if node_name in ['__graph', 'node', '\n']:
                #print("Ignoring node: ", node_name)
                continue

            if node.is_solved():
                # skip solved nodes
                #print("Skipping node: ", node_name)
                continue

            # processing input edges
            i_edges = len(node.i_edges)
            #print("input edges: ", i_edges)

            if i_edges > 1:
                print("Calculate sum for node: ", node_name)
                # try to sum up the values from incoming edges
                # and sum them up if all known
                sum_p = 0
                sum_f = 0
                no_solved_edges = 0
                for ie in node.i_edges:
                    #print("  input edge", ie.get_name(), ie.passed_tests, ie.failed_tests)
                    if ie.is_solved():
                        sum_p = sum_p + ie.passed_tests
                        sum_f = sum_f + ie.failed_tests
                        no_solved_edges = no_solved_edges + 1
                print( "solved edges: ", no_solved_edges)
                if no_solved_edges == i_edges:
                    node.set_tests(sum_p, sum_f)
                    #print("Sums: ", sum_p, sum_f)
    '''
    if node_name == "4":
        print("Current node: ",
              '=' + node_name + '=',
              node_label,
              node.passed_tests,
              node.failed_tests, "XXX: ",
              [e.get_name() for e in node.o_edges],
              node.is_solved())
    '''
    def __solve_multiple_outputs_node(self):
        print(" ******* solving output level >1 ")
        for node in self.__node_list:
            node_name = node.get_name()
            node_label = node.get_label()
            #print("Current node: ", node_name)

            # skipping unconnected nodes
            if node_name in ['__graph', 'node', '\n']:
                #print("Ignoring node: ", node_name)
                continue

            if node.is_solved():
                # skip solved nodes
                #print("Skipping node: ", node_name)
                continue

            # processing input edges
            o_edges = len(node.o_edges)
            #print("output edges: ", o_edges)

            if o_edges > 1:
                print("Calculate sum for node: ", node_name)
                # try to sum up the values from outgoing edges
                # and sum them up if all known
                sum_p = 0
                sum_f = 0
                no_solved_edges = 0
                for oe in node.o_edges:
                    #print("  output edge", oe.get_name(), oe.passed_tests, oe.failed_tests)
                    if oe.is_solved():
                        sum_p = sum_p + oe.passed_tests
                        sum_f = sum_f + oe.failed_tests
                        no_solved_edges = no_solved_edges + 1
                print( "solved output edges: ", no_solved_edges)
                if no_solved_edges == o_edges:
                    node.set_tests(sum_p, sum_f)
                    print("Writing sums: ", sum_p, sum_f)

    def __solve_top_node(self, no_passed, no_failed):
        # we only have one top node
        self.top_node.set_tests(no_passed, no_failed)

    def add_numbers_to_node(self):
        '''
        sdasd
        :param __graph:
        :return:
        '''
        print("Adding numbers to nodes...")  # , __graph)
        for node in self.__node_list:
            # we ignore nodes like '__graph' and "\n"
            if node.get_name().isnumeric():
                # merge name and label, removing "" from label, and adding new ones
                node.set("label", '"' + node.get_name() + ". " + node.get_label()[1:-1] + '"')
                # print(node.get_attributes())
                # print("NEW: ", node.get_label())
        print("...done")
    
    def find_node(self,block_id):
        for node in self.__node_list:
            if node.get_name().strip().startswith(str(block_id)):
                return node
            
    def find_node_by_name(self,name):
        for node in self.__node_list:
            if node.get_name()==name:
                return node

    def fetch_counters_from_file(self, csv_file):
        ''' returns a list of counter values '''
        import csv

        with open(csv_file, newline='') as f:
            contents = csv.reader(f)
            # print("contents:", contents)
            for row in contents:
                # only interested in the first row
                # print("row", row)
                return row

    def __get_node_by_name(self, node_name):
        # print("searching for node:_", node_name, "_in ", __graph.get_name())
        for node in self.__node_list:
            # print("inspecting node:_", node.get_name(), "_")
            # apparently node names have spaces around
            if node.get_name() and node.get_name() == node_name:
                # print("node found: ", node.get_name(), node.get_label())
                return node
        # print("node NOT found: ")
        return None

    # todo add doc
    def __get_edge_by_name(self, edge_name):
        # print("searching for edge:_", edge_name, "_in ", __graph.get_name())
        for edge in self.__edge_list:
            # print("inspecting edge:_", edge.get_name(), "_")
            # apparently edge names have spaces around??
            if edge.get_name() and edge.get_name() == edge_name:
                # print("edge found: ", edge.get_name(), edge.get_label())
                return edge
        # print("edge NOT found: ")

    def __search_edge_by_dest_node(self, node):
        # print("searching for node:_", node.get_name(), "_in_", __graph.get_name())
        for e in self.__graph.__edge_list:
            # print("inspecting edge:_", e.get_label(), "_", e.get_destination(), "label: ", node.get_label())
            if e.get_destination() == node.get_name():
                # print("edge found", e.get_label())
                return e
        # print("Edge not found")

    def __get_successor_edge_node(self, node):
        # TODO: this is non-deterministic, search for edge instead
        # returns outgoing edge of a node and its dest node
        # print("searching successor for node:_", node.get_label(), "_in_", __graph.get_name())
        # find edge exiting node
        for edge in self.__edge_list:
            # print("inspecting edge:_", edge.get_label(), "_")
            # apparently edge names have spaces around??
            if edge.get_source() == node.get_name():
                # print("edge found: ",  edge.get_label(), "dest node:", edge.get_destination())
                # looking for destination node
                return edge, self.__get_node_by_name(edge.get_destination())
        print("successor not found : terminal node")
        return None, None

    def __get_predecessor_edge_node(self, node):
        # TODO: this is non-deterministic, search for edge instead
        # returns incoming edge of a node and its source node
        # print("searching predecessors for node:_", node.get_name(), "_in_", __graph.get_name())
        # find edge exiting node
        for edge in self.__edge_list:
            # print("inspecting edge:_", edge.get_label(), "_")
            # apparently edge names have spaces around??
            if edge.get_destination() == node.get_name():
                # print("edge found: ",  edge.get_label(), "dest node:", edge.get_source())
                # looking for destination node
                return edge, self.__get_node_by_name(edge.get_source())
        print("predecessor not found : start node node")
        return None, None

    def remove_counter_elements_from_nodes_and_adding_to_edges(self):
        pattern = r'c\[\d+\]'
        
        for node in self.__node_list:
            node_label = node.get_label().strip('"')
            
            if re.search(pattern, node_label):
                lines = node_label.split('\n')
                new_lines = []
                
                for line in lines:
                    if not re.search(pattern, line):
                        new_lines.append(line)
                
                # Reconstruct the node label
                new_node_label = '\n'.join(new_lines)
                new_node_label = new_node_label.strip()
                
                # Update the node label
                node.set("label", f'"{node.get_name() + ". "+new_node_label}"')
                
                # Extract pattern from the first line matching the pattern
                for line in lines:
                    if re.search(pattern, line):
                        extracted_pattern = ''.join(re.findall(pattern, line))
                        break
                
                # Update edges connected to this node
                for edge in self.__edge_list:
                    if edge.get_destination() == node.get_name():
                        edge_label = edge.get_label() or ''
                        new_edge_label = edge_label + '\n' + extracted_pattern
                        edge.set_label(new_edge_label.strip())

    def add_suspiciousness_information(self, module_data, module_name):
        # sets edge width according to suspiciousness
        # print("***** Adding execution information on module ", module_name)
        # # print("Adding execution info module data ")
        # [print("{}:{}".format(x, module_data[x])) for x in module_data.keys()]
        # # getting list of counters
        # # we expect the module data in the shape
        # # {"module_name": {"pt": [], ft[], s_score[[]

        pattern = re.compile('c\[([\d]+)\]')

        # we add to counter edges the following info: "(pt, ft) sc'
        for edge in self.__edge_list:
            # print("Edge x: ", edge, edge.get_label())

            if edge.get_label() and 'c[' in edge.get_label():
                # print("found edge")
                old_label = edge.get_label()
                idx = int(re.search(pattern, old_label).groups()[0])

                # print("old label: ", old_label, idx, old_label) #+ str(module_data["tp"][idx-1]))
                

                tp = str(self.get_particular_test_value(module_data,'tp',idx))

                tf = str(self.get_particular_test_value(module_data,'tf',idx))

                ss = str(self.get_particular_ss_for_edge(module_data,'ss',edge))

                print('TP, TF, SS', tp,tf,ss)

                if(ss is not None and float(ss)!=0):
                    new_label = "  Score: {}".format(ss)

                    # print("old label: ", old_label, idx)
                    edge.set_label(old_label +'\n'+ new_label)

                # changing edge width based on suspiciousness score
                ss_list=[item['value'] for item in module_data["ss"]]
               
                maxs = max(ss_list)
                if float(ss) > 0.0:
                    # edge_inc = 1+(module_data["ss"][idx - 1] * max(module_data["ss"]) * 30)
                    edge_inc = 1 + (float(ss) / maxs) * 4
                    #print("setting edge width: ", edge_inc)
                    edge.set_penwidth(edge_inc)
        print("..done")

    def add_suspicious_scores_everywhere(self,sus_score):
        pattern = r'c\[\d+\]'
        for idx, edge in enumerate(self.__edge_list):
                old_label=''
                if edge.get_label():
                    old_label=str(edge.get_label())
                ss = str(sus_score[idx])
                print('EDGE LABEL SUS: ',edge.get_label())
                if float(ss) > 0.0 and edge.get_label() is not None and re.search(pattern, edge.get_label()):
                    ss_list=sus_score
                    maxs = max(ss_list)
                    new_label = "\n Score: {}".format(ss)
                    edge.set_label(old_label+''+new_label)
                    edge_inc = 1 + (float(ss) / maxs) * 4
                    edge.set_penwidth(edge_inc)
        print("..done")

    def get_particular_test_value(self,module_data,type_of_data,idx):
        print('Module Type Data: ',module_data[type_of_data])
        tp_values = module_data[type_of_data]
        for item in tp_values:
            if item['name'] == idx:
                return item['value']
        return None  # If the name is not found
    
    
    def get_particular_ss_for_edge(self,module_data,type_of_data,edge):
        print('Module Type Data: ',module_data[type_of_data])
        tp_values = module_data[type_of_data]
        for item in tp_values:
            if item['edge_name'] == edge.name:
                return item['value']
        return None  # If the name is not found
    

    def get_test_val(self,type_of_test,idx):
        for item in type_of_test:
            if item['name'] == idx:
                return item['value']
        return None  # If the name is not found


    def __get_i_edges(self, node_name, edge_list):
        return [e for e in edge_list if e.get_destination() == node_name]

    def __get_o_edges(self, node_name, edge_list):
        return [e for e in edge_list if e.get_source() == node_name and "_calls" not in e.get_destination()]

    def __get_idx(self, string):
        pattern = re.compile('c\[([\d]+)\]')
        return int(re.search(pattern, string).groups()[0])

    def __extend_Node(self):
        print("Extending Node class")
        # adding additional attributes and methods to Edge class
        # instantiate an Edge object to add members
        node = pydot.Node()
        node.__class__.passed_tests = -1
        node.__class__.failed_tests = -1
        node.__class__.i_edges = []
        node.__class__.o_edges = []

        def __set_xlabel(self, str1, str2):
            self.set("xlabel",
                     "<<br></br><br></br><br></br><font color='darkorange'>{},{}</font>>".format(str1, str2))

        def __is_solved(self):
            return self.passed_tests > -1 and self.failed_tests > -1

        def __set_tests(self, pt, ft):
            self.failed_tests = ft
            self.passed_tests = pt
            #print("setting tests for node {}: {} {}".format(self.get_name(), self.passed_tests, self.failed_tests))
            self.set_xlabel(pt, ft)

        def __get_tests(self):
            return self.passed_tests, self.failed_tests

        node.__class__.set_xlabel = __set_xlabel
        node.__class__.is_solved = __is_solved
        node.__class__.set_tests = __set_tests
        node.__class__.get_tests = __get_tests

    def __extend_Edge(self):
        print("Extending Edge class")
        # adding additional attributes and methods to Edge class
        # instantiate an Edge object to add members
        edge = pydot.Edge()
        edge.__class__.id = None
        edge.__class__.name = "a"
        edge.__class__.passed_tests = -1
        edge.__class__.failed_tests = -1
        edge.__class__.label = ""

        def set_name(self, s1, s2):
            # print("setting name: ", s1 + "->" + s2)
            self.name = str(s1) + "->" + str(s2)

        def get_name(self):
            return self.name

        def __set_xlabel(self, str1, str2):
            self.set("xlabel", "<<font color='darkmagenta' style='background-color:white;'><br/><br/>     {},{}  <br/><br/></font>>".format(str1, str2))






            
        def __is_solved(self):
            return self.passed_tests > -1 and self.failed_tests > -1

        def __set_tests(self, pt, ft):
            self.failed_tests = ft
            self.passed_tests = pt
            #print("setting tests for edge {}: {} {}".format(self.get_name(), self.passed_tests, self.failed_tests))
            self.set_xlabel(pt, ft)

        edge.__class__.get_name = get_name
        edge.__class__.set_name = set_name
        edge.__class__.is_solved = __is_solved
        edge.__class__.set_xlabel = __set_xlabel
        edge.__class__.set_tests = __set_tests

    def create_simplified_graph(self):
        # remove elements with 0,0 counterssss
        print("no edges {} no nodes {}".format(
            len(self.__edge_list),
            len(self.__node_list)))

        print("edges...")
        for e in self.__edge_list:
            print(e.passed_tests, e.failed_tests)
            if e.passed_tests == 0 and e.failed_tests == 0:
                print(" removing edge :", e.get_source(), e.get_destination(), e.passed_tests, e.failed_tests )
                self.__graph.del_edge(e.get_source(), e.get_destination())

        print("nodes...")
        for n in self.__node_list:
            print(n.passed_tests, n.failed_tests)
            if n.passed_tests == 0 and n.failed_tests == 0:
                print(" removing node :", n.get_name(), n.passed_tests, n.failed_tests)
                self.__graph.del_node(n)

        print("no edges {} no nodes {}".format(
            len(self.__graph.get_edge_list()),
            len(self.__graph.get_node_list())))
        
    def get_edge_list(self):
        return self.__edge_list

