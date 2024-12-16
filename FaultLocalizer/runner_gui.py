import json
import webbrowser
import PySimpleGUI as sg
from src import utils
import os
import base64
import io
import shutil
import threading
from PIL import Image
import regex as re
from src.localizer import Localizer
import webbrowser
import subprocess
import platform

def resize_image(image_path, resize=None):
    try:
        # Load the image from file or memory
        if isinstance(image_path, str):
            img = Image.open(image_path)
        else:
            img = Image.open(io.BytesIO(base64.b64decode(image_path)))

        # Detect original size of the image
        cur_width, cur_height = img.size

        # Resize proportionally if resize is requested
        if resize:
            new_width, new_height = resize
            img = img.resize((new_width, new_height), Image.LANCZOS)

        # Save the resized image to a bytes buffer
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        return bio.getvalue(), (cur_width, cur_height)  # Return the image and the original resolution

    except Exception as e:
        print(f"Error resizing image: {e}")
        return None, (0, 0)  # Return None if resizing fails

def update_image_display(image_element, zoom_level, image_path):
    try:
        min_zoom, max_zoom = -3, 5  # Define limits for zoom level
        zoom_factor = max(min_zoom, min(zoom_level, max_zoom))  # Clamp zoom level within the range


        if  isinstance(image_path, str):
            img = Image.open(image_path)
        else:
            img = Image.open(io.BytesIO(base64.b64decode(image_path)))

        # Detect original size of the image
        cur_width, cur_height = img.size
      
        # Get original width and height
        original_width, original_height = img.size
        print('ORIGINAL SIZE: ',img.size)
        # Scale width and height based on zoom level while maintaining the aspect ratio
        new_width = int(original_width * (1 + zoom_factor * 0.1))
        new_height = int(original_height * (1 + zoom_factor * 0.1))

        # Resize and update the image with the new dimensions
        resized_image, size_upated = resize_image(image_path, resize=(new_width, new_height))

        w,h=size_upated
        image_element.update(data=resized_image)
        
    except Exception as e:
        print(f"Error updating image display: {e}")

def update_image_and_column(image_element, column_element, zoom_level, image_path):
    new_width, new_height = update_image_display(image_element, zoom_level, image_path)
    # Update the column size to accommodate the new image size
    column_element.update(size=(new_width + 20, new_height + 20))

def load_menu_from_file():
    try:
        with open("menu_layout.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def clear_folder(folder_path):
    def clear():
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            os.mkdir(folder_path)

    thread = threading.Thread(target=clear)
    thread.start()


def is_empty_list(lst):
    return isinstance(lst, list) and not lst


def read_passed_failed_tests(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        if len(lines) != 2:
            raise ValueError("Invalid file format or insufficient lines")

        passed_tests = eval(lines[0])
        failed_tests = eval(lines[1])

        return [passed_tests, failed_tests]

    except FileNotFoundError:
        return "File not found"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"An error occurred: {str(e)}"


def count_passed_failed_tests(file_name):
    total_tests = read_passed_failed_tests(file_name)

    if isinstance(total_tests, str):  # Check for error messages
        return total_tests

    passed_tests = total_tests[0]
    failed_tests = total_tests[1]

    if not (isinstance(passed_tests, list) and isinstance(failed_tests, list)):
        return "Invalid format in the file"
    num_passed_tests = len(passed_tests)
    num_failed_tests = len(failed_tests)

    return f"Number of passed tests: {num_passed_tests}\nNumber of failed tests: {num_failed_tests}"


def file_format_error(file_name):
    try:
        total_tests = read_passed_failed_tests(file_name)

        if isinstance(total_tests, str):  # Check for error messages
            return True

        passed_tests = total_tests[0]
        failed_tests = total_tests[1]

        if not (isinstance(passed_tests, list) and isinstance(failed_tests, list)):
            return True

        return False
    except ValueError as e:
        return True
    except Exception as e:
        return True

def reset_fields(window):
    window['mbox'].update("")
    window['input_project_path'].update("")
    window['input_file_n'].update("")
    #window['selected-function'].update("")
    window['mtfile'].update("")
    window["fgraph"].update("")
    pass

def show_buttons(window, disable_buttons):
    print("DISABLED BUTTON: " + str(disable_buttons))
    window['Clear Folders'].update(disabled=disable_buttons)
    window['-Zoom'].update(disabled=disable_buttons)
    window['+Zoom'].update(disabled=disable_buttons)
    window['in-test-file'].update(disabled=disable_buttons)
    window['RUN'].update(disabled=disable_buttons)
    window['View Report'].update(disabled=disable_buttons)
    window['View Simplified Report'].update(disabled=disable_buttons)
    window['View Call Graph'].update(disabled=disable_buttons)
    window['View CFG'].update(disabled=disable_buttons)
    pass

def gen(loc,window):
    try:
        message=''
        for msg in loc.generate_call_graph():
            message+=msg+'\n'
            window['mbox'].update(message, text_color="black")

        loc.pre_localizer()
        for msg in loc.localize_python():
                message+=msg+'\n'
                window['mbox'].update(message, text_color="black")

        for msg in loc.creating_cfgs_and_calculating_suspiciousness():
                message+=msg+'\n'
                window['mbox'].update(message, text_color="black")
        
        f = [loc.create_fault_summary,loc.annotate_call_graph,loc.generating_reports]
        for fun in f:
            for msg in fun():
                message+=msg+'\n'
                window['mbox'].update(message, text_color="black")
        return True
    except Exception as e:
        print("Error: ", e)
        msg = "Error: " + str(e)
        window['mbox'].update(msg, text_color='Red')
        window.refresh()
        return False

def run_localizer_thread(loc,window):
    def run_localizer(loc,window):
        isGen = gen(loc,window)
        if isGen:
            window['View Report'].update(visible=True)
            window['View Simplified Report'].update(visible=True)
            window['View Call Graph'].update(visible=True)
            window['View Report'].update(disabled=False)
            window['View Simplified Report'].update(disabled=False)
            window['View Call Graph'].update(disabled=False)
            window['def-combo'].update(visible=True)
            window['View CFG'].update(disabled=False)
            window['View CFG'].update(visible=True)
            window['+Zoom'].update(disabled=False)
            window['-Zoom'].update(disabled=False)
            
        else:
            window['View Report'].update(visible=False)
            window['View Simplified Report'].update(visible=False)
            window['View Call Graph'].update(visible=False)
            window['View CFG'].update(visible=False)
            window['View Report'].update(disabled=True)
            window['View Simplified Report'].update(disabled=True)
            window['View Call Graph'].update(disabled=True)
            window['View CFG'].update(disabled=True)
            window['+Zoom'].update(disabled=True)
            window['-Zoom'].update(disabled=True)
    threading.Thread(target=run_localizer, args=(loc, window)).start()


def run_gui():
    dynamic_buttons = {}  # Dictionary to store dynamically generated buttons
    sg.set_options(font=('Arial Italic', 16), text_color="#e9bc9b", scrollbar_color='black')
    # sg.theme('DarkAmber')
    sg.theme('DefaultNoMoreNagging')
    target_width, target_height = 1200, 768
    func_list = []
    project_path = ''  # values['input_project_path']
    file_n = ""
    function = ""
    disable_actions = True
    test_file_path = ""
    entry_point=''

    loc = None
    TEXT_COLOR = 'black'
    BACKGROUND_COLOR = "#87CEEB"
    BUTTON_BACKGROUND_COLOR = 'black'
    STANDARD_FONT_STYLE = ("Montserrat Bold", 10)

    left_column = [
        [sg.FileBrowse("Select Project File", enable_events=True, initial_folder=os.path.dirname(os.path.abspath(__file__)), key="in-file", target='in-file',
                    button_color=("white", BUTTON_BACKGROUND_COLOR), size=(15, 1), font=("Montserrat Bold", 9))],
        [sg.Text('Project Path', size=(15, 1), font=STANDARD_FONT_STYLE, text_color=TEXT_COLOR,
                background_color=BACKGROUND_COLOR)],
        [sg.InputText(key='input_project_path', text_color="#134f5c", size=(26, 10), font=("Montserrat Bold", 10))
        ],
        [sg.Text('File', font=STANDARD_FONT_STYLE, size=30, background_color=BACKGROUND_COLOR, text_color=TEXT_COLOR)],

        [sg.InputText(key='input_file_n', text_color="#134f5c", size=(26, 10), font=STANDARD_FONT_STYLE)],
        [sg.HorizontalSeparator()],
        [sg.Text('Select Entry Point', size=15, font=STANDARD_FONT_STYLE, background_color=BACKGROUND_COLOR,
                text_color=TEXT_COLOR)],
        [sg.Combo(func_list, key="entry-point-def-combo", size=(25, 1), font=STANDARD_FONT_STYLE, readonly=True, enable_events=True,
                    background_color='white', text_color='black')],

        [sg.HorizontalSeparator()],
        [sg.FileBrowse('Select Test File', enable_events=True,initial_folder=os.path.dirname(os.path.abspath(__file__)), key="in-test-file", target='in-test-file', size=(12, 1),
                    button_color='black', font=STANDARD_FONT_STYLE, disabled=False)],
        [sg.Text('Test File', font=STANDARD_FONT_STYLE, size=(15, 1), background_color=BACKGROUND_COLOR,
                text_color=TEXT_COLOR)],
    [sg.Text('', key="mtfile", font=STANDARD_FONT_STYLE, size=(24, 3), text_color=TEXT_COLOR)],
    
        [sg.HorizontalSeparator()],
        [sg.Text('Suspicious Score Metric', size=(25, 1), font=STANDARD_FONT_STYLE, background_color=BACKGROUND_COLOR, text_color=TEXT_COLOR)],
        [sg.Combo(['savg','Tarantula', 'Ochiai', 'Jaccard', 'Goodman'], key='suspicious_score_metric', size=(25, 1), font=STANDARD_FONT_STYLE, readonly=True,
                background_color='white', text_color='black')],

    
        [sg.HorizontalSeparator()],
    
        [sg.Text('Message ', font=STANDARD_FONT_STYLE, size=(15, 1), background_color=BACKGROUND_COLOR,
                text_color=TEXT_COLOR)],
        [sg.Multiline( key="mbox", font=STANDARD_FONT_STYLE, text_color=TEXT_COLOR, size=(25, 3), autoscroll=True)],
        

        [sg.HorizontalSeparator()],
        [
            sg.Button('RUN', size=(12, 1), key="RUN", button_color='#082567', mouseover_colors="#226366",
                    font=STANDARD_FONT_STYLE, disabled=False),
            sg.Checkbox("Debug mode", key='debug', default=True, font=STANDARD_FONT_STYLE),
        ],
            [sg.Button('Clear Folders', button_color=BUTTON_BACKGROUND_COLOR, mouseover_colors="#226366", size=(12, 1),
                font=STANDARD_FONT_STYLE, disabled=True)]

        ,
        [sg.HorizontalSeparator()],

      
        [sg.Combo(func_list, key="def-combo", size=(20, 1), font=STANDARD_FONT_STYLE, readonly=True, enable_events=True,
              background_color='white', text_color='black', visible=False),
     sg.Button('View CFG', button_color=BUTTON_BACKGROUND_COLOR, mouseover_colors="#226366", size=(12, 1),
               font=STANDARD_FONT_STYLE, disabled=False, visible=False)],
          [sg.Button('View Call Graph', button_color=BUTTON_BACKGROUND_COLOR, mouseover_colors="#226366", size=(12, 1),
                font=STANDARD_FONT_STYLE, disabled=False, visible=False)],  

        [sg.Button('View Report', button_color=BUTTON_BACKGROUND_COLOR, mouseover_colors="#226366", size=(12, 1),
                font=STANDARD_FONT_STYLE, disabled=False, visible=False),sg.Button('View Simplified Report', button_color=BUTTON_BACKGROUND_COLOR, mouseover_colors="#226366", size=(19, 1),
        font=STANDARD_FONT_STYLE, disabled=False, visible=False)],
        [sg.Button('Exit', key="bExit", button_color="#E40000", mouseover_colors="#226366", size=(12, 1),
                font=STANDARD_FONT_STYLE)],
        [sg.HorizontalSeparator()],
    ]

    right_column = [
        [
            sg.Column(
                [
                    [sg.Button('+Zoom', key="+Zoom", button_color=("white", "black"), mouseover_colors="#226366",
                            size=(12, 1), font=STANDARD_FONT_STYLE, disabled=False),
                    sg.Button('-Zoom', key="-Zoom", button_color=("white", "black"), mouseover_colors="#226366",
                            size=(12, 1), font=STANDARD_FONT_STYLE, disabled=False)],
                    [sg.Image(key="fgraph", filename="")]
                ],
                size=(target_width, target_height),
                expand_x=True,
                expand_y=True,
                background_color='white'
            )
        ]
    ]

    layout = [
        [
            sg.Column(left_column, pad=((10, 10), (10, 10)),  # Set the outer padding
                    expand_x=True,  # Expand column horizontally
                    expand_y=True,  # Expand column vertically
                    background_color=BACKGROUND_COLOR,
                    ),  # Left column with buttons
            sg.VerticalSeparator(),  # Separator for visual distinction
            sg.Column(right_column, background_color=BACKGROUND_COLOR)  # Right column with the graph placeholder
        ]
    ]

    # Create the Window
    window = sg.Window('FaultLocalizer 2.0', layout, size=(1200, 750), location=(200, 10), resizable=True,
                    background_color=BACKGROUND_COLOR)
    image_element = window["fgraph"]
    zoom_level = 0

    output_path = ""
    # Event Loop to process "events" and get the "values" of the inputs
    # Disabled Buttons

    function=''
    zoom_level = 0
    original_size = (1200, 768)
    zoom_factor = 1.1  # Zoom in by 10%, zoom out by 10%
    suspicious_score_metric=''

    while True:
        event, values = window.read()
        short_file_n = file_n.split('.')[0]
        current_size = image_element.get_size()
    
        # Zoom In
        if event == "+Zoom":
            zoom_level += 1
            if (output_path):
                print(output_path)
                update_image_display(image_element, zoom_level, output_path)

        if event == "-Zoom":
            zoom_level -= 1
            if (output_path):
                update_image_display(image_element, zoom_level, output_path)

        if event == "Clear Folders":
            utils.delete_folders(project_path + short_file_n + '_temp/')
            utils.delete_folders(project_path + short_file_n + '_debug/')
            utils.delete_folders(project_path + 'reports/')
            window['def-combo'].update(visible=False)
            window['View Report'].update(visible=False)
            window['View Simplified Report'].update(visible=False)
            window['View Call Graph'].update(visible=False)
            window['View CFG'].update(visible=False)
            window['mbox'].update("Folders cleared.")

        if event == "RUN":
            
            if values['suspicious_score_metric'] == "":
                sg.Popup("Select a scoring metric before running", text_color='Red', font=STANDARD_FONT_STYLE)
                continue

            if test_file_path == "":
                sg.Popup("Select a test file before running", text_color='Red', font=STANDARD_FONT_STYLE)
                continue

            if (test_file_path != "" and file_format_error(test_file_path) == True):
                sg.Popup("Test File Format not correct.", text_color='Red', font=STANDARD_FONT_STYLE)
                continue
            window['mtfile'].update(test_file_path)
            window["bExit"].update(disabled=True)
            loc = Localizer(project_path=project_path, file_n=file_n, test_file=test_file_path,
                            debug=values['debug'],outputFile='fault_summary.json',entry_point=entry_point, metric=values['suspicious_score_metric'])
            run_localizer_thread(loc=loc,window=window)

            window["bExit"].update(disabled=False)

        if event == "Select Function":
            print("working with file: ", window["in-file"], values["in-file"])
            with open(values["in-file"], "r") as f:

                func_list = []
                for line in f.readlines():
                    print("line: ", line)
                    if "def " in line and not "def main" in line:
                        func_list.append(line)
                print(func_list)
                sg.Popup(" Available functions: " + ' '.join(func_list), keep_on_top=True)
        
        if event == "Select Entry Point":
            with open(values["in-file"], "r") as f:
                func_list = []
                for line in f.readlines():
                    if "def " in line:
                        func_list.append(line)
                sg.Popup(" Available functions: " + ' '.join(func_list), keep_on_top=True)

        if event == "in-file":
            print("Browse triggered")
            test_file_path = ""
            reset_fields(window)
            print("working with file: ", window["in-file"], values["in-file"])
            window['View Report'].update(disabled=True)
            window['View Simplified Report'].update(disabled=True)
            window['View Call Graph'].update(disabled=True)
            window['View CFG'].update(disabled=True)
            window['View Report'].update(visible=False)
            window['View Simplified Report'].update(visible=False)
            window['View Call Graph'].update(visible=False)
            window['View CFG'].update(visible=False)
            file_path = values["in-file"]
            print('FILE PATH: ',file_path)
            print("file", file_path.split('/')[-1:][0])
            print("folder", '/'.join(file_path.split('/')[:-1]))
            file_n = file_path.split('/')[-1:][0]
            # create relative project path
            project_path = os.path.relpath('/'.join(file_path.split('/')[:-1])) + '\\'
            print("Proj path1: ", project_path)
            if '\\' in project_path:
                project_path = project_path.replace('\\', '/')

            print("Proj path2: ", project_path)

            window['input_project_path'].update(value=project_path)
            window['input_file_n'].update(value=file_n)
            # window['input_function'].update(value=settings['input_function'])

            # creating combo with functions
            with open(file_path, "r") as f:
                func_list = []
                for line in f.readlines():
                    # print("line: ", line)
                    if "def " in line:
                        func_list.append(line)
                print(func_list)

            window["def-combo"].update(values=func_list, value="Select a function")
            window["entry-point-def-combo"].update(values=func_list, value="Select a Entry Point")
            if(project_path):
                window['Clear Folders'].update(disabled=False)
            disable_actions = True

            window.refresh()


        if event == "in-test-file":  # select test file
            print("Browse test file triggered")
            print("working with file: ", window["in-test-file"], values["in-test-file"])
            test_file_path = values["in-test-file"]
            passed_failed_tests = count_passed_failed_tests(test_file_path)
            sg.Popup(passed_failed_tests, font=STANDARD_FONT_STYLE, text_color=TEXT_COLOR)
            window['mtfile'].update(test_file_path)

            window["bExit"].update(disabled=True)
        
        if event == 'suspicious_score_metric':
            print('On Change Sus. Score')
            suspicious_score_metric = values["suspicious_score_metric"]
            window.refresh()



        if event == 'def-combo':

            # extract function name
            function = re.search(r'def\s+\w+', values['def-combo']).group().split(' ')[1]
            window['mbox'].update(function)
            print(function)
            if (function):
                disable_actions = False
            window.refresh()
        
        if event == 'entry-point-def-combo':
            print("selecting file:", values['def-combo'])
            # window["selected-function"].update(values['entry-point-def-combo'][:-2])
            # extract entry point function
            entry_point = re.search(r'def\s+\w+', values['entry-point-def-combo']).group().split(' ')[1]
            print(entry_point)
            if (entry_point):
                disable_actions = False
            window.refresh()
        
        if event == "View Report":
            file_path = values["in-file"]
            parent_directory = os.path.dirname(file_path) + "/"
            reports_path = parent_directory + "reports/"
            print("PATH: ", reports_path + "fault_report.html")
            # utils.generate_html_report(temp_folder_path,"updated_fault_info.json")
            webbrowser.open('file://' + os.path.realpath(reports_path + "fault_report.html"))

        if event == "View Simplified Report":
            file_path = values["in-file"]
            parent_directory = os.path.dirname(file_path) + "/"
            reports_path = parent_directory + "reports/"
            print("PATH: ", reports_path + "simp_fault_report.html")
            # utils.generate_html_report(temp_folder_path,"updated_fault_info.json")
            webbrowser.open('file://' + os.path.realpath(reports_path + "simp_fault_report.html"))

        if event == "View Call Graph":
            output_path = project_path + short_file_n + '_temp/' + "CG.png"
            window["fgraph"].update(filename=output_path)
        
        if event == "View CFG":
            print('CFG Function: ',function)
            if function == "":
                sg.Popup("Select a function before running", text_color='Red', font=STANDARD_FONT_STYLE)
            else:
                output_path = project_path + short_file_n + '_temp/' + function + "_cfg.png"
                window["fgraph"].update(filename=output_path)

        if event == sg.WIN_CLOSED or event == 'bExit':  # if user closes window or clicks cancel
            break
        # show_buttons(window, disable_actions)

    # window.close()


    # put browsing

run_gui()
