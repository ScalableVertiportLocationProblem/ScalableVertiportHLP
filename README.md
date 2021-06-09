The data and results in this repository are a snapshot of the data and results that were used in the research reported on in the paper Scalable Vertiport Hub Location Selection for Air Taxi Operations in a Metropolitan Region by Chen et al.

## Content

This repository includes
1. Results folder which includes CSV file of all the tables in Section Experimental Results and Appendix. The name of these files is their corresponding label in the manuscript.

2. Data folder which includes: 
   - raw data
     - requests.csv, containing 185,077 trip records of Beijing. Each record in the dataset includes the longitude and latitude of the origination and destination of the trip.
     - Base.png, which is the non-hubable area of Beijing, including the area inside the Second Ring Road (filled with gray), leisure area (filled with green), districts and protected infrastructures (filled with red), and water area (filled with blue).
     
   - Folder cw, which contains the cost(distance) matrix and demand matrix. Given $n_b$, the whole area is divided as $n_b \times n_b$ grid cells, and the corresponding cost matrix is saved in "cij%d.csv"%n_b while demand matrix in "wij%d.csv"%n_b.
   
   - Folder non_hub_area, which contains the non-hubable area of Beijing. Given $n_b$, the whole area is divided as $n_b \times n_b$ grid cells, and the corresponding index of the non-hubable area is saved in "non_hub%d.csv"%n_b.
   
   - codes used for generating cost matrix, demand matrix, and list of non-huable area (Requirements: NumPy, pandas, PIL, skimage)
     - data_process_cw.py, which generates cost matrix and demand matrix. Before running, make sure there are requests.csv and folder named cw in the same directory.
     - non_hub.py, which generates a list of non-hubable areas. Before running, make sure there are Base.png and folder named non_hub_area in the same directory.

We provide dataset of cost matrix, demand matrix, and non-hubable area for grid division with n_b ranging from 3 to 34. Interesting readers can use the provided python codes to generate the corresponding dataset with different grid divisions.
## Other resources
In the online supplement, we also provide results on the AP and URAND dataset.

[AP]( https://users.monash.edu/~andrease/Downloads.htm) dataset can be fetched via this website https://users.monash.edu/~andrease/Downloads.htm

[URAND]( http://turing.mi.sanu.ac.rs/~nenad/phub/) dataset can be fetched via this website http://turing.mi.sanu.ac.rs/~nenad/phub/ 
