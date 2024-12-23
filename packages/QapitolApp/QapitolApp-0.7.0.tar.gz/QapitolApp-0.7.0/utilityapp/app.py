import os
import logging
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import atexit
import pg8000
from . import app

'''
Task:
0. Add " please upload in correct format or download from here " in index page -- DONE
1. Log file will not be cleaned up . Create a folder where for each activation different files will be created --> We will clean it up after 30 days 
2. Don't delete the uploaded files , move it to "archive" folder --> Which will also be cleaned up after 30 days 
3. Add algorithm for deleting log files in 30 days .
4. Add readme file  . 
5. add checks to check the data of the column 
6. How to make it distributable - IMP - Wheel package 
7. Client name validation  -- DONE
8. Remove done.html . Add success pop up and refresh button --DONE

FRONT END --
1. Qap logo top left corner 
2. copyright right cornor below
3. "dashboard util" - Upload file 
4. remove home , done from index page 
5. center - Left allignment and put in a box 
6. client drop down should be below choose file button 
7. Color - Blue 
8. font - popins 
9. current file - left , delete button below that , change the done button name to process 

BACK END-- 
1. Fix delete button - in case of correct upload , delete button is broken -- DONE
2. Remove error message from the screen 
'''

app = Flask(__name__)

# Folders
UPLOAD_FOLDER = 'uploads'
ARCHIVE_FOLDER = 'archive'  # Folder for archived files
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(ARCHIVE_FOLDER):
    os.makedirs(ARCHIVE_FOLDER)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setting up logging to both file and console
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler to log to app.log file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)  # File logs at INFO or higher
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Stream handler to log to console (command prompt)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Helper function to check allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to clean up the file once your job is finished
def cleanup_file(filename):
    """Helper function to delete the uploaded file after processing."""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File {filename} has been deleted.")
        else:
            logger.warning(f"File {filename} does not exist.")
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {e}")

# Helper function to archive file
def archive_file(filename):
    """Move the file to the archive folder."""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        archive_path = os.path.join(ARCHIVE_FOLDER, filename)
        if os.path.exists(file_path):
            os.rename(file_path, archive_path)
            logger.info(f"File {filename} moved to archive.")
        else:
            logger.warning(f"File {filename} not found in uploads.")
    except Exception as e:
        logger.error(f"Error archiving file {filename}: {e}")

# Function to clean the log file
def clear_log_file():
    """Clears the app.log file at the end of the session."""
    try:
        with open('app.log', 'w'):  
            pass  # No need to write anything, just clearing the file
        logger.info("Log file has been cleared.")
    except Exception as e:
        logger.error(f"Error clearing the log file: {e}")

# Register the clear_log_file function to be called when the app shuts down
atexit.register(clear_log_file)

# Main route to upload and process files
@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    error_message = None
    file_data = None

    logger.info("Request received at / route")

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            logger.info(f"File {filename} uploaded successfully.")

            try:
                df = pd.read_excel(file_path)
                logger.info("File read successfully")

                col1_data = df.iloc[:, 0].tolist()
                col2_data = df.iloc[:, 1].tolist() if df.shape[1] > 1 else []

                # Based on the length of the excel file col - should be dynamic not hardcoded 
                file_data = {
                    'col1': col1_data,
                    'col2': col2_data,
                    'columns': df.columns.tolist()
                }

                logger.info(f"File {filename} processed successfully. Columns: {df.columns.tolist()}")

                # DATABASE CONNECTION AND INSERTION
                db_config = {
                    'host': 'localhost',      # Database server address
                    'port': 5432,             # Default port for PostgreSQL
                    'user': 'postgres',       # Your PostgreSQL username
                    'password': 'Admin@123',  # Your PostgreSQL password
                    'database': 'Dummy'       # The name of the database
                }

                # Connect to the PostgreSQL database using pg8000
                conn = pg8000.connect(
                    user=db_config['user'],
                    password=db_config['password'],
                    host=db_config['host'],
                    port=db_config['port'],
                    database=db_config['database']
                )
                # Create a cursor to interact with the database
                cursor = conn.cursor()

                # Define the table name
                table_name = 'test_data'  

                # Create the insert query
                insert_query = f"""
                    INSERT INTO {table_name} ({', '.join(file_data['columns'])})
                    VALUES (%s, %s)
                """

                # Prepare the data for insertion
                insert_values = list(zip(file_data['col1'], file_data['col2']))

                # Insert each row into the table
                for row in insert_values:
                    cursor.execute(insert_query, row)

                # Commit the transaction
                conn.commit()
                logger.info("Data inserted successfully!")

                # Cleanup the file after processing
                archive_file(filename)

            except Exception as e:
                error_message = f"Error reading the file: {str(e)}"
                logger.error(f"Error reading file {filename}: {e}")

        else:
            error_message = "This format is not supported, please upload the correct format."
            logger.warning(f"Unsupported file format uploaded: {file.filename}")

    return render_template('index.html', filename=filename, error_message=error_message, file_data=file_data)

# Route to delete a file manually (e.g., from UI)
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Check if the file exists before trying to delete
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"File {filename} deleted manually.")
        else:
            logger.warning(f"File {filename} does not exist.")
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {e}")
        return str(e)

# Route for cleanup: Delete the file after processing
@app.route('/cleanup', methods=['POST'])
def cleanup():
    # Retrieve the filename from the session (or wherever the file info is stored)
    filename = session.get('filename', None)

    if filename:
        # Clean up the file
        cleanup_file(filename)

        # Clear session data related to the uploaded file
        session.pop('filename', None)
        session.pop('col1', None)
        session.pop('col2', None)

        logger.info(f"File {filename} has been cleaned up.")  # Log cleanup
        return render_template('done.html', message="File has been deleted and activities are completed.")
    else:
        logger.warning("No file to clean up.")  # Log if no file to clean up
        return render_template('done.html', message="No file to clean up.")


def main():
    app.run(debug=True)

main()