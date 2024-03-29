# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:08:32 2024

@author: User
"""

import streamlit as str
import pandas as pd
import matplotlib.pyplot as ml
import numpy as np

#TOY DATA from Github Repo
guppy_K = "https://github.com/Kikking/CSS/raw/9e119a7bc200a745bfb87a0754109a482ef8d2df/streamlit_data/longqc/K_d_r1r2/longqc_sdust.txt"
guppy_A = "https://github.com/Kikking/CSS/raw/9e119a7bc200a745bfb87a0754109a482ef8d2df/streamlit_data/longqc/A_d_r1r3/longqc_sdust.txt"
dor_K = "https://github.com/Kikking/CSS/raw/00d971f95050da35005850a02bc06ffdae8a331e/streamlit_data/nanoplot/K_d_r1r2/NanoPlot-data.tsv.gz"
dor_A = "https://github.com/Kikking/CSS/raw/ee71314afcf0ccb0d26c9bcd78d9da1d436bc1b6/streamlit_data/nanoplot/A_d_r1r3/NanoPlot-data.tsv.gz"
str.set_page_config(page_title="My App", page_icon=None, layout="centered")#theme = "dark")


# To extract variable names as a string (eg, dork_K to "dor_K" so that cell type can be determined from name)
def print_var_name(variable):
    if variable.find("A_d") != -1:
        return "A549"
    elif variable.find("K_d") != -1:
        return "K562"
    else: return "No Cell Detected"

# To read in QC data from nanoplot
def nanostat(url,feature):

    QC_table = pd.DataFrame()
    print(url)      
    temp = pd.read_table(url, sep ='\t')
    temp["sample_name"] = print_var_name(url)
    #for length data
    if feature == "l":
        temp = temp[["lengths","sample_name"]]
    #for sequence quality data
    elif feature == "q":
        temp = temp[["quals","sample_name"]]   
    temp["basecaller"] = "Dorado"
    temp['cell'] = temp['sample_name'].apply(lambda x: 'A549' if 'A' in x else
                                   'MCF7' if 'M' in x else
                                   'K546' if 'K' in x else
                                   'HepG2' if 'H' in x else
                                   'Hct116' if 'Hc' in x else
                                   None)
    
    QC_table = pd.concat([QC_table, temp])
    return QC_table
        
#for extracting data from longQC. feature = {"quals" or "lengths"}
def sdust_sum(url, feature):
    
    QC_table = pd.DataFrame() 
    
    temp = pd.read_csv(url, sep="\t", names=["read_name", "num_masked", "lengths", "masked_fraction", "quals", "QV7"])
    temp["sample_name"] = print_var_name(url)
    #for length data
    if feature == "l":
        temp = temp[["lengths","sample_name"]]
    #for sequence quality data
    elif feature == "q":
        temp = temp[["quals","sample_name"]]
    temp["basecaller"] = "Guppy"
     
    temp['cell'] = temp['sample_name'].apply(lambda x: 'A549' if 'A' in x else
                                   'MCF7' if 'M' in x else
                                   'K546' if 'K' in x else
                                   'HepG2' if 'H' in x else
                                   'Hct116' if 'Hc' in x else
                                   None)
      
    QC_table = pd.concat([QC_table, temp])
       
    return QC_table

     

#Deploys either nanostat() or sdust_sum() based on specified tool. ("longqc" or "nanoplot")
@str.cache_data
def df_maker(url,feature,tool):
    if tool == "nanoplot":
        df = nanostat(url,feature)
    elif tool == "longqc":
        df = sdust_sum(url,feature)
    return df

#plots a line graph comparing sequence quality between two dataframes made by df_maker().
def line_plot(df,df2):
    fig, ax = ml.subplots()
    df = df.sort_values(by='quals', ascending=True)
    df['row_number'] = range(1, len(df) + 1)
   
    df2 = df2.sort_values(by='quals', ascending=True)
    df2['row_number'] = range(1, len(df2) + 1)
    ax.plot(df['row_number'], df["quals"], label=df["basecaller"][0], linewidth=1.2, alpha=0.8)
    ax.plot(df2['row_number'], df2["quals"], label=df2["basecaller"][0], linewidth=1.2, alpha=0.8)
    ml.style.use('dark_background')
    ml.legend()
       
#plots a histogram of read-length distribution between two dataframes made by df_maker().
def length_plot(df,df2, xfilt=5000, yfilt = 300000):
    df_mean = df["lengths"].mean()
    df2_mean =df2["lengths"].mean()
    fig, axs = ml.subplots(2, sharex= True)
    
    #Dorado
    axs[0].hist(df2[df2["basecaller" ]== "Dorado"]["lengths"], bins =3000 )
    ml.xlim((0 ,xfilt))
    ml.ylim((0, yfilt))
    ml.xlabel("Read Length")
    axs[0].set_title("Read Length Distribution")
    axs[0].set_ylabel('DORADO')
    axs[0].vlines(df2_mean, ymin = 0, ymax = yfilt)
    
    #Guppy
    axs[1].hist(df[df["basecaller" ]== "Guppy"]["lengths"], bins =3000)
    ml.xlim((0 ,xfilt))
    ml.ylim((0, yfilt))
    axs[1].set_ylabel('GUPPY')
    axs[1].vlines(df_mean, ymin = 0, ymax = yfilt, label = "Mean")
    
    ml.style.use('dark_background')
    ml.legend()


str.title("Nanopore DNA Sequencing Software Benchmark")
str.write("""
          DNA sequencing implements machine-learning to interpret signal data generated by Oxford Nanopore Technologies Sequencing Platform into meaningful strings of DNA sequences. 
          The two competing basecallers compared here: Guppy and Dorado.  
          """)


#Drop down bar options
options = ["","Sequence Quality", "Sequence length"]
selected_option = str.selectbox("Select an option:", options)

#Response after clicking on dropdown bar
if selected_option == "Sequence length":
    
    #Button Options:
    str.subheader("Click on a Cell Type to Analyse:")
    col1, col2 = str.columns(2)  # Create two columns with equal width
    plot_container = str.empty() # An empty container to stop the plot from sitting in the columns
    with col1:
         if str.button('Blood Cells'):
             plot_container.write("Massaging Data...")
             plot_container.empty()
           # Display plot from function
             plot_container.pyplot( length_plot(df_maker(guppy_K, "lengths", "longqc"),df_maker(dor_K, "lengths", "nanoplot"), yfilt = 30000))
             
       
    with col2:
         if str.button('Lung Cells'):
             plot_container.write("Massaging Data...")
             plot_container.empty()
           # Display plot from function
             plot_container.pyplot( length_plot(df_maker(guppy_A, "lengths", "longqc"),df_maker(dor_A, "lengths", "nanoplot")))
           

elif selected_option == "Sequence Quality":
    str.subheader("Click on a Cell Type to Analyse:")
    col1, col2 = str.columns(2)  # Create two columns with equal width
    plot_container = str.empty()
    with col1:
         if str.button('Blood Cells'):
             plot_container.write("Massaging Data...")
             x=3
             plot_container.empty()
           # Display plot from function
             
             plot_container.pyplot( line_plot(df_maker(guppy_K, "quals", "longqc"),df_maker(dor_K, "quals", "nanoplot")))
                
            
       
    with col2:
         if str.button('Lung Cells'):
             plot_container.write("Massaging Data...")
            
             x=0
             plot_container.empty()
           # Display plot from function
             plot_container.pyplot( line_plot(df_maker(guppy_A, "quals", "longqc"),df_maker(dor_A, "quals", "nanoplot")))


     



