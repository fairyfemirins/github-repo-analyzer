#!/usr/bin/env python3
"""
Tests for the GitHub Repository Analyzer
"""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


class TestRepoAnalyzer(unittest.TestCase):
    """Test cases for the GitHub Repository Analyzer."""

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.repo_dir = os.path.join(self.test_dir, "test-repo")
        os.makedirs(self.repo_dir)
        
        # Create test files
        with open(os.path.join(self.repo_dir, "README.md"), "w") as f:
            f.write("# Test Repository")
        with open(os.path.join(self.repo_dir, "LICENSE"), "w") as f:
            f.write("MIT License")
        with open(os.path.join(self.repo_dir, "test.py"), "w") as f:
            f.write("print('Hello, world!')\n")

    def tearDown(self):
        """Clean up the temporary directory."""
        subprocess.run(["rm", "-rf", self.test_dir], check=True)

    def test_analyze_code_quality(self):
        """Test code quality analysis."""
        from src.analyzer import analyze_code_quality
        
        result = analyze_code_quality(self.repo_dir)
        self.assertGreater(result["total_lines"], 0)
        self.assertIn("Python", result["languages"])

    def test_analyze_documentation(self):
        """Test documentation analysis."""
        from src.analyzer import analyze_documentation
        
        result = analyze_documentation(self.repo_dir)
        self.assertTrue(result["readme"])
        self.assertTrue(result["license"])
        self.assertFalse(result["contributing"])

    def test_generate_suggestions(self):
        """Test suggestion generation."""
        from src.analyzer import generate_suggestions
        
        code_quality = {"total_lines": 10, "languages": {"Python": 10}}
        docs = {"readme": True, "license": True, "contributing": False}
        community = {"stars": 5, "forks": 2, "issues": {"open": 1, "total": 1}, "pull_requests": {"open": 0, "total": 0}}
        
        suggestions = generate_suggestions(code_quality, docs, community)
        self.assertGreater(len(suggestions), 0)


if __name__ == "__main__":
    unittest.main()