
# **Inspyctor**  
*Your intelligent Python code reviewer and analyzer.*

[![PyPI version](https://badge.fury.io/py/inspyctor.svg)](https://badge.fury.io/py/inspyctor)  
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## **Overview**
**Inspyctor** is a Python package that helps developers improve their code quality by combining static analysis tools and free AI models. It provides actionable feedback on code style, security vulnerabilities, and best practices while offering intelligent suggestions for improvement.

---

## **Features**
- 🚀 **Static Analysis**:
  - Style checking with **Flake8**.
  - Security checks using **Bandit**.
- 🤖 **AI-Powered Suggestions**:
  - Provides free AI-based insights using Hugging Face models.
- 🛠️ **Comprehensive Feedback**:
  - Combines results from multiple tools in an easy-to-read format.
- 💸 **Free and Open Source**:
  - Uses open-source models and tools, making it entirely free to use.

---

## **Installation**

Install **inspyctor** using pip:

```bash
pip install inspyctor
```

---

## **Usage**

### **Command-Line Interface** *(if implemented)*:
Run the following command in your terminal:

```bash
inspyctor review <file_path>
```

### **Python API**:
Use the package directly in your Python scripts:

```python
from inspyctor import review_code

file_path = "example.py"
feedback = review_code(file_path)

for category, result in feedback.items():
    print(f"\n{category}:\n{result}")
```

---

## **Example Output**

When you review a Python file, **inspyctor** generates feedback like this:

```
Style Issues:
example.py:10:1: W293 blank line contains whitespace

Security Issues:
No issues found.

AI Suggestions:
- Use a list comprehension instead of a loop for better performance.
- Consider adding type annotations to improve readability.
```

---

## **How It Works**
1. **Static Analysis**:
   - Runs **Flake8** for style checks.
   - Executes **Bandit** to identify security vulnerabilities.
2. **AI Analysis**:
   - Uses Hugging Face's open-source models to provide intelligent suggestions.
3. **Combines Feedback**:
   - Merges results into an organized report.

---

## **Roadmap**
- ✨ Add support for more static analysis tools.
- 🌐 Provide a web-based interface for real-time feedback.
- 🔧 Include AI-based auto-fixes for common issues.

---

## **Contributing**
We welcome contributions! Follow these steps to contribute:
1. Fork the repository.
2. Create a new branch.
3. Submit a pull request with your changes.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

---

## **Acknowledgments**
- Open-source models by [Hugging Face](https://huggingface.co/).
- Static analysis tools: **Flake8**, **Bandit**.
