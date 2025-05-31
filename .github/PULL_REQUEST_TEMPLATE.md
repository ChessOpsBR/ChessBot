# 🔃 Pull Request – [UC-XX] Task Title

## 🔗 Linear Issue
[ISSUE-CODE – Task Name](https://linear.app/your-team/issue/ISSUE-CODE/task-title-kebab-case)

---

## 🗂 PR Category  
Select all that apply:

- [ ] Bug fix `bugfix`  
- [ ] Feature addition `feature`  
- [ ] Code refactoring `chore`  
- [ ] Dependency update `update`  
- [ ] Documentation `docs`

---

## 📦 Module  
**[UC-XX] Module or Feature Name**

---

## 🛠 Implementation Details  
Clearly describe what has been implemented in this PR. Include:

- Main changes made to the codebase
- New or updated files/modules
- Any refactoring or reorganizations
- Purpose and benefits of the change
- Any known impact on current functionality

**Example:**  
- Centralized Chess.com API logic into `infrastructure/chess_api.py`  
- Implemented `head_to_head` function in `application/get_head_to_head.py` to compute match statistics between players  
- General refactor to improve modularity and prepare for multi-platform support (e.g., Lichess)

---

## ✅ Pre-Merge Checklist  

- [ ] Tests were executed and passed  
- [ ] Code was reviewed locally  
- [ ] No debug files, temp files, or unnecessary comments remain  
- [ ] The PR is linked to a Linear issue  
- [ ] Code follows the project’s style guide  

---

## 🧪 Test Instructions (optional)  
If applicable, describe how to manually test this feature with clear steps:

```bash
# Example:
python main.py
