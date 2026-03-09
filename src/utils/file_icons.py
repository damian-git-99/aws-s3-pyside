"""File icon system for bucket browser."""
from typing import Dict, Optional
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter
from PySide6.QtWidgets import QFileIconProvider, QStyle
from PySide6.QtCore import QSize


class FileIconManager:
    """Manages icons for different file types."""
    
    # Icon cache to avoid recreating icons
    _icon_cache: Dict[str, QIcon] = {}
    _file_icon_provider = QFileIconProvider()
    
    @classmethod
    def get_icon(cls, icon_type: str) -> QIcon:
        """Get icon for a specific file type.
        
        Args:
            icon_type: Type of icon ('folder', 'image', 'document', 'code', 
                      'archive', 'generic')
            
        Returns:
            QIcon instance for the file type
        """
        if icon_type in cls._icon_cache:
            return cls._icon_cache[icon_type]
        
        icon = cls._create_icon(icon_type)
        cls._icon_cache[icon_type] = icon
        return icon
    
    @classmethod
    def _create_icon(cls, icon_type: str) -> QIcon:
        """Create an icon for the given type."""
        icon_map = {
            'folder': cls._create_folder_icon(),
            'image': cls._create_image_icon(),
            'document': cls._create_document_icon(),
            'code': cls._create_code_icon(),
            'archive': cls._create_archive_icon(),
            'generic': cls._create_generic_icon(),
        }
        return icon_map.get(icon_type, cls._create_generic_icon())
    
    @classmethod
    def _create_folder_icon(cls) -> QIcon:
        """Create a folder icon."""
        # Use system icon if available, fallback to custom
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#f0c040"))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#b09030"))
        painter.drawRect(4, 8, 24, 20)
        painter.drawRect(4, 4, 12, 6)
        painter.end()
        
        return QIcon(pixmap)
    
    @classmethod
    def _create_image_icon(cls) -> QIcon:
        """Create an image file icon."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#4CAF50"))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#2E7D32"))
        # Draw a simple mountain/landscape
        painter.drawRect(4, 4, 24, 24)
        painter.drawLine(4, 20, 12, 12)
        painter.drawLine(12, 12, 20, 20)
        painter.drawLine(20, 20, 28, 10)
        painter.end()
        
        return QIcon(pixmap)
    
    @classmethod
    def _create_document_icon(cls) -> QIcon:
        """Create a document icon."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#2196F3"))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#1565C0"))
        # Draw document shape
        painter.drawRect(4, 2, 24, 28)
        # Draw lines representing text
        for i in range(4):
            painter.drawLine(7, 8 + i * 5, 25, 8 + i * 5)
        painter.end()
        
        return QIcon(pixmap)
    
    @classmethod
    def _create_code_icon(cls) -> QIcon:
        """Create a code file icon."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#9C27B0"))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#6A1B9A"))
        painter.setBrush(QColor("white"))
        # Draw code brackets < />
        painter.drawRect(4, 2, 24, 28)
        painter.setPen(QColor("white"))
        font = painter.font()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(4, 2, 24, 28, 0x84, "{ }")  # Align center
        painter.end()
        
        return QIcon(pixmap)
    
    @classmethod
    def _create_archive_icon(cls) -> QIcon:
        """Create an archive icon."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#FF9800"))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#E65100"))
        # Draw box/archive shape
        painter.drawRect(4, 6, 24, 20)
        # Draw zipper line
        painter.drawLine(16, 6, 16, 26)
        for i in range(3):
            painter.drawPoint(16, 10 + i * 5)
        painter.end()
        
        return QIcon(pixmap)
    
    @classmethod
    def _create_generic_icon(cls) -> QIcon:
        """Create a generic file icon."""
        pixmap = QPixmap(32, 32)
        pixmap.fill(QColor("#757575"))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#424242"))
        painter.drawRect(4, 4, 24, 24)
        painter.end()
        
        return QIcon(pixmap)
    
    @classmethod
    def get_icon_for_object(cls, bucket_object) -> QIcon:
        """Get the appropriate icon for a bucket object.
        
        Args:
            bucket_object: BucketObject instance
            
        Returns:
            QIcon for the object
        """
        icon_type = bucket_object.get_icon_type()
        return cls.get_icon(icon_type)
