#!/usr/bin/env python3
"""
Autonomous GitHub Repository Analyzer

Analyzes GitHub repositories for:
- Code quality (LOC, language distribution)
- Documentation quality (README, LICENSE, CONTRIBUTING)
- Community health (stars, forks, issues, PRs)
- Actionable suggestions for improvement
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

import pygount


def run_gh_command(command: List[str]) -> str:
    """Run a GitHub CLI command and return its output."""
    try:
        result = subprocess.run(
            ["gh"] + command,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running 'gh {' '.join(command)}': {e.stderr}", file=sys.stderr)
        sys.exit(1)


def analyze_code_quality(repo_path: str) -> Dict:
    """Analyze code quality using a simple line counter."""
    analysis = {"languages": {}, "total_lines": 0}
    language_extensions = {
        ".py": "Python",
        ".js": "JavaScript",
        ".java": "Java",
        ".c": "C",
        ".cpp": "C++",
        ".go": "Go",
        ".rs": "Rust",
        ".rb": "Ruby",
        ".php": "PHP",
        ".html": "HTML",
        ".css": "CSS",
        ".md": "Markdown",
    }
    
    for file in Path(repo_path).rglob("*"):
        if file.is_file() and not file.name.startswith("."):
            ext = file.suffix.lower()
            if ext in language_extensions:
                language = language_extensions[ext]
                try:
                    with open(file, "r") as f:
                        lines = sum(1 for _ in f)
                    if language not in analysis["languages"]:
                        analysis["languages"][language] = 0
                    analysis["languages"][language] += lines
                    analysis["total_lines"] += lines
                except Exception:
                    continue
    return analysis


def analyze_documentation(repo_path: str) -> Dict:
    """Check for documentation files."""
    docs = {
        "readme": False,
        "license": False,
        "contributing": False,
    }
    for file in Path(repo_path).glob("*"):
        if file.is_file():
            if file.name.lower() in ["readme.md", "readme.txt", "readme"]:
                docs["readme"] = True
            elif file.name.lower() in ["license", "license.md", "license.txt"]:
                docs["license"] = True
            elif file.name.lower() in [
                "contributing.md",
                "contributing.txt",
                "contributing",
            ]:
                docs["contributing"] = True
    return docs


def analyze_community_health(repo: str) -> Dict:
    """Analyze community health using GitHub API."""
    # Fetch repository metadata
    repo_info = json.loads(run_gh_command(["repo", "view", repo, "--json", "stargazersCount,forksCount,issues,pullRequests"]))
    
    # Fetch issues and PRs
    issues = json.loads(run_gh_command(["issue", "list", "--repo", repo, "--json", "number,title,state"]))
    prs = json.loads(run_gh_command(["pr", "list", "--repo", repo, "--json", "number,title,state"]))
    
    return {
        "stars": repo_info["stargazersCount"],
        "forks": repo_info["forksCount"],
        "issues": {
            "total": len(issues),
            "open": sum(1 for issue in issues if issue["state"] == "OPEN"),
        },
        "pull_requests": {
            "total": len(prs),
            "open": sum(1 for pr in prs if pr["state"] == "OPEN"),
        },
    }


def generate_suggestions(code_quality: Dict, docs: Dict, community: Dict) -> List[str]:
    """Generate actionable suggestions for improvement."""
    suggestions = []
    
    # Code quality suggestions
    if code_quality["total_lines"] == 0:
        suggestions.append("❌ No code found. Add source files to the repository.")
    elif code_quality["total_lines"] < 100:
        suggestions.append("⚠️ Small codebase. Consider adding more features or documentation.")
    
    # Documentation suggestions
    if not docs["readme"]:
        suggestions.append("❌ Missing README. Add a README.md to explain the project.")
    if not docs["license"]:
        suggestions.append("❌ Missing LICENSE. Add a license to clarify usage rights.")
    if not docs["contributing"]:
        suggestions.append("⚠️ Missing CONTRIBUTING.md. Add guidelines for contributors.")
    
    # Community health suggestions
    if community["stars"] < 10:
        suggestions.append("⚠️ Low stars. Share the project on social media or forums.")
    if community["issues"]["open"] > 5:
        suggestions.append("⚠️ High open issues. Triage and close stale issues.")
    if community["pull_requests"]["open"] > 3:
        suggestions.append("⚠️ High open PRs. Review and merge pending contributions.")
    
    if not suggestions:
        suggestions.append("✅ Repository looks healthy! Keep up the great work.")
    
    return suggestions


def main():
    parser = argparse.ArgumentParser(description="Autonomous GitHub Repository Analyzer")
    parser.add_argument("repo", help="GitHub repository in format 'owner/repo'")
    parser.add_argument("--clone-dir", help="Directory to clone the repository into", default="/tmp/github-repo-analyzer")
    args = parser.parse_args()
    
    # Clone the repository
    print(f"🔍 Analyzing {args.repo}...")
    run_gh_command(["repo", "clone", args.repo, args.clone_dir])
    
    # Run analyses
    code_quality = analyze_code_quality(args.clone_dir)
    docs = analyze_documentation(args.clone_dir)
    community = analyze_community_health(args.repo)
    
    # Generate suggestions
    suggestions = generate_suggestions(code_quality, docs, community)
    
    # Print results
    print("\n📊 Analysis Results:")
    print("\n📈 Code Quality:")
    print(f"  Total Lines of Code: {code_quality['total_lines']}")
    print("  Language Distribution:")
    for lang, loc in code_quality["languages"].items():
        print(f"    {lang}: {loc} lines")
    
    print("\n📖 Documentation:")
    print(f"  README: {'✅' if docs['readme'] else '❌'}")
    print(f"  LICENSE: {'✅' if docs['license'] else '❌'}")
    print(f"  CONTRIBUTING: {'✅' if docs['contributing'] else '❌'}")
    
    print("\n👥 Community Health:")
    print(f"  Stars: {community['stars']}")
    print(f"  Forks: {community['forks']}")
    print(f"  Issues: {community['issues']['open']} open / {community['issues']['total']} total")
    print(f"  Pull Requests: {community['pull_requests']['open']} open / {community['pull_requests']['total']} total")
    
    print("\n💡 Suggestions:")
    for suggestion in suggestions:
        print(f"  {suggestion}")


if __name__ == "__main__":
    main()