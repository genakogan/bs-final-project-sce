from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import uuid
import base64
import Notebook as note
class TE(QTextEdit):
    """
    Class for isert data to notebook window 
    """
    def canInsertFromMimeData(self, source):
        
        """
            This function returns true if the object can return an image.
        Parameters:
        source : PyQt5.QtCore.QMimeData 
            QMimeData - class provides a container for data that records information about its MIME type.

        Returns:
            bool
        """
        if source.hasImage():
            return True
        else:
            return super(TE, self).canInsertFromMimeData(source)
    def insertFromMimeData(self, source):
        """
        
           A function places the data in a window

        Parameters:
        source : PyQt5.QtCore.QMimeData 
            QMimeData - class provides a container for data that records information about its MIME type.

        Returns:
            return - This is used for the same reason as break in loops.
            The return value doesn't matter and you only want to exit the whole function.
            It's extremely useful in some places, even though you don't need it that often.

        """
        cursor = self.textCursor()
        document = self.document()
        if source.hasUrls():
            for u in source.urls():
                file_ext = note.splitext(str(u.toLocalFile()))
                if u.isLocalFile() and file_ext in note.IMAGE_EXTENSIONS:
                    image = QImage(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, image)
                    cursor.insertImage(u.toLocalFile())

                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break
            else:
                # If all were valid images, finish here.
                return
        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return
        super(TE, self).insertFromMimeData(source)
