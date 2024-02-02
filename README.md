# Benchmarking Nanopore Basecalling Tools

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

# Streamlit Integration

Two column sections were defined to organise the buttons across the page:
  
    col1, col2 = str.columns(2)  # Create two columns with equal width

To ensure that the plot is generated in the centre of the page, an empty container is created. 

    plot_container = str.empty()
    
The length plot is then called when each button is clicked. Each button assigns a different x value passed to the data processing functions. x = 0 calls the A549 dataset and x = 2 calls the K562 dataset. 

    with col1:
         if str.button('Blood Cells'):
             plot_container.write("Massaging Data...")
             x=3
             plot_container.empty()
           # Display plot from function
             
             plot_container.pyplot( length_plot(sdust_sum(x),nanostat(x)))
              
    with col2:
         if str.button('Lung Cells'):
             plot_container.write("Massaging Data...")
             x=0
             plot_container.empty()
           # Display plot from function
             plot_container.pyplot( length_plot(sdust_sum(x),nanostat(x)))
               
              
        

         

 

