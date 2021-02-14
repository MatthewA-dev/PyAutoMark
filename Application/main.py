import sys
import os
import shutil
import json
import zipfile
from pathlib import Path
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from importlib import import_module, reload
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

from main_window import Ui_MainWindow
from moodle_window import Ui_MoodleWindow


class Main(QMainWindow):
    def __init__(self):
        # Initialize the main window
        super().__init__()
        
        # Main directory (Pyinstaller friendly code)
        if getattr(sys, 'frozen', False):
            self.main_dir = os.path.dirname(sys.executable)
        else:
            self.main_dir = os.path.dirname(os.path.abspath(__file__))
            
        #Build the main window interface from main_window.py
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Read in config settings from config.json
        with open(Path(self.main_dir, 'config.json'), 'r') as f:
            self.config = json.load(f)
            
        # Define key variables
        self.button1_dir = self.config['default_dir1']
        self.button2_dir = self.config['default_dir2']
        self.button1_bool = False
        self.button2_bool = False
        self.checked = [] # this will hold all previously checked zipped file paths
        self.modules = [] # this will hold all previously imported student assignments
        self.win2button1_dir = self.config['default_dir_win2_1'] # On Moodle window
        self.win2button2_dir = self.config['default_dir_win2_2'] # On Moodle window
        
        # Define menubar functionality
        self.ui.actionMoodle.triggered.connect(self.moodle_handler)
        self.ui.actionClear.triggered.connect(self.clear_handler)
        self.ui.actionReset.triggered.connect(self.reset_handler)
        self.ui.actionDocumentation_PDF.triggered.connect(self.doc_handler)
        
        # Defining button functionality
        self.ui.button1.clicked.connect(self.button1_handler)
        self.ui.button2.clicked.connect(self.button2_handler)
        self.ui.button3.clicked.connect(self.button3_handler)
        self.ui.button4.clicked.connect(self.button4_handler)
        
        # Define list functionality
        self.ui.list1.itemDoubleClicked.connect(self.list1_handler)
        
    def button1_handler(self):
        filename = QFileDialog.getOpenFileName(None, "Select a solution key (.py).", self.button1_dir, "Python file (*.py)")
        self.button1_file = filename[0]
        self.button1_dir = os.path.dirname(self.button1_file)
        self.button1_basename = os.path.basename(self.button1_file)

        if self.button1_file != "":
            # update label
            self.ui.label1.setText(self.button1_basename)
            self.button1_bool = True
            
            # update the config file
            path = os.path.dirname(self.button1_file)
            self.config['default_dir1'] = path
            with open('config.json', 'w') as f:
                json.dump(self.config, f)
        else:
            self.button1_bool = False
            self.ui.label1.setText("")
        
        if self.button1_bool == True and self.button2_bool == True:
            self.ui.button3.setEnabled(True)
        else:
            self.ui.button3.setEnabled(False)
            
    def button2_handler(self):
        filename = QFileDialog.getOpenFileNames(None, "Select any number of student assignments (.zip).", self.button2_dir, "Zip file(s) (*.zip)")
        self.button2_list = filename[0]
        
        if self.button2_list != []:
            # update label
            self.ui.label2.setText("{0} zip file(s) selected".format(len(self.button2_list)))
            self.button2_bool = True
            
            self.button2_dir = os.path.dirname(self.button2_list[0]) # used in button3_handler
            
            # update the config file
            path = os.path.dirname(self.button2_list[0])
            self.config['default_dir2'] = path
            with open('config.json', 'w') as f:
                json.dump(self.config, f)
        else:
            self.button2_bool = False
            self.ui.label2.setText("")
            
        if self.button1_bool == True and self.button2_bool == True:
            self.ui.button3.setEnabled(True)
        else:
            self.ui.button3.setEnabled(False)
             
    def button3_handler(self):
        # Obtain needed paths and import the solution key 
        head, tail = os.path.split(self.button1_file) #store the sol dir and the sol file in separate local variables
        trim_tail = os.path.splitext(tail)[0]
        sys.path.insert(1, head) # places the desired dir in the correct place for import_module below
        solMod = import_module(trim_tail) # variables defined in trim_tail should be referenced as: solMod.variable
        
        # Loop through each zip file in self.button2_list
        self.extracted_dir = Path(self.button2_dir, "Temp_Extracted")
        for zip_file in self.button2_list:
            # we continue to the next zip_file if the current one is in 'checked'
            if zip_file not in self.checked:
                # First, we determine if the zip_file was a bulk moodle download or an individual moodle download
                # Bulk moodle download file format: 'firstname lastname_ID#_assignsubmission_file_.zip' - set by Moodle
                # Individual moodle download file format: 'A#_firstname.zip' - set by me
                keyword = "A{0}_".format(solMod.assignment_num) # from solution key
                file_name = Path(zip_file).stem # returns the basename of the zip_file
                if keyword in file_name:
                    student_name = file_name.replace(keyword,'')
                else:
                    student_name = file_name[:file_name.find('_')]
                
                # word = zip_file[zip_file.rfind('/')+1:]
                # word1 = "A{0}_".format(solMod.assignment_num)
                # word2 = word.replace(word1, '')
                # student_name = word2.replace('.zip', '')

                # Define the output text file for this student
                self.output_dir = Path(self.button2_dir, "Output_Summaries")
                Path(self.output_dir).mkdir(parents=True, exist_ok=True) #checks if output_dir exists - if not, it creates it
                
                # Initialize the output text file.
                # If the zip_file is from a bulk moodle download, the name must be file_name for easy feedback dump.
                #self.output_file = Path(self.output_dir, "{0}{1}{2}".format(word1,student_name,".txt"))
                self.output_file = Path(self.output_dir, "{0}{1}".format(file_name,".txt"))
                with open(self.output_file, 'w') as f:
                    f.write("Assignment {0}\n\n".format(solMod.assignment_num))
                      
                # Extract zipped assignment submission
                with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                    zip_ref.extractall(self.extracted_dir)
                
                # Running grade total
                self.grade = 0
                NHI = False
                
                # Run each python script in extracted_dir and compare it to the inputs/outputs in solMod.Q_all
                marked_questions = []
                question_numbers = list(range(1,len(solMod.Q_all)+1))
                
                for i in question_numbers:
                    mark = 0 # Initialize the mark that a student gets on a question as 0
                    for entry in os.scandir(self.extracted_dir):
                        if "A{0}_{1}.py".format(solMod.assignment_num, i) in entry.path:
                            marked_questions.append(i)
                            if type(solMod.Q_all[i-1]) is dict:
                                inputs = list(solMod.Q_all[i-1].keys())
                                outputs = list(solMod.Q_all[i-1].values())
                                #call method
                                mark = self.question(i, entry, inputs, outputs, self.output_file, solMod.Q_weight, solMod.Q_flexible) 
                            else:
                                inputs = []
                                outputs = [solMod.Q_all[i-1]]
                                #call method
                                mark = self.question(i, entry, inputs, outputs, self.output_file, solMod.Q_weight, solMod.Q_flexible)
                            break
                            
                    self.grade += mark
                    
                if question_numbers != marked_questions:
                    unmarked_questions = sorted(list(set(question_numbers) - set(marked_questions)))
                    with open(self.output_file, 'a') as f:
                        output_arg = str(unmarked_questions)[1:-1]
                        f.write("{0}The following questions were not found: {1}.".format(chr(0x002A), output_arg))
                        NHI = True
                
                # Update table heading 'Grade' with the assignment total
                item = self.ui.table1.horizontalHeaderItem(1)
                item.setText("Grade /{0}".format(sum(solMod.Q_weight)))
                
                # Populate the table with the name of the student and his/her grade
                rowPosition = self.ui.table1.rowCount()
                self.ui.table1.insertRow(rowPosition)
                self.ui.table1.setItem(rowPosition,0, QTableWidgetItem(student_name))
                if NHI == True:
                    item = QTableWidgetItem(str(self.grade)+ chr(0x002A))
                else:
                    item = QTableWidgetItem(str(self.grade))
                
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.table1.setItem(rowPosition,1, item)
                
                # Populate the list with the name of the output text file
                self.ui.list1.addItem(QListWidgetItem("{0}.txt".format(file_name)))
                #self.ui.list1.addItem(QListWidgetItem("{0}{1}.txt".format(word1, student_name)))
            
                # Add zip_file to checked if it isn't in already
                self.checked.append(zip_file)
                
                # Detete the 'Temp_Extracted' directory and all of its contents
                if Path(self.extracted_dir).is_dir():
                    shutil.rmtree(self.extracted_dir) # detete the 'Temp_Extracted' directory and all of its contents
        
        self.ui.button4.setEnabled(True)

    def button4_handler(self):
        os.startfile(self.output_dir) # Windows only; this lauches the folder that contains the output .txt files (in explorer)
   
    def list1_handler(self, item):
        os.startfile("{0}\\{1}".format(self.output_dir, item.text())) # Windows only;

    def moodle_handler(self):
        self.MoodleWindow = MoodleWindow()
        self.MoodleWindow.show()
        
    def clear_handler(self):
        self.ui.table1.setRowCount(0) # clears the table
        # Reset table heading 'Grade'
        item = self.ui.table1.horizontalHeaderItem(1)
        item.setText("Grade")
        self.ui.list1.clear()
        self.checked = []
    
    def reset_handler(self):
        self.ui.table1.setRowCount(0) # clears the table
        # Reset table heading 'Grade'
        item = self.ui.table1.horizontalHeaderItem(1)
        item.setText("Grade")
        self.ui.list1.clear()
        self.checked = []
        self.config_initialize()
        
        # Read in config settings from config.json
        with open(Path(self.main_dir, 'config.json'), 'r') as f:
            self.config = json.load(f)
            
        # Define key variables
        self.button1_dir = self.config['default_dir1']
        self.button2_dir = self.config['default_dir2']
        self.win2button1_dir = self.config['default_dir_win2_1']
        self.win2button2_dir = self.config['default_dir_win2_2']
        
        # Reset labels
        self.ui.label1.setText('')
        self.ui.label2.setText('')
        
        # Disable the bottom two buttons
        self.ui.button1_bool = False
        self.ui.button2_bool = False
        self.ui.button3.setEnabled(False)
        self.ui.button4.setEnabled(False)
        
    def config_initialize(self):
        config = {"default_dir1": self.main_dir, "default_dir2": self.main_dir, "default_dir_win2_1": self.main_dir, "default_dir_win2_2": self.main_dir} # This resets the default path to the program location
        with open(Path(self.main_dir, 'config.json'), 'w') as f:
            json.dump(config, f)
    
    def doc_handler(self):
        doc = Path(self.main_dir, "PyAutoMark_Documentation.pdf")
        os.startfile(doc)
        
    def question(self, Q_num, file, inp, outp, outfile, weight, flexible):
        # Note: The outfile is opened in append mode; all console output is also written outfile.
        head, tail = os.path.split(file.path) #store the sol dir and the sol file in separate local variables
        trim_tail = os.path.splitext(tail)[0]
        sys.path.insert(1, head)
        
        # This is broken into two main types of solutions: (1) No user input is expected; (2) User input is expected.
        # Recall: 'inp' contains the user input from the solution key. 
        if inp == []:
            # Properly format the desired output from the solution key (with newlines)
            if type(outp[0]) is tuple:
                formatted_output = self.in_out_with_newlines(outp[0])
            else:
                formatted_output = str(outp[0])
            
            # Capture the result of the submission
            result = self.running_assignments(trim_tail, None)
            
            # For printing out to text files
            print_out = formatted_output.replace("\n", "\\n")
            print_res = str(result).replace("\n", "\\n")
            
            # Report output or errors.
            # If Q_num is in solMod.Q_flexible, then we check only for containment.
            # We also lower case both the key and the submission when checking if flexible.
            if Q_num in flexible:
                if type(outp[0]) is tuple:
                    # If the type is a tuple then we check each element of the tuple for containment in result.
                    containment_check = []
                    for element in outp[0]:
                        containment_check.append(str(element).lower() in result.lower()) #holds True or False (lower case everything)
                    
                    if True in containment_check: # only require one True for a success
                        with open(outfile, 'a') as f:
                            f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, print_res))
                        return 0
                    else:
                        with open(outfile, 'a') as f:
                            f.write("{0}. Correct\n\n".format(Q_num))
                        return weight[Q_num-1]
                else:
                    # This is the simple case: no newlines should be presented in desired ouput.
                    # Again, if flexible, then everything is lower cased.
                    if formatted_output.lower() not in result.lower():
                        with open(outfile, 'a') as f:
                            f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, print_res))
                        return 0
                    else:
                        with open(outfile, 'a') as f:
                            f.write("{0}. Correct\n\n".format(Q_num))
                        return weight[Q_num-1]
            else: 
                if result != str(formatted_output): # Checks for strict equality
                    #print("{0}. Incorrect\n      Desired output: {1} \n      Your output: {2}".format(Q_num, outp[0], result.stdout))
                    with open(outfile, 'a') as f:
                        f.write("{0}. Incorrect\n     Desired output: {1} \n     Your output: {2}\n\n".format(Q_num, print_out, result))
                    return 0
                else:
                    #print("{0}. Correct\n".format(Q_num))
                    with open(outfile, 'a') as f:
                        f.write("{0}. Correct\n\n".format(Q_num))
                    return weight[Q_num-1]
        else:
            success = True
            console_output = []
    
            # We check each list of inputs in 'input' and compare them to the corresponding outputs in 'outputs'.
            for i in range(len(inp)):
                # Properly format the desired output from the solution key (with newlines)
                if type(outp[i]) is tuple:
                    formatted_output = self.in_out_with_newlines(outp[i])
                else:
                    formatted_output = str(outp[i])
                
                # Properly format the input with newlines
                if type(inp[i]) is tuple:
                    formatted_input = self.in_out_with_newlines(inp[i])
                    result = self.running_assignments(trim_tail, formatted_input)
                else:
                    result = self.running_assignments(trim_tail, str(inp[i]))
                
                # For printing out to text files
                print_out = formatted_output.replace("\n", "\\n")
                print_res = str(result).replace("\n", "\\n")
            
                # Report output or errors.
                # If Q_num is in solMod.Q_flexible, then we check only for containment
                if Q_num in flexible:
                    if type(outp[i]) is tuple:
                        # If the type is a tuple then we check each element of the tuple for containment in result.
                        # We also lower case both the key and the submission when checking if flexible.
                        containment_check = []
                        for element in outp[i]:
                            containment_check.append(str(element).lower() in result.lower())
                        
                        if False in containment_check:
                            success = False
                            console_output.append("    -Test {0}: failure\n".format(i+1))
                            console_output.append("       Input: {0}\n       Desired output: {1}\n       Your output: {2}\n\n".format(inp[i], print_out, print_res))
                        else:
                            if i == len(inp)-1:
                                console_output.append("    -Test {0}: success\n\n".format(i+1))
                            else:
                                console_output.append("    -Test {0}: success\n".format(i+1))
                    else:
                        # This is the simple case: no newlines should be presented in desired ouput.
                        # We also lower case both the key and the submission when checking if flexible.
                        if formatted_output.lower() not in result.lower():
                            success = False
                            console_output.append("    -Test {0}: failure\n".format(i+1))
                            console_output.append("       Input: {0}\n       Desired output: {1}\n       Your output: {2}\n\n".format(inp[i], print_out, print_res))
                        else:
                            if i == len(inp)-1:
                                console_output.append("    -Test {0}: success\n\n".format(i+1))
                            else:
                                console_output.append("    -Test {0}: success\n".format(i+1))
                else:
                    if result != formatted_output: # Checks for strict equality
                        success = False
                        console_output.append("    -Test {0}: failure\n".format(i+1))
                        console_output.append("       Input: {0}\n       Desired output: {1}\n       Your output: {2}\n\n".format(inp[i], print_out, print_res))
                    else:
                        if i == len(inp)-1:
                            console_output.append("    -Test {0}: success\n\n".format(i+1))
                        else:
                            console_output.append("    -Test {0}: success\n".format(i+1))
            
            if success:
                #print("{0}. Correct".format(Q_num))
                with open(outfile, 'a') as f:
                    f.write("{0}. Correct\n".format(Q_num))
                for line in console_output:
                    #print(line)
                    with open(outfile, 'a') as f:
                        f.write(line)
                return weight[Q_num-1]
            else:
                #print("{0}. Incorrect".format(Q_num))
                with open(outfile, 'a') as f:
                    f.write("{0}. Incorrect\n".format(Q_num))
                for line in console_output:
                    #print(line)
                    with open(outfile, 'a') as f:
                        f.write(line)
                return 0

    def running_assignments(self, assignment, input_feed):
        output_feed = StringIO()
        with redirect_stdout(output_feed):
            with self.replace_stdin(StringIO(input_feed)):
                if assignment not in self.modules:
                    try:
                        varMod = import_module(assignment)
                        self.modules.append(assignment)
                        res = output_feed.getvalue().rstrip()
                    except Exception as err:
                        res = "Error: {0}".format(err)
                else:
                    try:
                        varMod = import_module(assignment)
                        varMod = reload(varMod)
                        res = output_feed.getvalue().rstrip()
                    except Exception as err:
                        res = "Error: {0}".format(err)
        return res
    
    def in_out_with_newlines(self, some_tuple):
        new_string = ""
        for x in some_tuple:
            temp_entry = "{0}\n".format(x)
            new_string += temp_entry
    
        new_string = new_string.rstrip()
        return new_string
    
    @contextmanager
    def replace_stdin(self, target):
        orig = sys.stdin
        sys.stdin = target
        yield
        sys.stdin = orig


class MoodleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MoodleWindow()
        self.ui.setupUi(self)
        
        # Set M equal to the Main class for access to its variables
        self.M = Main()
        
        # Define key variables
        self.win2button1_bool = False
        self.win2button2_bool = False
        
        # Defining button functionality
        self.ui.win2button1.clicked.connect(self.win2button1_handler)
        self.ui.win2button2.clicked.connect(self.win2button2_handler)
        self.ui.win2button3.clicked.connect(self.win2button3_handler)
        self.ui.win2button3.setEnabled(False)
        
    def win2button1_handler(self):
        self.moodle_zip = QFileDialog.getOpenFileName(None, "Select a single Moodle zip file (.zip).", self.M.win2button1_dir, "Zip file (*.zip)")[0] #returns as tuple: (path, type)
        self.moodle_zip_file = Path(self.moodle_zip)
        self.moodle_dir = Path(self.moodle_zip).resolve().parent # directory of the moodle zip
        self.moodle_name = Path(self.moodle_zip).stem # basename of the moodle zip
        self.new_moodle_dir = Path(self.moodle_dir, self.moodle_name)
        
        # update the config file if the user selected a zip
        if self.moodle_zip != "":
            self.ui.win2label1.setText(self.moodle_name)
            self.win2button1_bool = True
            
            # update the config file
            self.M.config['default_dir_win2_1'] = str(self.moodle_dir)
            with open('config.json', 'w') as f:
                json.dump(self.M.config, f)
        else:
            self.ui.win2label1.setText("")
            self.win2button1_bool = False
        
        if self.win2button1_bool == True and self.win2button2_bool == True:
            self.ui.win2button3.setEnabled(True)
        else:
            self.ui.win2button3.setEnabled(False)
    
    def win2button2_handler(self):
        student_dir = QFileDialog.getExistingDirectory(None, "Select a directory to extract student submissions.", self.M.win2button2_dir)
        self.student_submissions_dir = Path(student_dir)
        student_dir_basename = self.student_submissions_dir.stem
        
        # update the config file if the user selected a zip
        if student_dir != "":
            self.ui.win2label2.setText(student_dir_basename)
            self.win2button2_bool = True
            
            # update the config file
            self.M.config['default_dir_win2_2'] = str(self.student_submissions_dir)
            with open('config.json', 'w') as f:
                json.dump(self.M.config, f)
        else:
            self.ui.win2label2.setText("")
            self.win2button2_bool = False
        
        if self.win2button1_bool == True and self.win2button2_bool == True:
            self.ui.win2button3.setEnabled(True)
        else:
            self.ui.win2button3.setEnabled(False)
        
    def win2button3_handler(self):
        # Checks if Student_Submissions folder exists - if not, it creates it in the directory that contains the Moodle zip
        #zipped_submissions = Path(self.student_submissions_dir, "Student_Submissions")
        Path(self.student_submissions_dir).mkdir(parents=True, exist_ok=True)
        
        # Extract the zipped Moodle file
        with zipfile.ZipFile(self.moodle_zip_file, 'r') as zip_ref:
            zip_ref.extractall(self.new_moodle_dir)

        # Iterate over each folder in self.student_submissions_dir
        for entry in os.scandir(self.new_moodle_dir):
            # We prep future file for a single feedback file zip (following Moodle's formatting).
            full_moodle_name = entry.name
            for A_name_zip in Path(entry).iterdir(): # There should only be 1 zip file here
                extension = os.path.splitext(A_name_zip)[1]
                new_name = Path(full_moodle_name + extension)
                #shutil.move(A_name_zip, self.student_submissions_dir.joinpath(A_name_zip.name)) # replaces files if they already exist
                shutil.move(A_name_zip, self.student_submissions_dir.joinpath(new_name)) # replaces files if they already exist
                
        # Delete the self.new_moodle_dir and all of its contents
        if Path(self.new_moodle_dir).is_dir():
            shutil.rmtree(self.new_moodle_dir)
        

        os.startfile(self.student_submissions_dir) # Windows only; this lauches the folder that contains the extracted student submissions






if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec_())

















