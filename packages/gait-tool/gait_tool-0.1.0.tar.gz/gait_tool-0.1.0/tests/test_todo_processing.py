import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.gait.ai_pr import process_todos
import subprocess

class TestProcessTodos(unittest.TestCase):
    def setUp(self):
        self.sample_diff = """diff --git a/src/example.py b/src/example.py
--- a/src/example.py
+++ b/src/example.py
@@ -10,6 +10,7 @@ class Example:
     def some_method():
+        # TODO: Implement error handling
+        # TODO(ENG-123): Existing ticket
+        # TODO: Add validation
+        # TODO : still valid TODO
+        # TODO(some_context): still valid TODO
+        # TODO (some_context): still valid TODO
         pass"""

    @patch('src.gait.ai_pr.LinearClient')
    @patch('builtins.open', new_callable=mock_open)
    @patch('subprocess.run')
    def test_process_todos(self, mock_subprocess, mock_file, mock_linear_client):
        # Setup LinearClient mock
        mock_instance = mock_linear_client.return_value
        mock_instance.create_issue.side_effect = ['ABC-456', 'ABC-789', 'ABC-101', 'ABC-102', 'ABC-103']
        
        # Setup file content mock
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            '        # TODO: Implement error handling\n',
            '        # TODO(ENG-123): Existing ticket\n',
            '        # TODO: Add validation\n',
            '        # TODO : still valid TODO\n',
            '        # TODO(some_context): still valid TODO\n',
            '        # TODO (some_context): still valid TODO\n'
        ]
        mock_file.return_value.__enter__.return_value.read.return_value = '\n'.join([
            '        # TODO(ABC-456): Implement error handling',
            '        # TODO(ENG-123): Existing ticket',
            '        # TODO(ABC-789): Add validation',
            '        # TODO(ABC-101): still valid TODO',
            '        # TODO(ABC-102): still valid TODO',
            '        # TODO(ABC-103): still valid TODO'
        ])

        # Run the function
        updated_diff, todos = process_todos(self.sample_diff, test_mode=False)
        
        # Verify LinearClient was initialized
        mock_linear_client.assert_called_once()
        
        # Verify Linear issues were created for new TODOs
        self.assertEqual(mock_instance.create_issue.call_count, 5)
        mock_instance.create_issue.assert_any_call(
            title='Implement error handling',
            file_path='src/example.py',
            context=None
        )
        mock_instance.create_issue.assert_any_call(
            title='Add validation',
            file_path='src/example.py',
            context=None
        )
        mock_instance.create_issue.assert_any_call(
            title='still valid TODO',
            file_path='src/example.py',
            context=None
        )
        mock_instance.create_issue.assert_any_call(
            title='still valid TODO',
            file_path='src/example.py',
            context='some_context'
        )
        mock_instance.create_issue.assert_any_call(
            title='still valid TODO',
            file_path='src/example.py',
            context='some_context'
        )
        
        # Verify file was updated
        mock_file.assert_called()
        handle = mock_file()
        
        # Verify git commands were called
        mock_subprocess.assert_any_call(['git', 'add', 'src/example.py'], check=True)
        mock_subprocess.assert_any_call(
            ['git', 'commit', '-m', 
             'Update TODO references with Linear ticket IDs\n\nUpdated 5 TODOs in src/example.py'],
            check=True
        )
        mock_subprocess.assert_any_call(['git', 'push'], check=True)
        
        # Verify todos were collected correctly
        self.assertEqual(len(todos), 6)
        
        # Verify existing ticket was not modified
        self.assertTrue(any(todo[2] == 'ENG-123' for todo in todos))
        
        # Verify new tickets were created and added
        self.assertTrue(any(todo[2] == 'ABC-456' for todo in todos))
        self.assertTrue(any(todo[2] == 'ABC-789' for todo in todos))
        self.assertTrue(any(todo[2] == 'ABC-101' for todo in todos))
        self.assertTrue(any(todo[2] == 'ABC-102' for todo in todos))
        self.assertTrue(any(todo[2] == 'ABC-103' for todo in todos))
        
        # Verify updated diff contains new ticket references
        self.assertIn('TODO(ABC-456): Implement error handling', updated_diff)
        self.assertIn('TODO(ENG-123): Existing ticket', updated_diff)
        self.assertIn('TODO(ABC-789): Add validation', updated_diff)
        self.assertIn('TODO(ABC-101): still valid TODO', updated_diff)
        self.assertIn('TODO(ABC-102): still valid TODO', updated_diff)
        self.assertIn('TODO(ABC-103): still valid TODO', updated_diff)

    @patch('src.gait.ai_pr.LinearClient')
    def test_process_todos_test_mode(self, mock_linear_client):
        # Run in test mode
        updated_diff, todos = process_todos(self.sample_diff, test_mode=True)
        
        # Verify LinearClient was NOT initialized in test mode
        mock_linear_client.assert_not_called()
        
        # Verify todos were collected
        self.assertIsNotNone(todos)
        self.assertEqual(len(todos), 6)
        
        # Verify todos maintain their original form
        expected_todos = [
            ('src/example.py', '+        # TODO: Implement error handling', None, 'Implement error handling'),
            ('src/example.py', '+        # TODO(ENG-123): Existing ticket', 'ENG-123', 'Existing ticket'),
            ('src/example.py', '+        # TODO: Add validation', None, 'Add validation'),
            ('src/example.py', '+        # TODO : still valid TODO', None, 'still valid TODO'),
            ('src/example.py', '+        # TODO(some_context): still valid TODO', 'some_context', 'still valid TODO'),
            ('src/example.py', '+        # TODO (some_context): still valid TODO', 'some_context', 'still valid TODO')
        ]
        self.assertEqual(todos, expected_todos)
        
        # Original diff should remain unchanged in test mode
        self.assertEqual(updated_diff, self.sample_diff)

    @patch('src.gait.ai_pr.LinearClient')
    def test_process_todos_linear_client_failure(self, mock_linear_client):
        # Setup LinearClient to fail
        mock_linear_client.side_effect = ValueError("Linear client initialization failed")
        
        # Run the function
        updated_diff, todos = process_todos(self.sample_diff)
        
        # Should return the original diff and None for todos when Linear client fails
        self.assertEqual(updated_diff, self.sample_diff)
        self.assertIsNone(todos)

    def test_process_todos_invalid_diff(self):
        invalid_diff = """diff --git a/src/example.py b/src/example.py
--- a/src/example.py
+++ b/src/example.py
@@ -1,1 +1,2 @@
+        # todo: lowercase not matched
+        print("TODO: not a comment")
+        # TODO no semicolon
+        # this TODO: is not matched
+        print("TODO: not a comment")
"""
        # Run the function
        updated_diff, todos = process_todos(invalid_diff)
        
        # Verify no todos were found
        self.assertEqual(len(todos), 0)
        
        # Diff should remain unchanged
        self.assertEqual(updated_diff, invalid_diff)

    def test_process_todos_different_comment_styles(self):
        diff_with_different_comments = """diff --git a/src/example.py b/src/example.py
--- a/src/example.py
+++ b/src/example.py
@@ -1,1 +1,3 @@
+        # TODO: Python style comment
+        // TODO: JavaScript style comment
+        /* TODO: C style comment */"""
        
        # Run in test mode to avoid actual Linear API calls
        updated_diff, todos = process_todos(diff_with_different_comments, test_mode=True)
        
        # Verify all comment styles are detected
        self.assertEqual(len(todos), 3, "Should detect all three TODO styles")
        
        # Verify each comment style is correctly captured
        todo_comments = [todo[3] for todo in todos]
        expected_comments = [
            'Python style comment',
            'JavaScript style comment',
            'C style comment'
        ]
        
        # Check if all expected comments are present
        for expected in expected_comments:
            self.assertTrue(
                any(expected in comment for comment in todo_comments),
                f"Missing TODO comment: {expected}"
            )
        
        # Verify file paths are correct
        self.assertTrue(all(todo[0] == 'src/example.py' for todo in todos))
        
        # Verify none have issue IDs (test mode)
        self.assertTrue(all(todo[2] is None for todo in todos))

    @patch('builtins.open', new_callable=mock_open)
    def test_process_removed_todos(self, mock_file):
        # Diff with removed TODOs
        diff_with_removed = """diff --git a/src/example.py b/src/example.py
--- a/src/example.py
+++ b/src/example.py
@@ -1,3 +1,2 @@
-        # TODO(ENG-123): This will be removed
-        # TODO(PRO-456): Another removed todo
+        # TODO: New todo
         pass"""

        # Setup file content mock
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            '        # TODO: New todo\n',
        ]
        mock_file.return_value.__enter__.return_value.read.return_value = '\n'.join([
            '        # TODO(ABC-789): New todo',
        ])

        with patch('src.gait.ai_pr.LinearClient') as mock_linear_client:
            # Setup LinearClient mock
            mock_instance = mock_linear_client.return_value
            mock_instance.create_issue.return_value = 'ABC-789'
            mock_instance.complete_issue.side_effect = [True, True]
            
            # Run the function
            updated_diff, todos = process_todos(diff_with_removed)
            
            # Verify LinearClient was initialized
            mock_linear_client.assert_called_once()
            
            # Verify complete_issue was called for removed TODOs
            mock_instance.complete_issue.assert_any_call('ENG-123')
            mock_instance.complete_issue.assert_any_call('PRO-456')
            self.assertEqual(mock_instance.complete_issue.call_count, 2)
            
            # Verify new TODO was processed
            mock_instance.create_issue.assert_called_once()
            self.assertIsNotNone(todos)
            self.assertEqual(len(todos), 1)
            
            # Verify diff still contains the removal lines
            self.assertIn('-        # TODO(ENG-123): This will be removed', updated_diff)
            self.assertIn('-        # TODO(PRO-456): Another removed todo', updated_diff)
