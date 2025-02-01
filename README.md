# 🗑️ Chrome Password Cleaner

A Python script to **delete unnecessary saved passwords** from Google Chrome while **protecting important ones** (e.g., Google, Yahoo, Binance, Netflix, etc.).

## 📌 Features
✅ Lists all saved passwords (URL + username).  
✅ Allows **selective deletion** of passwords.  
✅ **Skips important passwords** for Google,Yahoo,Netflix.  
✅ Creates a **backup** before modifying the database.  
✅ Deletes only selected passwords, leaving others intact.  

## 🚀 Installation & Usage
### 1️⃣ Close Chrome Before Running
Make sure Chrome is **completely closed** before using the script. Run:
```bash
pkill chrome
```

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/chrome-password-cleaner.git
cd Chrome-Password-Cleaner
```

### 3️⃣ Install Dependencies (if needed)
This script only requires Python's built-in `sqlite3` module, which is included in standard Python installations.

### 4️⃣ Run the Script
```bash
python3 main.py
```

### 5️⃣ Select Passwords to Delete
- The script will **list all saved passwords**.
- **Protected passwords** (Google, Yahoo, Binance, etc.) will be marked **❌ (Protected)** and cannot be deleted.
- Enter the **numbers** of the passwords you want to delete (comma-separated).

### 6️⃣ Restart Chrome
After deleting passwords, restart Chrome to see the changes.

## 🛠 Troubleshooting
### "sqlite3.OperationalError: database is locked"
If you get this error:
1. **Close Chrome completely:**
   ```bash
   pkill chrome
   ```
2. **Check if Chrome is still using the file:**
   ```bash
   lsof ~/.config/google-chrome/Default/Login\ Data
   ```
   If a process is listed, **kill it**:
   ```bash
   kill -9 <PID>
   ```
3. **Make a copy of the database and edit the copy:**
   ```bash
   cp ~/.config/google-chrome/Default/Login\ Data ~/Desktop/LoginData_copy
   ```
   Then modify `main.py` to use `~/Desktop/LoginData_copy` instead.

## ⚠️ Disclaimer
- **Use this script at your own risk.** Editing Chrome's database directly can corrupt it if done incorrectly.
- **Always create a backup** (this script does it automatically).



