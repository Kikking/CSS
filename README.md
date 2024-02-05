# Benchmarking Nanopore Basecalling Tools
Dependencies:

     streamlit
     pandas
     matplotlib
     (Data is stored on GitHub Long Form Storage (LFS))

This takes data generated using Long-Read Quality Control tools to effectively measure the produced read lengths. LongQC was used to analyse results from the Guppy Basecaller and Nanoplot was used to analyse results from the Dorado Basecaller. 

# Data Extraction
File names are abbreviated according to their cell type. eg, A_d_r1r3 comes from the A549 cell line and K_d_r1r2 comes from the K562 cell line. This information was thus extracted to the Cell column using the following code:

     temp['cell'] = temp['sample_name'].apply(lambda x: 'A549' if 'A' in x else
                                           'MCF7' if 'M' in x else
                                           'K546' if 'K' in x else
                                           'HepG2' if 'H' in x else
                                           'Hct116' if 'Hc' in x else
                                           None)
            
 # Read Length Distribution 
 In Nanopore Sequencing, long reads are everything. Measuring this metric is thus an important indicator of the accuracy of the Neural Network deployed by each Basecaller. 

 To display the data in Streamlit, a function !length_plot! can be used that takes both data frames from each basecaller and an optional parameter to control the X-axis of the Histogram plots. 
     
     length_plot(df,df2, xfilt=5000)
     
 The mean read length of each dataset is calculated:
 
       df_mean = df["lengths"].mean()
      df2_mean =df2["lengths"].mean()

Both graphs are plotted together as a subplot:
       
        fig, axs = ml.subplots(2, sharex= True)
        
          #Dorado Plot
          axs[0].hist(df2[df2["basecaller" ]== "Dorado"]["lengths"], bins =3000 )
          ml.ylim((0, 300000))
          axs[0].vlines(df2_mean, ymin = 0, ymax = 300000)
          
          #Guppy Plot
          axs[1].hist(df[df["basecaller" ]== "Guppy"]["lengths"], bins =3000)
          ml.ylim((0, 300000))
          axs[1].vlines(df_mean, ymin = 0, ymax = 300000, label = "Mean")


# Sequence Quality Plot 
To compare the quality of each sequence across the dataframe, a line plot is implemented. 
     
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

# Plot Calling 

To allow for easier calling of plot functions, a wrapper function was created to call either plotting function based on the "feature" parameter specified. 

     def df_maker(url,feature,tool):
         if tool == "nanoplot":
             df = nanostat(url,feature)
         elif tool == "longqc":
             df = sdust_sum(url,feature)
         return df

# Streamlit Integration

Two column sections were defined to organise the buttons across the page:
  
    col1, col2 = str.columns(2)  # Create two columns with equal width

To ensure that the plot is generated in the centre of the page, an empty container is created. 

    plot_container = str.empty()
    
The length plot is then called when each button is clicked. 

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

               
              
        

         

 

