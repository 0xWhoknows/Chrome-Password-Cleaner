import sqlite3
import os
import shutil

class ChromePasswordManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.backup_path = db_path + ".backup"
        self.skip_list = {
            "accounts.google.com", "gmail.com", "google.com", "netflix.com",
            "yahoo.com", "discord.com"} # Websites to **NOT** delete passwords 
        self._backup_database()

    def _backup_database(self):
        """Creates a backup of the database if it doesn't exist."""
        if not os.path.exists(self.backup_path):
            shutil.copy(self.db_path, self.backup_path)
            print(f"📂 Backup created at: {self.backup_path}")

    def _connect_db(self):
        """Connects to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def list_saved_passwords(self):
        """Fetches and lists saved passwords (URLs + usernames)."""
        conn = self._connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value FROM logins")
        passwords = cursor.fetchall()
        conn.close()
        return passwords

    def delete_selected_passwords(self, urls_to_delete):
        """Deletes selected passwords from the database."""
        if not urls_to_delete:
            print("⚠ No valid URLs selected for deletion.")
            return
        
        conn = self._connect_db()
        cursor = conn.cursor()
        for url in urls_to_delete:
            cursor.execute("DELETE FROM logins WHERE origin_url=?", (url,))
            print(f"✅ Deleted passwords for: {url}")
        conn.commit()
        conn.close()
        print("🗑️ Selected passwords deleted successfully!")

    def run(self):
        """Main execution flow."""
        print("\n🔍 Fetching saved passwords...\n")
        passwords = self.list_saved_passwords()

        for i, (url, user) in enumerate(passwords, start=1):
            protected = "❌ (Protected)" if any(skip in url for skip in self.skip_list) else ""
            print(f"[{i}] {url} - {user} {protected}")

        choices = input("\nEnter the numbers of the passwords you want to delete (comma):\n> ").strip()
        
        if choices:
            selected_indexes = [int(x.strip()) - 1 for x in choices.split(",") if x.strip().isdigit()]
            urls_to_delete = [
                passwords[i][0] for i in selected_indexes
                if 0 <= i < len(passwords) and not any(skip in passwords[i][0] for skip in self.skip_list)
            ]
            self.delete_selected_passwords(urls_to_delete)
        else:
            print("❌ No input provided. Exiting.")

if __name__ == "__main__":
    CHROME_LOGIN_DB = os.path.expanduser("~/.config/google-chrome/Default/Login Data")
    manager = ChromePasswordManager(CHROME_LOGIN_DB)
    manager.run()