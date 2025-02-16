# test script to test each function in app/phase_a_tasks.py

from app.phase_a_tasks import *
import tempfile
import os
import random
import glob

# test the format_markdown_file()
def test_format_markdown_file():
    # create a temporary .md file for testing the true condition
    with open("test_data/format.md", 'r') as temp_file:
        temp_file_path = temp_file.name

    # test if the function returns True when the file exists
    assert format_markdown_file(temp_file_path) == True

    # test if the function returns False when the file does not exist
    assert format_markdown_file("tests/test2.md") == False

# test the count_specific_days()
def test_count_specific_days():
    # read the dates.txt file from test_data for testing the true condition
    with open("test_data/dates.txt", 'r') as temp_file:
        temp_file_path = temp_file.name

    # test if the function returns True when the file exists
    assert count_specific_days(temp_file_path, "monday", temp_file_path) == True

    # test if the function returns False when the file does not exist
    assert count_specific_days("tests/test2.txt", "monday", "tests/test2.txt") == False

    # read the dates.txt file from test_data for testing the false condition
    with open("test_data/dates.txt", 'r') as temp_file:
        temp_file_path = temp_file.name

    # test if the function returns None when the day_of_week is invalid
    assert count_specific_days(temp_file_path, "invalid", temp_file_path) == None

# test the sort_contacts()
def test_sort_contacts():
    # read the contacts.json file from test_data for testing the true condition
    with open("test_data/contacts.json", 'r') as temp_file:
        temp_file_path = temp_file.name

    # test if the function returns True when the file exists
    assert sort_contacts(temp_file_path, temp_file_path) == True

    # test if the function returns False when the file does not exist
    assert sort_contacts("tests/test2.json", "tests/test2.json") == False

# test the read_log_files()
def test_read_log_files():
    # test if the function returns True when the directory contains .log files
    assert read_log_files("test_data/logs", 1, "test_data/recent-log.txt") == True

    # test if the function returns False when the directory does not contain .log files
    assert read_log_files("tests", 2, "tests/output.txt") == False

# test the extract_h1_headings()
def test_extract_h1_headings():
    # test if the function returns True when the directory contains .md files
    assert extract_h1_headings("test_data/docs", "test_data/docs/index.json") == True

    # test if the function returns False when the directory does not contain .md files
    assert extract_h1_headings("tests", "tests/test.json") == False

# test email_extractor()
def test_extract_email_sender():
    # read the email.txt file from test_data for testing the true condition
    with open("test_data/email.txt", 'r') as temp_file:
        temp_file_path = temp_file.name

    output_file_path = "test_data/email-sender.txt"

    # test if the function returns True when the file exists
    assert extract_email_sender(temp_file_path, output_file_path) == True

    # test if the function returns False when the file does not exist
    assert extract_email_sender("tests/test2.txt", output_file_path) == False

# test the extract_card_numbers()
def test_extract_numbers_from_image():
    # get a list of all images in the images_test_data folder
    image_files = glob.glob("images_test_data/*")

    # filter the image files to include only image1 to image4
    image_files = [img for img in image_files if os.path.basename(img) in ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg"]]
    # select a random image file
    image_file_path = random.choice(image_files)

    output_file_path = "test_data/credit-card.txt"

    # test if the function returns True when the image file exists
    assert extract_numbers_from_image(image_file_path, output_file_path) == True

    # test if the function returns False when the image does not contain a card number
    assert extract_numbers_from_image("images_test_data/image5.jpg", output_file_path) == False

    # test if the function returns False when the image file does not exist
    assert extract_numbers_from_image("tests/test_image.jpg", output_file_path) == False

# test the find_similar_comments()
def test_find_similar_comments():
    input_file_path = "test_data/comments.txt"
    output_file_path = "test_data/comments-similar.txt"

    # test if the function returns True when the file exists
    assert find_similar_comments(input_file_path, output_file_path) == True

    # test if the function returns False when the file does not exist
    assert find_similar_comments("tests/test2.txt", output_file_path) == False

# test read_db_file()
def test_read_db_file():
    # read the .db in db_test_data
    db_file = "db_test_data/tickets.db"

    output_file_path = "test_data/ticket-sales-gold.txt"

    # test the function with query that returns True
    assert read_db_file(db_file, output_file_path, "SELECT * FROM tickets") == True

    # test the function without query that returns False
    assert read_db_file(db_file, output_file_path) == False

    # test the function with no file that returns False
    assert read_db_file("tests/test2.db", output_file_path, "SELECT * FROM tickets") == False
