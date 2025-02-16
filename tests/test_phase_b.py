from app.phase_b_tasks import *

# test script to test each function in app/phase_b_tasks.py

# test fetch_and_save_data()
def test_fetch_and_save_data():
    api_url = "https://catfact.ninja/fact"
    output_file_path = "test_data/api_data.json"

    assert fetch_and_save_data(api_url, output_file_path) == True

    # Test with an incorrect email
    incorrect_api_url = "https://rat.ninja/incorrect"
    assert fetch_and_save_data(incorrect_api_url, output_file_path) == False

# test clone_and_commit()
def test_clone_and_commit():
    repo_url = "https://github.com/danielrayappa2210/TDS-GA2.git"
    clone_to_path = "test_data/repo"
    commit_message = "Test commit"
    file_to_modify = "README.md"
    modification_content = "test sentence"

    assert clone_and_commit(repo_url, clone_to_path, commit_message, file_to_modify, modification_content) == True

    # Test with an incorrect repo URL
    incorrect_repo_url = "https://github.com/example"
    clone_to_path = "test_data/repo1"
    assert clone_and_commit(incorrect_repo_url, clone_to_path, commit_message, file_to_modify, modification_content) == False

# test extract_web_data()
def test_extract_web_data():
    url = "https://en.wikipedia.org/wiki/Demographics_of_India"
    output_file_path = "test_data/output.csv"

    assert extract_web_data(url, output_file_path=output_file_path) == True

    url = "https://example.com"
    output_file_path = "test_data/output.csv"

    assert extract_web_data(url, output_file_path=output_file_path) == False

# test compress_image()
def test_compress_image():
    input_path = "test_data/input.jpg"
    output_path = "test_data/output.jpg"

    assert compress_image(input_path, output_path) == True

    input_path = "test_data/input1.jpg"
    output_path = "test_data/output1.jpg"

    assert compress_image(input_path, output_path) == False

# test markdown_to_html()
def test_markdown_to_html():
    # Check when input file is present
    input_file_path = "test_data/docs/f1.md"
    output_file_path = "test_data/docs/output.html"

    # Check when input file is present
    assert markdown_to_html(input_file_path, output_file_path) == True

    # Check when input file is not present
    input_file_path = "test_data/docs/f0.md"
    output_file_path = "test_data/docs/output.html"

    # Check when input file is present
    assert markdown_to_html(input_file_path, output_file_path) == False