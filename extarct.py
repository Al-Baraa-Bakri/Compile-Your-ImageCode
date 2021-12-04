# import  cv2 
import os
import pytesseract
from pytesseract import Output
from PIL import Image
import pandas as pd
import subprocess

def compailing(code , lang) :
    print(code)
    with open(f"output2.{lang}", "w") as text_file:
        text_file.write(code)
        text_file.close()
    p = subprocess.Popen(['python', f'output2.{lang}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell = True)
    out, err = p.communicate()
    print(out , err)


def extractFromPython(path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    custom_config = r'-c preserve_interword_spaces=1 --oem 1 --psm 1 -l eng+ita'
    d = pytesseract.image_to_data(Image.open(f"{path}"), config=custom_config, output_type=Output.DICT)
    df = pd.DataFrame(d)

    # clean up blanks
    df1 = df[(df.conf!='-1')&(df.text!=' ')&(df.text!='')]
    # sort blocks vertically
    sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()
    for block in sorted_blocks:
        curr = df1[df1['block_num']==block]
        sel = curr[curr.text.str.len()>3]
        char_w = (sel.width/sel.text.str.len()).mean()
        prev_par, prev_line, prev_left = 0, 0, 0
        text = ''
        for ix, ln in curr.iterrows():
            # add new line when necessary
            if prev_par != ln['par_num']:
                text += '\n'
                prev_par = ln['par_num']
                prev_line = ln['line_num']
                prev_left = 0
            elif prev_line != ln['line_num']:
                text += '\n'
                prev_line = ln['line_num']
                prev_left = 0

            added = 0  # num of spaces that should be added
            if ln['left']/char_w > prev_left + 1:
                added = int((ln['left'])/char_w) - prev_left
                text += ' ' * added 
            text += ln['text'] + ' '
            prev_left += len(ln['text']) + added + 1
        text += '\n'
        compailing(text , 'py')
def extractFromC(imageSrc) :
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(Image.open(f'{imageSrc}'))
    compailing(text , 'cpp')

#For C++
#extractFromC("YOUR PATH HERE")

#For Python
#extractFromPython("YOUR PATH HERE")


