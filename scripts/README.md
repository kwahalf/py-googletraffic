# Scripts 🛠️

Utility scripts for maintaining the **py-googletraffic** project.

## Available Scripts

### generate_contributors.py

Automatically generates `CONTRIBUTORS.md` from git commit history.

**Purpose:** 
- Extract all contributors from git log
- Count commits per contributor
- Generate formatted CONTRIBUTORS.md file
- Support for `.mailmap` to normalize names/emails

**Usage:**

```bash
# Run directly
python scripts/generate_contributors.py

# Or use Makefile
make contributors
```

**Features:**
- ✅ Counts total commits per contributor
- ✅ Detects first contribution date
- ✅ Respects `.mailmap` for name normalization
- ✅ Generates markdown table with statistics
- ✅ Automatically formats with GitHub links when possible

**How it works:**

1. Runs `git shortlog` to get commit counts
2. Uses `git log` to extract contributor details
3. Applies `.mailmap` to normalize duplicate names
4. Generates markdown file with formatted table
5. Adds summary statistics at bottom

**Configuration:**

Edit `.mailmap` in the repository root to normalize contributor names:

```
# Format: Preferred Name <preferred@email> Commit Name <commit@email>
John Doe <john@example.com> johndoe <john@other.com>
```

**Automation:**

This script is run automatically by GitHub Actions on every push to main:
- Workflow: `.github/workflows/update-contributors.yml`
- Auto-commits changes with `[skip ci]` tag
- Keeps CONTRIBUTORS.md always up to date

## Adding New Scripts

When adding new utility scripts:

1. **Name it clearly** - Use descriptive names like `generate_*.py`
2. **Add shebang** - Start with `#!/usr/bin/env python3`
3. **Add docstring** - Explain what it does at the top
4. **Make it executable** - `chmod +x scripts/your_script.py`
5. **Document it here** - Add section above
6. **Add to Makefile** - Create a convenient target if appropriate

## Requirements

These scripts use only Python standard library and git commands. No additional dependencies needed.

## Testing Scripts Locally

Before committing changes to scripts:

```bash
# Test the script
python scripts/your_script.py

# Check for syntax errors
python3 -m py_compile scripts/your_script.py

# Make sure it's executable
chmod +x scripts/your_script.py

# Test from any directory
cd /tmp
python /path/to/py-googletraffic/scripts/your_script.py
```

## Contributing

Have an idea for a useful script? We'd love to include it!

1. Create the script in `scripts/`
2. Test it thoroughly
3. Document it in this README
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

---

For questions about these scripts, [open an issue](https://github.com/yourusername/py-googletraffic/issues).
