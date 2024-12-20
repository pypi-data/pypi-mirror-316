import pytest
from unittest.mock import patch, MagicMock
from gait.ai_pr import get_branch_changes, generate_pr_content, handle_ai_pr

# 测试 get_branch_changes
@pytest.fixture
def mock_subprocess_run():
    with patch('subprocess.run') as mock_run:
        # 模拟git命令返回
        mock_run.side_effect = [
            MagicMock(stdout='main'),  # 模拟分支名
            MagicMock(stdout='mock diff'),  # 模拟diff
            MagicMock(stdout='commit1\ncommit2')  # 模拟commit消息
        ]
        yield mock_run

def test_get_branch_changes(mock_subprocess_run):
    diff, commits = get_branch_changes()
    assert diff == 'mock diff'
    assert commits == 'commit1\ncommit2'

# 测试 generate_pr_content
@pytest.fixture
def mock_openai_response():
    with patch('openai.ChatCompletion.create') as mock_create:
        mock_create.return_value = MagicMock(
            choices=[
                MagicMock(
                    message={'content': 'TITLE: Test PR\nBODY: Test body content'}
                )
            ]
        )
        yield mock_create

def test_generate_pr_content(mock_openai_response):
    title, body = generate_pr_content('test diff', 'test commits')
    assert title == 'Test PR'
    assert body == 'Test body content'

# 测试 handle_ai_pr
@pytest.fixture
def mock_all_dependencies():
    with patch('gait.ai_pr.get_branch_changes') as mock_changes, \
         patch('gait.ai_pr.generate_pr_content') as mock_generate, \
         patch('gait.ai_pr.create_pull_request') as mock_create, \
         patch('builtins.input') as mock_input:
        
        mock_changes.return_value = ('diff', 'commits')
        mock_generate.return_value = ('PR Title', 'PR Body')
        mock_create.return_value = (True, 'Success')
        mock_input.return_value = 'y'
        
        yield {
            'changes': mock_changes,
            'generate': mock_generate,
            'create': mock_create,
            'input': mock_input
        }

def test_handle_ai_pr_success(mock_all_dependencies):
    result = handle_ai_pr()
    assert result == 0
