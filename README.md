## Note
This repository was published under `fairyfemirins` due to GitHub namespace restrictions. A transfer to `femirins` is pending.

An autonomous CLI tool to analyze GitHub repositories for code quality, documentation, and community health.

## Features
- **Code Quality**: Lines of code, language distribution.
- **Documentation**: Checks for `README.md`, `LICENSE`, and `CONTRIBUTING.md`.
- **Community Health**: Stars, forks, issues, and pull requests.
- **Actionable Suggestions**: Recommendations for improvement.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
# Analyze a repository
repo-analyzer owner/repo
```

## Example Output
```
🔍 Analyzing femirins/github-repo-analyzer...

📊 Analysis Results:

📈 Code Quality:
  Total Lines of Code: 150
  Language Distribution:
    Python: 150 lines

📖 Documentation:
  README: ✅
  LICENSE: ✅
  CONTRIBUTING: ❌

👥 Community Health:
  Stars: 0
  Forks: 0
  Issues: 0 open / 0 total
  Pull Requests: 0 open / 0 total

💡 Suggestions:
  ⚠️ Missing CONTRIBUTING.md. Add guidelines for contributors.
  ⚠️ Low stars. Share the project on social media or forums.
```

## License
MIT