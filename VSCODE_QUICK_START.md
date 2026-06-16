# VS Code Quick Start - TechVault Debugging

## ⚡ 30-Second Setup

### 1. Open Project in VS Code
```bash
cd /Users/encikwad/Documents/Software_Design/Project_Assignment
code .
```

### 2. Required Extensions (3 total)
- Search in Extensions (Ctrl+Shift+X):
  - ✅ **Python** by Microsoft (should auto-install)
  - ✅ **Debugger for Chrome** by Microsoft
  - ✅ **Prettier** by Prettier (optional, for formatting)

---

## 🚀 Quick Debug Session (5 minutes)

### Terminal 1: Start Backend
```bash
# Opens in VS Code integrated terminal (Ctrl+`)
# Or open new terminal and type:
cd backend && python3 run.py
```

**You should see:**
```
Default accounts ready (admin@techvault.com / customer@techvault.com)
Running on http://127.0.0.1:5000
```

### Terminal 2: Start Frontend
```bash
# Press Ctrl+Shift+` to open second terminal
cd frontend && python3 -m http.server 8000
```

**You should see:**
```
Serving HTTP on 0.0.0.0 port 8000
```

---

## 🎯 Debug a Checkout (Right Now!)

### Step 1: Set Breakpoints
1. Open `frontend/js/cart.js` (Ctrl+P, type `cart.js`)
2. **Click on line 72** (the `async function checkout()` line)
   - Red dot appears ✓
3. Open `backend/app/routes/order.py` (Ctrl+P, type `order.py`)
4. **Click on line 18** (inside checkout function)
   - Red dot appears ✓

### Step 2: Open Browser
```
http://localhost:8000/pages/index.html
```

### Step 3: Trigger Breakpoint
1. Login: `customer@techvault.com` / `customer123`
2. Add a product to cart
3. Click "Checkout" button

### Step 4: Debugger Pauses!
- **VS Code pauses at frontend breakpoint** (cart.js:72)
- **Left panel shows:**
  - `userId`: 2
  - `paymentMethod`: "card"
- Press **F10** to step to next line
- Press **F5** to continue

### Step 5: Watch Backend Breakpoint
- Click checkout button again
- **VS Code pauses at backend breakpoint** (order.py:18)
- Shows:
  - `user_id`: 2
  - `payment_method`: "card"
- Look at **TERMINAL** → See debug output with STRATEGY pattern!

---

## 📍 Key Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **F5** | Start/Continue debugging |
| **F10** | Step over (next line) |
| **F11** | Step into (enter function) |
| **Shift+F11** | Step out (exit function) |
| **Ctrl+Shift+D** | Open Debug panel |
| **Ctrl+`` | Toggle Terminal |
| **Ctrl+P** | Quick file open |

---

## 🔍 Debug Panels (Left Side)

### VARIABLES
- Shows all local variables
- Expand to see object properties
- Hover over variables in code to preview

### WATCH
- Add custom variables to watch
- Click **+** to add
- Examples:
  - `order_id`
  - `cart.total`
  - `localStorage`

### CALL STACK
- Shows function call chain
- Click to jump to previous function

### BREAKPOINTS
- List of all breakpoints
- Check/uncheck to enable/disable
- Right-click → "Remove breakpoint"

---

## 💻 Debug Console (Bottom)

**Type commands to inspect:**
```javascript
localStorage               // See all stored values
localStorage.getItem('userId')    // Get specific value
cart                      // Check cart object
order                     // Check order object
```

---

## 🎓 3-Minute Demo for Lecturer

```
[Preparation - 1 min]
- Open VS Code
- Show .vscode/launch.json (already created!)
- Show breakpoints set in cart.js and order.py

[Demo - 2 min]
- F5 → Start backend debug
- Open browser → Login → Add cart
- Click Checkout → Frontend pauses
- Show Variables: userId, paymentMethod
- F10 → Step through code
- F5 → Continue to backend breakpoint
- Show backend Variables
- Terminal shows: STRATEGY, STATE, OBSERVER pattern logs
- Complete and show database updated
```

**Result: Shows design patterns in action!** ✨

---

## 📊 Common Tasks

### Find & Set Breakpoint
1. **Ctrl+P** (Quick Open)
2. Type `cart.js`
3. Press Enter
4. **Ctrl+G** (Go to Line)
5. Type `72` (line number)
6. Press Enter → Click line number to set breakpoint

### View Database
1. Open Terminal (Ctrl+`)
2. Type:
   ```bash
   sqlite3 backend/data.db
   SELECT * FROM orders;
   .exit
   ```

### Clear All Breakpoints
1. **Ctrl+Shift+D** (Debug panel)
2. **BREAKPOINTS** section
3. Click **X** on "TechVault Backend" to remove all

### Debug with Conditional Breakpoint
1. Right-click on breakpoint (red dot)
2. Click "Edit Breakpoint"
3. Type condition: `user_id == 2`
4. Only pauses for user 2!

---

## ✅ Verification Checklist

- [ ] Extensions installed (Python + Debugger for Chrome)
- [ ] launch.json exists in .vscode folder
- [ ] Backend runs without errors
- [ ] Frontend server running on port 8000
- [ ] Can set breakpoint (red dot appears)
- [ ] Debugger pauses when breakpoint is hit
- [ ] Variables panel shows values
- [ ] Can step through code (F10)
- [ ] Console shows design pattern logs

---

## 🆘 Troubleshooting

| Problem | Fix |
|---------|-----|
| **Debugger won't start** | Reload VS Code (Ctrl+R), check Python installed |
| **Breakpoint not pausing** | Reload browser (Cmd+R), check line number |
| **Can't see variables** | Breakpoint may be before variable declaration |
| **Backend won't run** | Check Python path: `which python3` |
| **Port 5000 already in use** | Kill process: `lsof -i :5000`, then `kill -9 <PID>` |

---

## 🎯 Next Steps

1. ✅ Set up extensions
2. ✅ Open project in VS Code
3. ✅ Run quick debug session (follow above)
4. ✅ Practice setting breakpoints
5. ✅ Test full stack debugging
6. ✅ Demonstrate to lecturer!

---

**You're ready! Press F5 to start debugging.** 🚀
