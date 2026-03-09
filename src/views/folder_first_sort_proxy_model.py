from PySide6.QtCore import QSortFilterProxyModel, Qt, QModelIndex, QPersistentModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem


class FolderFirstSortProxyModel(QSortFilterProxyModel):
    """Custom proxy model that ensures folders always appear before files.
    
    This proxy model enforces folders-first sorting as the primary key,
    then applies the user-selected column as the secondary sort key.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._secondary_sort_column = 0
        self._sort_order = Qt.SortOrder.AscendingOrder
    
    def set_secondary_sort_column(self, column: int):
        """Set the column to use for secondary sorting.
        
        Args:
            column: Column index for secondary sort
        """
        self._secondary_sort_column = column
        self.invalidate()
        self.sort(self._secondary_sort_column, self._sort_order)
    
    def set_sort_order(self, order: Qt.SortOrder):
        """Set the sort order.
        
        Args:
            order: Qt.AscendingOrder or Qt.DescendingOrder
        """
        self._sort_order = order
        self.sort(self._secondary_sort_column, order)
    
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        """Compare two indices, ensuring folders come first.
        
        Primary sort: folders before files
        Secondary sort: user-selected column
        
        Args:
            left: Left model index
            right: Right model index
            
        Returns:
            True if left should come before right
        """
        source_model = self.sourceModel()
        if not source_model:
            return False
        
        left_is_folder = source_model.data(left, Qt.ItemDataRole.UserRole + 1)
        right_is_folder = source_model.data(right, Qt.ItemDataRole.UserRole + 1)
        
        if left_is_folder != right_is_folder:
            return bool(left_is_folder) and not bool(right_is_folder)
        
        col = self._secondary_sort_column if self._secondary_sort_column > 0 else 0
        left_index = source_model.index(left.row(), col, left.parent())
        right_index = source_model.index(right.row(), col, right.parent())
        
        left_data = source_model.data(left_index, Qt.ItemDataRole.DisplayRole)
        right_data = source_model.data(right_index, Qt.ItemDataRole.DisplayRole)
        
        if left_data and right_data:
            left_str = left_data.toString()
            right_str = right_data.toString()
            
            if left_str and right_str:
                if self._sort_order == Qt.SortOrder.AscendingOrder:
                    return left_str < right_str
                else:
                    return left_str > right_str
        
        return False
