import subprocess
import os
import re

if __name__ == '__main__':
    testCaseDirectory = 'test_cases'
    pythonFilePath = "put_your_code_here/knights_and_knaves.py"
    resPath = 'out_put'
    
    if not os.path.exists(resPath):
        os.makedirs(resPath)

    allTestCases = os.listdir(testCaseDirectory)

    for testCaseName in allTestCases:
        if not re.match('.*\.txt$',testCaseName):
            continue
        testFilePath = f'test_cases/{testCaseName}\n'

        process = subprocess.Popen(["python3", pythonFilePath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error_output = process.communicate(input=testFilePath)
        outputContent = 'Subprocess output:\n\n' + output + '-----------------------\nSubprocess error output:\n\n' + error_output + '-----------------------'
        print(outputContent)

        outputPath = f'{resPath}/RESULT{testCaseName}'
        with open(outputPath, 'w') as file:
            file.write(outputContent)