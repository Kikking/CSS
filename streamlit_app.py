# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:08:32 2024

@author: User
"""

import streamlit as str
#import os
import pandas as pd
import matplotlib.pyplot as ml
import numpy as np



str.set_page_config(page_title="My App", page_icon=None, layout="centered")#theme = "dark")

#for extracting data from nanoplot. x = {0 (A549) or 1 (K562)}. feature = {"quals" or "lengths"}
def nanostat(x,feature):
    nano_directory_path = "C:/Users/User/CSS/streamlit_data/nanoplot"
    nano_stats = os.listdir(nano_directory_path)
    QC_table = pd.DataFrame()
      
    temp_file = nano_stats[x:x+1]
    print(temp_file)
    for sample in temp_file :
          file_path = os.path.join('D:\SGNEX\\nplot', sample, 'NanoPlot-data.tsv.gz')
          if os.path.exists(file_path):
              temp = pd.read_csv(file_path, sep ='\t')
              temp["sample_name"] = sample
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
        
          else: print(f"The file {file_path} does not exist.")
#for extracting data from longQC. x = {0 (A549) or 1 (K562)}. feature = {"quals" or "lengths"}
def sdust_sum(x, feature):
    long_directory_path = "C:/Users/User/CSS/streamlit_data/longqc"
    long_stats = os.listdir(long_directory_path)
    QC_table = pd.DataFrame() 
    temp_file = long_stats[x:x+1]
    for sample in temp_file:
        
        file_path = os.path.join("C:/Users/User/CSS/streamlit_data/longqc", sample, "longqc_sdust.txt")
        if os.path.exists(file_path):
            temp = pd.read_csv(file_path, sep="\t", names=["read_name", "num_masked", "lengths", "masked_fraction", "quals", "QV7"])
            temp["sample_name"] = sample
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

        else: print(f"The file {file_path} does not exist.")

#Deploys either nanostat() or sdust_sum() based on specified tool. ("longqc" or "nanoplot")
def df_maker(x,feature,tool):
    if tool == "nanoplot":
        df = nanostat(x,feature)
    elif tool == "longqc":
        df = sdust_sum(x,feature)
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
    #str.pyplot(fig)    
#plots a histogram of read-length distribution between two dataframes made by df_maker().
def length_plot(df,df2, xfilt=5000):
    df_mean = df["lengths"].mean()
    df2_mean =df2["lengths"].mean()
    fig, axs = ml.subplots(2, sharex= True)
    
    #Dorado
    axs[0].hist(df2[df2["basecaller" ]== "Dorado"]["lengths"], bins =3000 )
    ml.xlim((0 ,xfilt))
    ml.ylim((0, 300000))
    ml.xlabel("Read Length")
    axs[0].set_title("Read Length Distribution")
    axs[0].set_ylabel('DORADO')
    axs[0].vlines(df2_mean, ymin = 0, ymax = 300000)
    
    #Guppy
    axs[1].hist(df[df["basecaller" ]== "Guppy"]["lengths"], bins =3000)
    ml.xlim((0 ,xfilt))
    ml.ylim((0, 300000))
    axs[1].set_ylabel('GUPPY')
    axs[1].vlines(df_mean, ymin = 0, ymax = 300000, label = "Mean")
    
    ml.style.use('dark_background')
    ml.legend()
    #ml.show(fig)
    #str.pyplot(fig)

str.title("Nanopore DNA Sequencing Software Benchmark")
str.write("""
          DNA sequencing implements machine-learning to interpret signal data generated by Oxford Nanopore Technolies Sequencing Platform into meaningful strings of DNA sequence. 
          Two competing basecallers:Guppy and Dorado.  
          """)
#str.text_input("What plot?:", "bar graph.......")


options = ["","Sequence Quality", "Sequence length"]
selected_option = str.selectbox("Select an option:", options)

if selected_option == "Sequence length":
   

    str.subheader("Click on a Cell Type to Analyse:")
    col1, col2 = str.columns(2)  # Create two columns with equal width
    plot_container = str.empty()
    with col1:
         if str.button('Blood Cells'):
             plot_container.write("Massaging Data...")
             x=3
             plot_container.empty()
           # Display plot from function
             
             plot_container.pyplot( length_plot(df_maker(1, "lengths", "longqc"),df_maker(1, "lengths", "nanoplot")))
                
            
       
    with col2:
         if str.button('Lung Cells'):
             plot_container.write("Massaging Data...")
            
             x=0
             plot_container.empty()
           # Display plot from function
             plot_container.pyplot( length_plot(df_maker(0, "lengths", "longqc"),df_maker(0, "lengths", "nanoplot")))
           

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
             
             plot_container.pyplot( line_plot(df_maker(1, "quals", "longqc"),df_maker(1, "quals", "nanoplot")))
                
            
       
    with col2:
         if str.button('Lung Cells'):
             plot_container.write("Massaging Data...")
            
             x=0
             plot_container.empty()
           # Display plot from function
             plot_container.pyplot( line_plot(df_maker(0, "quals", "longqc"),df_maker(0, "quals", "nanoplot")))


     



