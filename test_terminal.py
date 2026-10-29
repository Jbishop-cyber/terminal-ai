import unittest
from unittest.mock import patch

from terminal import run_command


class TestRunCommand(unittest.TestCase):

    @patch("terminal.subprocess.run")
    def test_safe_command_runs_without_confirmation(self, mock_run):
        mock_run.return_value.stdout = "Jay is working"
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0

        with patch("builtins.input") as mock_input:
            result = run_command(["echo", "Jay is working"])

        self.assertEqual(result, "Jay is working")
        mock_input.assert_not_called()
        mock_run.assert_called_once()

    @patch("terminal.subprocess.run")
    @patch("terminal.user_choice", return_value=False)
    def test_dangerous_command_can_be_cancelled(
        self, mock_choice, mock_run
    ):
        result = run_command(["sudo", "rm", "text.txt"])

        self.assertEqual(result, "Command cancelled.")
        mock_choice.assert_called_once()
        mock_run.assert_not_called()

    @patch("terminal.subprocess.run")
    @patch("terminal.user_choice", return_value=True)
    def test_dangerous_command_runs_after_confirmation(
        self, mock_choice, mock_run
    ):
        mock_run.return_value.stdout = ""
        mock_run.return_value.stderr = ""
        mock_run.return_value.returncode = 0

        result = run_command(["sudo", "rm", "text.txt"])

        self.assertEqual(result, "")
        mock_choice.assert_called_once()
        mock_run.assert_called_once()


if __name__ == "__main__":
    unittest.main()