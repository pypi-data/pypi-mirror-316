import pytest
from unittest.mock import patch, MagicMock
import subprocess
from gait.github_wrapper import (
    check_gh_auth,
    guide_auth,
    create_pull_request,
    handle_pr_command
)

# Fixtures
@pytest.fixture
def mock_subprocess():
    with patch('subprocess.run') as mock_run:
        yield mock_run

@pytest.fixture
def mock_print():
    with patch('builtins.print') as mock_print:
        yield mock_print

# Test check_gh_auth
def test_check_gh_auth_success(mock_subprocess):
    mock_subprocess.return_value = MagicMock(returncode=0, stdout="Logged in")
    status, message = check_gh_auth()
    assert status is True
    assert message == "Logged in"

def test_check_gh_auth_not_installed(mock_subprocess):
    mock_subprocess.side_effect = FileNotFoundError()
    status, message = check_gh_auth()
    assert status is False
    assert "not installed" in message

def test_check_gh_auth_not_authenticated(mock_subprocess):
    mock_subprocess.return_value = MagicMock(returncode=1, stdout="Not logged in")
    status, message = check_gh_auth()
    assert status is False
    assert message == "Not logged in"

# Test guide_auth
def test_guide_auth_success(mock_subprocess, mock_print):
    mock_subprocess.return_value = MagicMock(returncode=0)
    assert guide_auth() is True
    mock_print.assert_called_with("\nStarting GitHub authentication process...")

def test_guide_auth_failure(mock_subprocess, mock_print):
    mock_subprocess.side_effect = subprocess.CalledProcessError(1, "gh auth login")
    assert guide_auth() is False
    assert mock_print.call_count == 2  # Starting message + error message

# Test create_pull_request
@pytest.fixture
def mock_auth_check():
    with patch('gait.github_wrapper.check_gh_auth') as mock:
        mock.return_value = (True, "Authenticated")
        yield mock

@pytest.fixture
def mock_input():
    with patch('builtins.input') as mock:
        mock.return_value = 'e'  # 默认模拟用户输入 'e'
        yield mock

def test_create_pr_success(mock_subprocess, mock_auth_check, mock_input):
    mock_subprocess.return_value = MagicMock(
        returncode=0,
        stdout="https://github.com/org/repo/pull/1"
    )
    
    success, message = create_pull_request(
        title="Test PR",
        body="Test body"
    )
    
    assert success is True
    assert "Successfully created PR" in message
    
    # 验证命令构造正确
    mock_subprocess.assert_called_once()
    cmd = mock_subprocess.call_args[0][0]
    assert cmd == ["gh", "pr", "create", "-t", "Test PR", "-b", "Test body"]

def test_create_pr_with_additional_args(mock_subprocess, mock_auth_check, mock_input):
    mock_subprocess.return_value = MagicMock(returncode=0)
    
    create_pull_request(
        title="Test PR",
        body="Test body",
        additional_args=["--draft"]
    )
    
    cmd = mock_subprocess.call_args[0][0]
    assert cmd == ["gh", "pr", "create", "-t", "Test PR", "-b", "Test body", "--draft"]

def test_create_pr_user_cancels(mock_subprocess, mock_auth_check, mock_input):
    # 模拟用户取消
    mock_input.return_value = 'n'
    
    success, message = create_pull_request(
        title="Test PR",
        body="Test body"
    )
    
    assert success is False
    assert "cancelled by user" in message
    mock_subprocess.assert_not_called()

def test_create_pr_command_failure(mock_subprocess, mock_auth_check, mock_input):
    mock_subprocess.return_value = MagicMock(
        returncode=1,
        stderr="Error: invalid title"
    )
    
    success, message = create_pull_request(
        title="Test PR",
        body="Test body"
    )
    
    assert success is False
    assert "Failed to create PR" in message

def test_create_pr_no_preview(mock_subprocess, mock_auth_check):
    # 测试不显示预览的情况
    mock_subprocess.return_value = MagicMock(returncode=0)
    
    create_pull_request(
        title="Test PR",
        body="Test body",
        preview=False  # 跳过预览确认
    )
    
    # 验证直接创建了 PR，没有请求用户输入
    cmd = mock_subprocess.call_args[0][0]
    assert cmd == ["gh", "pr", "create", "-t", "Test PR", "-b", "Test body"]

# Test handle_pr_command
def test_handle_pr_command_success(mock_subprocess, mock_auth_check):
    mock_subprocess.return_value = MagicMock(
        returncode=0,
        stdout="PR created successfully"
    )
    
    result = handle_pr_command(["create", "--title", "Test"])
    
    assert result == 0
    mock_subprocess.assert_called_with(
        ["gh", "pr", "create", "--title", "Test"],
        check=True,
        stdout=-1,  # subprocess.PIPE
        stderr=-1,  # subprocess.PIPE
        text=True
    )

def test_handle_pr_command_not_installed(mock_subprocess, mock_print):
    mock_subprocess.side_effect = FileNotFoundError()
    
    result = handle_pr_command(["list"])
    
    assert result == 1
    assert any("not installed" in str(call) for call in mock_print.call_args_list)

def test_handle_pr_command_error(mock_subprocess, mock_auth_check):
    error = subprocess.CalledProcessError(1, "gh pr create")
    error.stderr = "Error creating PR"
    mock_subprocess.side_effect = error
    
    result = handle_pr_command(["create"])
    
    assert result == 1
