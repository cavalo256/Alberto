import sqlite3
import shutil
from datetime import datetime

class BackupSystem:
    @staticmethod
    def create_backup():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backups/bot_data_{timestamp}.db"
        shutil.copyfile('bot_data.db', backup_name)
        return backup_name