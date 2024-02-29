1. SETTING THE PROBLEM STATEMENT

1.1 Objective
The goal of this project is to analyze and gain insights from a video games dataset. The dataset includes information about various video games, such as their titles, release dates, developers, publishers, genres, age ratings and platform. The main objectives are to clean the data, conduct a comprehensive analysis, and visualize key trends.

2. ACQUIRING THE DATA 

2.1 Data Source
The video games dataset was obtained from Kaggle, providing a diverse set of information about different video games.

2.2 Project Structure
The project is organized into two files: one containing functions (video_games.py) and another for calling these functions (video_games_access.py). This separation aims to enhance code modularity and readability.

2.3 Libraries
Relevant libraries such as pandas and matplotlib, seaborn, and logging have been installed to facilitate data manipulation, analysis, visualization, and logging of key information.

2.4 Directories and Output Files
Necessary directories and output files have been created to store processed data, logs, and visualizations. This ensures a well-organized structure for the project.

2.5 Initial Data Exploration
Basic exploratory data analysis has been performed to check information, description, and the first few rows of the dataset. This initial exploration provides insights into the structure and content of the data.

3. CLEANING THE DATA 

3.1 Data Cleaning Steps
•	Unnecessary columns such us user score and user rating counts have been removed for project focus. Remaining columns have been renamed for clarity.
•	Blank rows, blank cells and duplicate entries have been eliminated to ensure data accuracy.
•	The content of the "Age Rating" column has been standardized for better comprehension.
•	The 'Platforms Info' column was processed to extract exclusive platform information, excluding metascore and count details. The extracted platform information was then stored in a new column named 'Platform,' and subsequently, the original 'Platforms Info' column was removed for clarity and conciseness.
•	The cleaned dataset has been exported to a new CSV and XLSX file for further analysis.

4. ANALYSING THE DATA

4.1 Key Analysis Steps
• Game counts, determined by titles, have been counted.
• Analysis based on release date, developers, publishers, genres, age ratings, and platform includes the following:
• Counting the number of games
• Identifying the most common
• Identifying the least common

5. VISUALISING THE DATA
5.1 Bar & Line Charts
Visual representations in the form of graphs (bas and lines) have been created for release dates, developers, publishers, genres, age ratings, and platforms.

By following these steps, the project aims to provide a thorough understanding of the video games dataset, enabling meaningful insights and supporting decision-making processes related to the gaming industry.

IF I HAD MORE TIME I WOULD HAVE DONE
Performed additional cross-analysis to reveal further insights.

IF YOU WOULD LIKE TO KNOW MORE ABOUT MY PROJECT
For additional information regarding this project or specific analyses conducted, please check the link below:
