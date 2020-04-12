import tkinter as tk
import pandas as pd
import numpy as np
import os,sys
import time
import datetime
import os.path
from os import path
from os import listdir



window = tk.Tk()
window.geometry("500x400")
window.title("USI GUI")

tk.Label(window,text="File-1 (csv,excel)").grid(row=0)
e1 = tk.Entry(window,bd=5,width=30)
e1.grid(row=0,column=5)

tk.Label(window,text="File-2 (csv,excel)").grid(row=1)
e2 = tk.Entry(window,bd=5,width=30)
e2.grid(row=1,column=5)


   

'''
    reformat to specific spec

'''
def auto_script(df):
    
    required_list = ["Level","Number","*Description","Lifecycle Phase","BOM.UOM","BOM.AltItemGroup","BOM.TW&PL usage(%)","BOM.SH&KS&JQ usage(%)","BOM.Qty","BOM.Ref Des"]
    try:
        
        data = df[required_list]
        output = data[data['Lifecycle Phase']!="Document Released"]
        output = output.drop(['Lifecycle Phase'],axis=1)
        output.index = np.arange(1,len(output)+1)
        #output.to_excel("revised_"+f)
        return output
    except:
        print("mistake from auto script ")
        pass


    


def match(path1,path2):
    df_1 = pd.read_excel(path1)
    df_1 = auto_script(df_1)
    
    df_2 = pd.read_excel(path2)
    df_2 = auto_script(df_2)
    
    f_1 = df_1['Number'].unique()
    f_2 = df_2['Number'].unique()
    list_ = list(set(f_1).symmetric_difference(set(f_2)))
    same_=list(set(f_1).intersection(f_2))
    

    '''
        for two bom report intersection
    '''
    df_same = pd.DataFrame()
    df1 = df_1.loc[df_1['Number'].isin(same_)]
    df1.dropna(subset=['BOM.Ref Des'],inplace=True)
    
    df2 = df_2.loc[df_2['Number'].isin(same_)]
    df2.dropna(subset=['BOM.Ref Des'],inplace=True)
    
    same_num = []
    dec = []
    for _1,_2,num in zip(df1['BOM.Ref Des'],df2['BOM.Ref Des'],df1['Number']):

        try:
            list_1 = []
            element_1 = _1.split(",")
            for e in element_1:
                list_1.append(e)
            list_2 = []
            element_2 = _2.split(",")
            for e in element_2:
                list_2.append(e)
            diff = list(set(list_1).symmetric_difference(set(list_2)))
            if len(diff) == 0:
                pass
            else:
                same_num.append(num)
                dec.append(diff)
        except:
            pass
    
    from_ =[]
    df = pd.DataFrame()
    for l in list_:
        if len(df_1[df_1.Number == l])!=0:
            from_.append(path1)
        elif len(df_2[df_2.Number ==l])!=0:
            from_.append(path2)
        else:
            pass
    df['Different Number'] = list_
    df['From'] = from_
    df_same['Same Number'] = same_num
    df_same['BOM.Ref Des'] = dec
    if len(same_num) ==0:
        print("file is perfect")
    else:
        pass
    return df,df_same
 
'''
            Process data with correct format

'''


def getEnter():
    input_1 = e1.get()
    input_2 = e2.get()
    result,result_same = match(input_1,input_2)
    result.to_csv(input_1+"_Not_"+input_2+".csv")
    result_same.to_csv(input_1+"_And_"+input_2+".csv")
    

    

'''
    clear all input in the labels

'''
def clear():
    e1.delete(0,'end')    
    e2.delete(0,'end')
        # creating a button instance

EnterButton = tk.Button(window,text="Enter",command=getEnter)
QuitButton = tk.Button(window,text="Cancel",command=clear)
EnterButton.place(x=190,y=115)
QuitButton.place(x=250,y=115)
window.mainloop()
