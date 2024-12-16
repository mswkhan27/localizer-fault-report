

## Name
FaultLocalizer

## Description

### Steps for Localizing the Program

Python version: 3.9
Install the requirements. (pip install -r requirements.txt)
Install graphviz
File to run: runner_gui.py

1. Choose src file. (from examples folder e.g. examples>multiply>multiply.py)
2. Choose the entry point. (select the main function i.e. multiply in case of multiply)
3. Choose the Test File
4. Select the score metric.
5. Run the program.
    a. First, it will create the CG without annotation. (using PyCG)
    b. Then, it will instrument the file by including counters after each predicate and function definition and give counter list size present in each method.
    c. Then it will execute the tests and it will populate the counter value for each module depends on the name of the counter.
    d. After that, it will split the instrument file into sub files.
    e. CFG for each methods will be created from these split instrumented files.
    f. Calculates the suspiciousness score based on the counter values with passed and failed counters.
    g. Calculate Max scores per method.
    h. Annotate the CFG.
    i. Not working with these python programs:
        - Some Class Based
        - for conditions in one line. for (x in if ....)
        - method defining another method in it def a(): def b(): return 1
6. Output: Call Graph (for multi-function), CFGs, Fault Report, Simplified Fault Report.

---
If you want to run all examples at once using script.
Follow these steps:
1. python runner.py
2. See examples folders, it will be updated with outputs.


CLI:
#How to Run?
#e.g: python39 runner.py --project_path "examples/hex_conversion/" --file_n "hex_conversion.py" --test_file "examples/hex_conversion/tests/tests.txt" --outputFile "fault_summary.json" --debug --entry_point "hex_conversion" --metric "savg"