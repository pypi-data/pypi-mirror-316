import os
import pytest
from unittest.mock import Mock, patch
from gait.ai_commit import generate_commit_message

def load_sample_diff(filename):
    """Helper function to load sample diff from file"""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    diff_path = os.path.join(tests_dir, 'sample_diffs', filename)
    with open(diff_path, 'r') as f:
        return f.read()

@pytest.fixture
def mock_openai_response():
    mock_message = Mock()
    mock_message.content = "feat: add user authentication"
    
    mock_choice = Mock()
    mock_choice.message = mock_message
    
    mock_response = Mock()
    mock_response.choices = [mock_choice]
    return mock_response

@patch('gait.ai_commit.OpenAI')
def test_generate_commit_message(mock_openai_client, mock_openai_response):
    # Setup mock
    mock_client_instance = Mock()
    mock_client_instance.chat.completions.create.return_value = mock_openai_response
    mock_openai_client.return_value = mock_client_instance

    # Load sample diff from file
    diff_text = load_sample_diff('sample1.txt')  # Replace with your actual filename

    # Execute
    result = generate_commit_message(diff_text)

    # Assert
    assert result == "feat: add user authentication"
    mock_client_instance.chat.completions.create.assert_called_once()

# You can add more test cases using different sample files
@patch('gait.ai_commit.OpenAI')
def test_generate_commit_message_with_different_diff(mock_openai_client, mock_openai_response):
    mock_client_instance = Mock()
    mock_client_instance.chat.completions.create.return_value = mock_openai_response
    mock_openai_client.return_value = mock_client_instance

    # Load a different sample diff
    diff_text = load_sample_diff('sample2.txt')  # Replace with your actual filename

    result = generate_commit_message(diff_text)
    assert result == "feat: add user authentication"
