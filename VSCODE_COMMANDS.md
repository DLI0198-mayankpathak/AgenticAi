# 🎯 VS Code Quick Commands

This project includes VS Code tasks and launch configurations for easy development.

## 🚀 Running the API

### Method 1: Command Palette (Recommended)

1. Press **`Ctrl+Shift+P`** (or `Cmd+Shift+P` on Mac)
2. Type: **"Tasks: Run Task"**
3. Select: **"🚀 Start Jira Analysis API"**

The API will start in a dedicated terminal with hot-reload enabled!

### Method 2: Quick Task Shortcut

1. Press **`Ctrl+Shift+B`** (or `Cmd+Shift+B` on Mac)
2. This runs the default build task (Start API)

### Method 3: Terminal Menu

1. Click **Terminal** → **Run Task...**
2. Select: **"🚀 Start Jira Analysis API"**

---

## 📋 Available Tasks

Access via **Command Palette** → **"Tasks: Run Task"**:

| Task | Description |
|------|-------------|
| **🚀 Start Jira Analysis API** | Starts the API server with auto-reload |
| **📖 Open API Documentation** | Opens http://localhost:8000/docs in browser |
| **🧪 Test API Health** | Checks if API is running |
| **📦 Install Dependencies** | Installs/updates Python packages |

---

## 🐛 Debugging

### Debug the API

1. Press **`F5`** or go to **Run and Debug** panel
2. Select: **"🚀 Debug Jira Analysis API"**
3. Set breakpoints in your code
4. API starts in debug mode with hot-reload

### Debug Single Analysis

1. Press **`F5`**
2. Select: **"🧪 Debug Single Analysis"**
3. Runs `run.py` with debugging enabled

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **`Ctrl+Shift+B`** | Start API (default build task) |
| **`Ctrl+Shift+P`** → Tasks | Show all tasks |
| **`F5`** | Start debugging |
| **`Shift+F5`** | Stop debugging |
| **`Ctrl+C`** (in terminal) | Stop API server |

---

## 🔧 Task Details

### 🚀 Start Jira Analysis API

```json
{
  "label": "🚀 Start Jira Analysis API",
  "command": ".venv/Scripts/python.exe start.py",
  "isBackground": true,
  "group": "build"
}
```

**Features:**
- ✅ Dedicated terminal panel
- ✅ Auto-reload on code changes
- ✅ Clear output on each run
- ✅ Focus on terminal when started

### 📖 Open API Documentation

Opens the interactive Swagger UI documentation in your default browser.

**URL:** http://localhost:8000/docs

### 🧪 Test API Health

Runs a quick `curl` command to check if the API is responding.

**Command:** `curl http://localhost:8000/health`

**Expected Response:** `{"status": "healthy"}`

---

## 📁 Configuration Files

All VS Code configurations are stored in `.vscode/`:

- **`tasks.json`** - Task definitions for running commands
- **`launch.json`** - Debug configurations

---

## 💡 Pro Tips

### 1. Quick Start API
Just press **`Ctrl+Shift+B`** for instant API launch!

### 2. Open Docs After Starting
1. Start API: `Ctrl+Shift+B`
2. Run task: "📖 Open API Documentation"

### 3. Multiple Terminals
Tasks run in dedicated terminals, so you can:
- Start API in one terminal
- Run tests in another
- Keep your main terminal free

### 4. Task Chaining
You can run multiple tasks in sequence via Command Palette.

---

## 🆘 Troubleshooting

### Task Not Found
**Problem:** "No tasks found" message

**Solution:**
1. Ensure `.vscode/tasks.json` exists
2. Reload VS Code: `Ctrl+Shift+P` → "Reload Window"

### Python Not Found
**Problem:** "Python not found" error

**Solution:**
1. Check virtual environment exists: `.venv/`
2. Activate environment manually first
3. Update path in `tasks.json` if needed

### Port Already in Use
**Problem:** Port 8000 is already busy

**Solution:**
1. Stop existing API process
2. Or change port in `start.py`

### Task Won't Stop
**Problem:** API keeps running after closing terminal

**Solution:**
1. Press `Ctrl+C` in the terminal
2. Or kill process manually: `taskkill /F /IM python.exe`

---

## 🎨 Customization

### Change Default Task

Edit `.vscode/tasks.json`:

```json
"group": {
    "kind": "build",
    "isDefault": true  // Make this the default (Ctrl+Shift+B)
}
```

### Add Custom Tasks

Add new tasks to `tasks.json`:

```json
{
    "label": "Your Task Name",
    "type": "shell",
    "command": "your-command",
    "args": ["arg1", "arg2"]
}
```

---

## 📚 More Information

- **VS Code Tasks**: https://code.visualstudio.com/docs/editor/tasks
- **VS Code Debugging**: https://code.visualstudio.com/docs/editor/debugging
- **Python in VS Code**: https://code.visualstudio.com/docs/python/python-tutorial

---

**Quick Start:** Press `Ctrl+Shift+B` to launch the API now! 🚀
