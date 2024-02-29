# # # # # # # # # # # #
#   LIBRARIES         #
# # # # # # # # # # # #

import pandas as pd
import sys
from io import StringIO
import os
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import ast

# # # # # # # # # # # #
#   OUTPUT FILES      #
# # # # # # # # # # # #

# get the file path
def get_file_path(file_name, extension):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, f"{os.path.splitext(file_name)[0]}.{extension}")
    return file_path

def get_log_file_path(file_name):
    return get_file_path(file_name, "log")

def get_txt_file_path(file_name):
    return get_file_path(file_name, "txt")

def get_png_file_path(file_name):
    return get_file_path(file_name, "png")

def get_xlsx_file_path(file_name):
    return get_file_path(file_name, "xlsx")

def get_csv_file_path(file_name):
    return get_file_path(file_name, "csv")

# setup logging to save logs to a file
def setup_logging(log_file):
    logging.basicConfig(level=logging.INFO, filemode='w', filename=log_file)
    logging.getLogger().setLevel(logging.INFO)

# read the csv file, extract the name and create a txt output file
def start_process_csv_file(file_name):
    logging.info(f"'start process csv file' {file_name} started.")
    df = pd.read_csv(file_name)
    output_file = f"{os.path.splitext(file_name)[0]}.txt"
    output_buffer = StringIO()
    sys.stdout = output_buffer
    logging.info("'start process csv file' completed.")
    return df, output_file, output_buffer

# save the analysis results to the txt file
def end_process_csv_file(output_file, output_buffer):
    logging.info("'end process csv file' started.")
    sys.stdout = sys.__stdout__
    with open(output_file, "w") as output_file:
        output_file.write(output_buffer.getvalue())
        logging.info("'end process csv file' completed.")

# # # # # # # # # # # #
#   CHECKS            #
# # # # # # # # # # # #

# check if the excel file exists
def check_csv_file(file_name):
    logging.info("'check csv file' started.")
    if not os.path.isfile(file_name):
        logging.error(f"Error: csv file '{file_name}' not found.")
        sys.exit(1)
    else:
        logging.info("'check csv file' completed.")

# check if the columns exist
def columns_validation(df):
    logging.info("'columns validation' started.")
    required_columns = ['Title', 'Release Date', 'Developer', 'Publisher', 'Genres', 'Product Rating', 'User Score', 'User Ratings Count', 'Platforms Info']
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        missing_columns_str = ', '.join(missing_columns)
        logging.warning(f"Missing required column(s): {missing_columns_str}")
        sys.exit(1)
    else:
        logging.info("'columns validation' completed.")

# # # # # # # # # # # #
#   INFO              #
# # # # # # # # # # # #

# print the info of the excel file
def print_info(df):
    logging.info("'print info' started.")
    df.info()
    logging.info("'print info' completed.")

# print a description of the excel file
def print_description(df):
    logging.info("'print description' started.")
    print(df.describe())
    logging.info("'print description' completed.")

# print the first 5 rows of the excel file
def print_first_row(df):
    logging.info("'print first row' started.")
    print(df.head())
    logging.info("'print first row' completed.")

# # # # # # # # # # # #
#   CLEANING          #
# # # # # # # # # # # #

# removes columns from the dataframe
def remove_columns(df):
    logging.info("'remove columns' started.")
    df.drop(columns=['User Score', 'User Ratings Count', 'Platforms Info'], inplace=True)
    logging.info("'remove columns' completed.")

# rename column
def rename_column(df):
    logging.info("'rename column' started.")
    df.rename(columns={'Product Rating' : 'Age Rating', 'Genres' : 'Genre'}, inplace=True)
    logging.info("'rename column' completed.")

# removes rows from the dataframe
def remove_rows(df):
    logging.info("'remove rows' started.")
    df = df.drop([0], inplace=True)
    logging.info("'remove rows' completed.")

# removes duplicates from the dataframe
def remove_duplicates(df):
    logging.info("'remove duplicates' started.")
    df = df.drop_duplicates(inplace=True)
    logging.info("'remove duplicates' completed.")

# reset index after removing rows
def reset_index(df):
    logging.info("'reset index' started.")
    df = df.reset_index(drop=True, inplace=True)
    logging.info("'reset index' completed.")

# check missing values
def check_missing_values(df):
    logging.info("'check missing values' started.")
    missing_values = df.isnull().sum()
    print('Missing values:\n', missing_values)
    
    if missing_values.any():
        df.dropna(inplace=True)
    
    # df.fillna(value=fill_value, inplace=True)
    
    logging.info("'check missing values' completed.")
    return missing_values

# clean up the "Age Rating" column
def clean_age_rating(df):
    logging.info("'clean age rating' started.")
    rating_mapping = {
        'Rated T For Teen': 'Teen',
        'Rated E For Everyone': 'Everyone',
        'Rated M For Mature': 'Mature',
        'Rated E +10 For Everyone +10': 'Everyone +10',
        'Rated RP For Rate Pending': 'Rate Pending',
        'Rated AO For Adults Only': 'Adults Only'
    }
    df['Age Rating'] = df['Age Rating'].map(rating_mapping)
    logging.info("'clean age rating' completed.")

# extracting information from the "Platform" column
def extract_platform_info(df):
    logging.info("'extract platform info' started.")
    df['Platform'] = df['Platforms Info'].apply(lambda x: ast.literal_eval(x)[0]['Platform'] if pd.notnull(x) and ast.literal_eval(x) else None)
    logging.info("'extract platform info' completed.")

# # # # # # # # # # # #
#   TITLE             #
# # # # # # # # # # # #

# the sum of all the games
def total_games(df):
    logging.info("'total games' started.")
    total_games = df["Title"].count()
    print(f"The total games made is: {total_games:.0f}")
    logging.info("'total games' completed.")

# # # # # # # # # # # #
#   RELEASE DATE      #
# # # # # # # # # # # #

# counts all the games by release date
def count_release_date(df):
    logging.info("'count release date' started.")
    count_release_date = df["Release Date"].value_counts()
    count_release_date.index.name = None
    print("Games by release date:")
    print(count_release_date.to_string(name=False))
    logging.info("'count release date' completed.")

# highlight the most common release date
def most_common_release_date(df):
    logging.info("'most common release date' started.")
    most_common_release_date = df["Release Date"].mode().iloc[0]
    print(f"The most common release date is: {most_common_release_date}")
    logging.info("'most common release date' completed.")

# highlight the least common release date
def least_common_release_date(df):
    logging.info("'least common release date' started.")
    least_common_release_date = min(df["Release Date"].unique(), key=df["Release Date"].tolist().count)
    print(f"The least common release date is: {least_common_release_date}")
    logging.info("'least common release date' completed.")

# release date year bar chart
def release_date_year_bar_chart(df, file_name):
    logging.info("'release date year bar chart' started.")

    df['Release Year'] = pd.to_datetime(df['Release Date']).dt.year
    release_year_count = df['Release Year'].value_counts().sort_index()

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))

    bar_colors = sns.color_palette("viridis", len(release_year_count))
    bars = ax.bar(release_year_count.index.astype(int), release_year_count, color=bar_colors)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

    plt.xticks(release_year_count.index.astype(int), rotation=45)

    ax.set_title("Games Released by Year", fontsize=16, color='white')
    ax.set_xlabel("Year", fontsize=12, color='white')
    ax.set_ylabel("Games", fontsize=12, color='white')

    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    png_file_name = f"{os.path.splitext(file_name)[0]}_release_date_year.png"
    plt.savefig(png_file_name, bbox_inches='tight', dpi=300)
    logging.info("'release date year bar chart' completed.")

# release date month line chart
def release_date_month_line_chart(df, file_name):
    logging.info("'release date month line chart' started.")

    df['Release Year'] = pd.to_datetime(df['Release Date']).dt.year

    plt.style.use('dark_background')

    monthly_counts = df.groupby(['Release Year', pd.to_datetime(df['Release Date']).dt.month]).size().unstack()

    fig, ax = plt.subplots(figsize=(12, 6))

    line_colors = sns.color_palette("viridis", len(monthly_counts))

    for year, color in zip(monthly_counts.index, line_colors):
        ax.plot(monthly_counts.columns, monthly_counts.loc[year], marker='o', label=year, color=color)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax.set_xticks(monthly_counts.columns)
    ax.set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    ax.set_title("Games Released by Month", fontsize=16, color='white')
    ax.set_xlabel("Month", fontsize=12, color='white')
    ax.set_ylabel("Games", fontsize=12, color='white')

    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Year', title_fontsize='12', facecolor='black', edgecolor='white')

    png_file_name = f"{os.path.splitext(file_name)[0]}_release_date_month.png"
    plt.savefig(png_file_name, bbox_inches='tight', dpi=300)
    logging.info(f"'release date month line chart' completed.")

# # # # # # # # # # # #
#   DEVELOPER         #
# # # # # # # # # # # #

# counts all the games by developer
def count_developer(df):
    logging.info("'count developer' started.")
    count_developer = df["Developer"].value_counts()
    count_developer.index.name = None
    print("Games by developer:")
    print(count_developer.to_string(name=False))
    logging.info("'count developer' completed.")

# highlight the most common developer
def most_common_developer(df):
    logging.info("'most common developer' started.")
    most_common_developer = df["Developer"].mode().iloc[0]
    print(f"The most common developer is: {most_common_developer}")
    logging.info("'most common developer' completed.")

# highlight the least common developer
def least_common_developer(df):
    logging.info("'least common developer' started.")
    least_common_developer = min(df["Developer"].unique(), key=df["Developer"].tolist().count)
    print(f"The least common developer is: {least_common_developer}")
    logging.info("'least common developer' completed.")

# developer bar chart
def developer_bar_chart(df, file_name):
    logging.info("'developer bar chart' started.")

    developer_count_top = df['Developer'].value_counts().head(10)
    developer_count_bottom = df['Developer'].value_counts().tail(10)

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

    bar_colors_top = sns.color_palette("viridis", len(developer_count_top))
    bars_top = ax1.bar(developer_count_top.index, developer_count_top, color=bar_colors_top)

    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax1.set_title("Top 10 Developers", fontsize=16, color='white')
    ax1.set_xlabel("Developer", fontsize=12, color='white')
    ax1.set_ylabel("Games", fontsize=12, color='white')

    ax1.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')

    for bar in bars_top:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    bar_colors_bottom = sns.color_palette("viridis", len(developer_count_bottom))
    bars_bottom = ax2.bar(developer_count_bottom.index, developer_count_bottom, color=bar_colors_bottom)

    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax2.set_title("Bottom 10 Developers", fontsize=16, color='white')
    ax2.set_xlabel("Developer", fontsize=12, color='white')
    ax2.set_ylabel("Games", fontsize=12, color='white')

    ax2.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    for bar in bars_bottom:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    plt.subplots_adjust(hspace=0.5)

    png_file_name = f"{os.path.splitext(file_name)[0]}_developer.png"
    plt.savefig(png_file_name, bbox_inches='tight', dpi=300)
    logging.info("'developer bar chart' completed.")

# # # # # # # # # # # #
#   PUBLISHER         #
# # # # # # # # # # # #

# counts all the games by publisher
def count_publisher(df):
    logging.info("'count publisher' started.")
    count_publisher = df["Publisher"].value_counts()
    count_publisher.index.name = None
    print("Games by publisher:")
    print(count_publisher.to_string(name=False))
    logging.info("'count publisher' completed.")

# highlight the most common publisher
def most_common_publisher(df):
    logging.info("'most common publisher' started.")
    most_common_publisher = df["Publisher"].mode().iloc[0]
    print(f"The most common publisher is: {most_common_publisher}")
    logging.info("'most common publisher' completed.")

# highlight the least common publisher
def least_common_publisher(df):
    logging.info("'least common publisher' started.")
    least_common_publisher = min(df["Publisher"].unique(), key=df["Publisher"].tolist().count)
    print(f"The least common publisher is: {least_common_publisher}")
    logging.info("'least common publisher' completed.")

# publisher bar chart
def publisher_bar_chart(df, file_name):
    logging.info("'publisher bar chart' started.")

    top_publisher_count = df['Publisher'].value_counts().head(10)
    bottom_publisher_count = df['Publisher'].value_counts().tail(10)

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

    bar_colors_top = sns.color_palette("viridis", len(top_publisher_count))
    bars_top = ax1.bar(top_publisher_count.index, top_publisher_count, color=bar_colors_top)

    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax1.set_title("Top 10 Publishers", fontsize=16, color='white')
    ax1.set_xlabel("Publisher", fontsize=12, color='white')
    ax1.set_ylabel("Games", fontsize=12, color='white')

    ax1.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')

    for bar in bars_top:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    bar_colors_bottom = sns.color_palette("viridis", len(bottom_publisher_count))
    bars_bottom = ax2.bar(bottom_publisher_count.index, bottom_publisher_count, color=bar_colors_bottom)

    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax2.set_title("Bottom 10 Publishers", fontsize=16, color='white')
    ax2.set_xlabel("Publisher", fontsize=12, color='white')
    ax2.set_ylabel("Games", fontsize=12, color='white')

    ax2.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    for bar in bars_bottom:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    plt.subplots_adjust(hspace=0.5)

    png_file_name = f"{os.path.splitext(file_name)[0]}_publisher.png"
    plt.savefig(png_file_name, bbox_inches='tight', dpi=300)
    logging.info("'publisher bar chart' completed.")

# # # # # # # # # # # #
#   GENRE             #
# # # # # # # # # # # #

# counts all the games by genre
def count_genre(df):
    logging.info("'count genre' started.")
    count_genre = df["Genre"].value_counts()
    count_genre.index.name = None
    print("Games by genre:")
    print(count_genre.to_string(name=False))
    logging.info("'count genre' completed.")

# highlight the most common genre
def most_common_genre(df):
    logging.info("'most common genre' started.")
    most_common_genre = df["Genre"].mode().iloc[0]
    print(f"The most common genre is: {most_common_genre}")
    logging.info("'most common genre' completed.")

# highlight the least common genre
def least_common_genre(df):
    logging.info("'least common genre' started.")
    least_common_genre = min(df["Genre"].unique(), key=df["Genre"].tolist().count)
    print(f"The least common genre is: {least_common_genre}")
    logging.info("'least common genre' completed.")

# genre bar chart
def genre_bar_chart(df, file_name):
    logging.info("'genre bar chart' started.")

    top_genre_count = df['Genre'].value_counts().head(10)
    bottom_genre_count = df['Genre'].value_counts().tail(10)

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

    bar_colors_top = sns.color_palette("viridis", len(top_genre_count))
    bars_top = ax1.bar(top_genre_count.index, top_genre_count, color=bar_colors_top)

    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax1.set_title("Top 10 Genre", fontsize=16, color='white')
    ax1.set_xlabel("Genre", fontsize=12, color='white')
    ax1.set_ylabel("Games", fontsize=12, color='white')

    ax1.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax1.tick_params(axis='x', colors='white')
    ax1.tick_params(axis='y', colors='white')

    for bar in bars_top:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    bar_colors_bottom = sns.color_palette("viridis", len(bottom_genre_count))
    bars_bottom = ax2.bar(bottom_genre_count.index, bottom_genre_count, color=bar_colors_bottom)

    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax2.set_title("Bottom 10 Genre", fontsize=16, color='white')
    ax2.set_xlabel("Publisher", fontsize=12, color='white')
    ax2.set_ylabel("Games", fontsize=12, color='white')

    ax2.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    for bar in bars_bottom:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    plt.subplots_adjust(hspace=0.5)

    png_file_name = f"{os.path.splitext(file_name)[0]}_genre.png"
    plt.savefig(png_file_name, bbox_inches='tight', dpi=300)
    logging.info("'genre bar chart' completed.")

# # # # # # # # # # # #
#   AGE RATING        #
# # # # # # # # # # # #

# counts all the games by age rating
def count_age_rating(df):
    logging.info("'count age rating' started.")
    count_age_rating = df["Age Rating"].value_counts()
    count_age_rating.index.name = None
    print("Games by age rating:")
    print(count_age_rating.to_string(name=False))
    logging.info("'count age rating' completed.")

# highlight the most common age rating
def most_common_age_rating(df):
    logging.info("'most common age rating' started.")
    most_common_age_rating = df["Age Rating"].mode().iloc[0]
    print(f"The most common age rating is: {most_common_age_rating}")
    logging.info("'most common age rating' completed.")

# highlight the least common age rating
def least_common_age_rating(df):
    logging.info("'least common age rating' started.")
    least_common_age_rating = min(df["Age Rating"].unique(), key=df["Age Rating"].tolist().count)
    print(f"The least common age rating is: {least_common_age_rating}")
    logging.info("'least common age rating' completed.")

# age rating bar chart
def age_rating_bar_chart(df, file_name):
    logging.info("'age rating bar chart' started.")

    age_rating_count = df['Age Rating'].value_counts()

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_colors = sns.color_palette("viridis", len(age_rating_count))
    bars = ax.bar(age_rating_count.index, age_rating_count, color=bar_colors)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax.set_title("Games by Age Rating", fontsize=16, color='white')
    ax.set_xlabel("Age Rating", fontsize=12, color='white')
    ax.set_ylabel("Games", fontsize=12, color='white')

    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    png_file_name = f"{os.path.splitext(file_name)[0]}_age_rating.png"
    plt.savefig(png_file_name, bbox_inches='tight', dpi=300)
    logging.info("'age rating bar chart' completed.")

# # # # # # # # # # # #
#   PLATFORM          #
# # # # # # # # # # # #

# counts all the games by platform
def count_platform(df):
    logging.info("'count platform' started.")
    count_platform = df["Platform"].value_counts()
    count_platform.index.name = None
    print("Games by platform:")
    print(count_platform.to_string(name=False))
    logging.info("'count platform' completed.")

# highlight the most common platform
def most_common_platform(df):
    logging.info("'most common platform' started.")
    most_common_platform = df["Platform"].mode().iloc[0]
    print(f"The most common platform is: {most_common_platform}")
    logging.info("'most common platform' completed.")

# highlight the least common platform
def least_common_platform(df):
    logging.info("'least common platform' started.")
    least_common_platform = min(df["Platform"].unique(), key=df["Platform"].tolist().count)
    print(f"The least common platform is: {least_common_platform}")
    logging.info("'least common platform' completed.")

# platform bar chart
def platform_bar_chart(df, file_name):
    logging.info("'platform bar chart' started.")

    platform_count = df['Platform'].value_counts()

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))

    bar_colors = sns.color_palette("viridis", len(platform_count))
    bars = ax.bar(platform_count.index, platform_count, color=bar_colors)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha='right')

    ax.set_title("Games by Platform", fontsize=16, color='white')
    ax.set_xlabel("Platform", fontsize=12, color='white')
    ax.set_ylabel("Games", fontsize=12, color='white')

    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f"{yval:.0f}", ha='center', va='bottom', color='white', fontsize=8)

    png_file_name = f"{os.path.splitext(file_name)[0]}_platform.png"
    plt.savefig(png_file_name, bbox_inches='tight', dpi=300)
    logging.info("'platform bar chart' completed.")

# # # # # # # # # # # #
#   END               #
# # # # # # # # # # # #
