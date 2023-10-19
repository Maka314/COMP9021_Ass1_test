import subprocess
import os
import re

if __name__ == '__main__':
    testCaseDirectory = 'test_cases'
    expDirectory = 'expected_output'
    pythonFilePath = "put_your_code_here/knights_and_knaves.py"
    resPath = 'out_put'
    
    if not os.path.exists(resPath):
        os.makedirs(resPath)

    ques_len = 51 
    allTestCases = os.listdir(testCaseDirectory)
    allExpectedOutputs = os.listdir(expDirectory)

    for testCaseName in allTestCases:
        if not re.match('.*\.txt$',testCaseName):
            continue
        testFilePath = f'{testCaseDirectory}/{testCaseName}'

        process = subprocess.Popen(["python3", pythonFilePath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error_output = process.communicate(input=testFilePath)

        output = output[ques_len:-1]
        # Compared with the expect output if provided
        if testCaseName in allExpectedOutputs:
            print(testFilePath.split('/')[1], '->', end=' ')
            
            with open(f"{expDirectory}/{testCaseName}", 'r') as f:
                expected_output = ""
                lines = f.readlines()
                for line in lines:
                    expected_output += line

                if output == expected_output:
                    print('\x1b[6;30;42m' + 'Passed' + '\x1b[0m')
                else:
                    print('\x1b[6;30;41m' + 'Failed' + '\x1b[0m')
                    print('----- Compared --------')
                    print('Output:', output, sep='\n')
                    print()
                    print('Expected:', expected_output, sep='\n')
                    print('----------------------')
                    
        outputPath = f'{resPath}/RESULT_{testCaseName}'
        outputContent = 'Subprocess output:\n\n' + output + '\n' + '-----------------------\nSubprocess error output:\n\n' + error_output + '-----------------------'
        with open(outputPath, 'w') as file:
            file.write(outputContent)