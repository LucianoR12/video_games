import video_games as vg

import pandas as pd
import sys
from io import StringIO
import os
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import ast

def run_video_games_access(file_name):
    try:
        log_file_path = vg.get_file_path(file_name, "log")
        txt_file_path = vg.get_file_path(file_name, "txt")
        png_file_path = vg.get_file_path(file_name, "png")
        xlsx_file_path = vg.get_file_path(file_name, "xlsx")
        csv_file_path = vg.get_file_path(file_name, "csv")

        vg.setup_logging(log_file_path)
        logging.info("'video games access' script started.")

        vg.check_csv_file(file_name)
        df, output_file, output_buffer = vg.start_process_csv_file(file_name)
        vg.columns_validation(df)

        # vg.print_info(df)
        # vg.print_description(df)
        # vg.print_first_row(df)

        vg.rename_column(df)        
        vg.clean_age_rating(df)
        vg.extract_platform_info(df)
        vg.check_missing_values(df)
        vg.remove_duplicates(df)
        vg.remove_columns(df)
        # vg.remove_rows(df)
        vg.reset_index(df)

        cleaned_csv = vg.get_file_path(f"{os.path.splitext(file_name)[0]}_cleaned", "csv")
        df.to_csv(cleaned_csv, index=False)

        cleaned_xlsx = vg.get_file_path(f"{os.path.splitext(file_name)[0]}_cleaned", "xlsx")
        df.to_excel(cleaned_xlsx, index=False)

        vg.count_release_date(df)
        vg.most_common_release_date(df)
        vg.least_common_release_date(df)
        vg.release_date_year_bar_chart(df, file_name)
        vg.release_date_month_line_chart(df, file_name)

        vg.count_developer(df)
        vg.most_common_developer(df)
        vg.least_common_developer(df)
        vg.developer_bar_chart(df, file_name)

        vg.count_publisher(df)
        vg.most_common_publisher(df)
        vg.least_common_publisher(df)
        vg.publisher_bar_chart(df, file_name)

        vg.count_genre(df)
        vg.most_common_genre(df)
        vg.least_common_genre(df)
        vg.genre_bar_chart(df, file_name)

        vg.count_age_rating(df)
        vg.most_common_age_rating(df)
        vg.least_common_age_rating(df)
        vg.age_rating_bar_chart(df, file_name)

        vg.count_platform(df)
        vg.most_common_platform(df)
        vg.least_common_platform(df)
        vg.platform_bar_chart(df, file_name)

        cleaned_df = df.copy()
        return cleaned_df

    except Exception as e:
        logging.error(f"An unexpected {type(e).__name__} error occurred: {e}")
        sys.exit(1)

    finally:
        vg.end_process_csv_file(output_file, output_buffer)

    logging.info("'video games access' script completed.")

    log_file_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(log_file_path))
    os.replace(log_file_path, log_file_destination)

    txt_file_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(txt_file_path))
    os.replace(txt_file_path, txt_file_destination)

    png_file_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(png_file_path))
    os.replace(png_file_path, png_file_destination)

    xlsx_file_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(xlsx_file_path))
    os.replace(xlsx_file_path, xlsx_file_destination)

    csv_file_destination = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.basename(csv_file_path))
    os.replace(csv_file_path, csv_file_destination)

if __name__ == "__main__":
    file_name = input("Enter the file name (including extension): ")
    run_video_games_access(file_name)