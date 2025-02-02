import sqlite3
import os
import shutil
import sys

class ChromePasswordManager:
    def __init__(self):
        """Detect OS and set the correct path for Chrome's Login Data database."""
        self.os_type = sys.platform

        if self.os_type.startswith("win"):
            self.chrome_login_db = os.path.expandvars(
                r"%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Login Data"
            )
        elif self.os_type == "darwin":  # macOS
            self.chrome_login_db = os.path.expanduser(
                "~/Library/Application Support/Google/Chrome/Default/Login Data"
            )
        else:  # Linux
            self.chrome_login_db = os.path.expanduser(
                "~/.config/google-chrome/Default/Login Data"
            )

        self.backup_db = self.chrome_login_db + ".backup"

        self.skip_list = {"accounts.google.com", "gmail.com", "google.com", 
            "netflix.com", "yahoo.com", "discord.com"} # Websites to **NOT** delete passwords 

        # Ensure database backup before modifications
        self.create_backup()

    def create_backup(self):
        """Create a backup of the Chrome Login Data database."""
        if not os.path.exists(self.backup_db):
            shutil.copyfile(self.chrome_login_db, self.backup_db)
            print(f"📂 Backup created at: {self.backup_db}")

    def connect_db(self):
        """Connect to the Chrome database and set PRAGMA for safety."""
        conn = sqlite3.connect(self.chrome_login_db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")  # Prevent database locking
        return conn, cursor

    def list_saved_passwords(self):
        """Fetch and list saved passwords (URLs + usernames)."""
        conn, cursor = self.connect_db()
        cursor.execute("SELECT origin_url, username_value FROM logins")
        passwords = cursor.fetchall()
        conn.close()
        return passwords

    def delete_selected_passwords(self, urls_to_delete):
        """Deletes selected passwords from the database."""
        conn, cursor = self.connect_db()

        for url in urls_to_delete:
            cursor.execute("DELETE FROM logins WHERE origin_url=?", (url,))
            print(f"✅ Deleted passwords for: {url}")

        conn.commit()
        conn.close()

    def run(self):
        """Main function to display passwords and allow selective deletion."""
        print("\n🔍 Fetching saved passwords...\n")
        passwords = self.list_saved_passwords()

        # Display saved passwords
        for i, (url, user) in enumerate(passwords, start=1):
            if any(skip in url for skip in self.skip_list):
                print(f"[{i}] {url} - {user} ❌ (Protected)")
            else:
                print(f"[{i}] {url} - {user}")

        # Get user input for deletion
        print("\nEnter the numbers of the passwords you want to delete (comma-separated):")
        choices = input("> ").strip()

        if choices:
            selected_indexes = [
                int(x.strip()) - 1 for x in choices.split(",") if x.strip().isdigit()
            ]
            urls_to_delete = [
                passwords[i][0] for i in selected_indexes
                if 0 <= i < len(passwords) and not any(skip in passwords[i][0] for skip in self.skip_list)
            ]

            if urls_to_delete:
                self.delete_selected_passwords(urls_to_delete)
                print("\n🗑️ Selected passwords deleted successfully!")
            else:
                print("⚠ No valid selection made (protected entries skipped).")
        else:
            print("❌ No input provided. Exiting.")

# Run the program
if __name__ == "__main__":
    ChromePasswordManager().run()
