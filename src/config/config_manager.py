"""Configuration manager with SQLite persistence."""

import os
import sys
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any

from PySide6.QtCore import QObject, Signal


class ConfigManager(QObject):
    """Manages application configuration with SQLite persistence.
    
    This class provides persistent storage for application settings using SQLite.
    It is compatible with both development mode and PyInstaller builds.
    
    Signals:
        config_changed(key, value): Emitted when a configuration value changes
        config_saved(): Emitted when configuration is saved successfully
    """
    
    config_changed = Signal(str, str)
    config_saved = Signal()
    
    # Required configuration keys for AWS S3
    REQUIRED_KEYS = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 
        'AWS_DEFAULT_REGION',
        'AWS_S3_BUCKET_NAME'
    ]
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialize the configuration manager.
        
        Args:
            db_path: Optional custom database path. If not provided,
                    uses the default user data directory.
        """
        super().__init__()
        self._db_path = db_path or self._get_default_db_path()
        self._ensure_data_dir_exists()
        self._init_db()
    
    def _get_default_db_path(self) -> str:
        """Get the default database file path.
        
        Returns a path in the user's data directory, compatible with
        both development and PyInstaller builds.
        
        Returns:
            Path to the SQLite database file
        """
        app_name = "BucketBrowser"
        
        # Check if running as PyInstaller bundle
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running as PyInstaller executable
            # Use user's home directory for data persistence
            if sys.platform == 'win32':
                base_dir = Path(os.environ.get('APPDATA', Path.home()))
            elif sys.platform == 'darwin':
                base_dir = Path.home() / 'Library' / 'Application Support'
            else:
                base_dir = Path.home() / '.config'
        else:
            # Running in development mode
            base_dir = Path.home() / '.config'
        
        data_dir = base_dir / app_name
        return str(data_dir / 'config.db')
    
    def _ensure_data_dir_exists(self):
        """Ensure the data directory exists."""
        data_dir = Path(self._db_path).parent
        data_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_db(self):
        """Initialize the database schema."""
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create table for schema versioning
            conn.execute("""
                CREATE TABLE IF NOT EXISTS __meta__ (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)
            
            # Initialize schema version
            conn.execute("""
                INSERT OR IGNORE INTO __meta__ (key, value) 
                VALUES ('schema_version', '1')
            """)
            
            conn.commit()
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute(
                'SELECT value FROM settings WHERE key = ?', 
                (key,)
            )
            row = cursor.fetchone()
            return row[0] if row else default
    
    def set(self, key: str, value: str):
        """Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("""
                INSERT INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
            """, (key, value))
            conn.commit()
        
        self.config_changed.emit(key, value)
    
    def get_all(self) -> Dict[str, str]:
        """Get all configuration values.
        
        Returns:
            Dictionary of all configuration key-value pairs
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute('SELECT key, value FROM settings')
            return dict(cursor.fetchall())
    
    def set_many(self, settings: Dict[str, str]):
        """Set multiple configuration values at once.
        
        Args:
            settings: Dictionary of key-value pairs
        """
        with sqlite3.connect(self._db_path) as conn:
            for key, value in settings.items():
                conn.execute("""
                    INSERT INTO settings (key, value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(key) DO UPDATE SET
                        value = excluded.value,
                        updated_at = CURRENT_TIMESTAMP
                """, (key, value))
            conn.commit()
        
        self.config_saved.emit()
    
    def has_config(self) -> bool:
        """Check if any configuration exists.
        
        Returns:
            True if at least one required key is configured
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute(
                'SELECT COUNT(*) FROM settings WHERE key IN ({})'.format(
                    ','.join('?' * len(self.REQUIRED_KEYS))
                ),
                self.REQUIRED_KEYS
            )
            count = cursor.fetchone()[0]
            return count > 0
    
    def is_fully_configured(self) -> bool:
        """Check if all required configuration is present.
        
        Returns:
            True if all required keys have values
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute(
                'SELECT COUNT(*) FROM settings WHERE key IN ({})'.format(
                    ','.join('?' * len(self.REQUIRED_KEYS))
                ),
                self.REQUIRED_KEYS
            )
            count = cursor.fetchone()[0]
            return count == len(self.REQUIRED_KEYS)
    
    def get_missing_keys(self) -> list[str]:
        """Get list of required keys that are not configured.
        
        Returns:
            List of missing configuration keys
        """
        with sqlite3.connect(self._db_path) as conn:
            cursor = conn.execute(
                'SELECT key FROM settings WHERE key IN ({})'.format(
                    ','.join('?' * len(self.REQUIRED_KEYS))
                ),
                self.REQUIRED_KEYS
            )
            configured_keys = {row[0] for row in cursor.fetchall()}
            return [key for key in self.REQUIRED_KEYS if key not in configured_keys]
    
    def delete(self, key: str):
        """Delete a configuration value.
        
        Args:
            key: Configuration key to delete
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.execute('DELETE FROM settings WHERE key = ?', (key,))
            conn.commit()
    
    def clear_all(self):
        """Clear all configuration. Use with caution."""
        with sqlite3.connect(self._db_path) as conn:
            conn.execute('DELETE FROM settings')
            conn.commit()


# Global instance for convenience
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """Get the global ConfigManager instance.
    
    Returns:
        ConfigManager singleton instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
