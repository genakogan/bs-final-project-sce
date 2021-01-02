from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import uuid
import base64
import TextEditNote as te
# Global Variables
IMAGE_EXTENSIONS = ['.jpg','.png','.bmp'] # Accepted image extensions
HTML_EXTENSIONS = ['.htm', '.html']  # Accepted file extensions
# Possible font sizes
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]



class Note(QMainWindow):
    """
        Creating main window class for Notebook app
    """
    def __init__(self):
      
        """
            Constructor
            
        Parameters:
            self - current object
            
        Return:
            None
        """
        super(Note, self).__init__()
        
        # QVBoxLayout Organizes your widgets vertically in a window
        layout = QVBoxLayout()
        
        # TE() class in TextEdit
        self.editor = te.TE()
        
        # Setup the QTextEdit editor configuration
        #self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.updateFormat)
        
        # Initialize default font size.
        font = QFont('Times', 12)
        self.editor.setFont(font)
        
        # We need to repeat the size to init the current format.
        self.editor.setFontPointSize(12)
        
        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None
        
        # Insert widgets into a layout
        layout.addWidget(self.editor)

        # Create central window
        container = QWidget()
        
        # SetLayout() function applies a layout to a widget
        container.setLayout(layout)
        
        #Sets the given widget to be the main window's central widget.
        self.setCentralWidget(container)
        
        # QStatusBar class provides a horizontal bar suitable for presenting status information.
        self.status = QStatusBar()
        
        # Add status bar in left side of window
        self.setStatusBar(self.status)
        
        # A QToolBar widget is a movable panel consisting of text buttons, buttons with icons or other widgets
        fileToolbar = QToolBar("File")
        
        # In order to change the icon size of items icon we will use setIconSize method.
        fileToolbar.setIconSize(QSize(14, 14))
        
        # Add toolbar - Open file, Save, Sava as, Print
        self.addToolBar(fileToolbar)
        
        # Add a horizontal bar with buttons items, typically file menu and others.
        fileMenu = self.menuBar().addMenu("&File")
        
        # Add "Open file" action to the Toolbars
        openFileAction = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        
        # Status tip is basically text set by the developer to give the tip(information)
        # About the spin box state to other developers.
        openFileAction.setStatusTip("Open file")
        
        # To connect an method with it when triggered signal is emitted
        openFileAction.triggered.connect(self.file_open)
        fileMenu.addAction(openFileAction)
        fileToolbar.addAction(openFileAction)
        
        # Add "Save" action to the Toolbars
        saveFileAction = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        saveFileAction.setStatusTip("Save current page")
        saveFileAction.triggered.connect(self.file_save)
        fileMenu.addAction(saveFileAction)
        fileToolbar.addAction(saveFileAction)
        
        # Add "Save as" action to the Toolbars
        saveasFileAction = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveasFileAction.setStatusTip("Save current page to specified file")
        saveasFileAction.triggered.connect(self.file_saveas)
        fileMenu.addAction(saveasFileAction)
        fileToolbar.addAction(saveasFileAction)
        
        # Add "Print" action to the Toolbars
        printAction = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        printAction.setStatusTip("Print current page")
        printAction.triggered.connect(self.file_print)
        fileMenu.addAction(printAction)
        fileToolbar.addAction(printAction)
        
        # A movable panel for "Edit" options - redo, cut, copy, paste
        editToolbar = QToolBar("Edit")
        
        # Size of "Edit" panel
        editToolbar.setIconSize(QSize(16, 16))
        self.addToolBar(editToolbar)
        
        # Add a horizontal bar with buttons items, typically file menu and others.
        editMenu = self.menuBar().addMenu("&Edit")
        
        # Add "Undo" to the "Edit" menu
        undoAction = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undoAction.setStatusTip("Undo last change")
        undoAction.triggered.connect(self.editor.undo)
        editMenu.addAction(undoAction)
        
        # Add "Redo" to the "Edit" menu
        redoAction = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redoAction.setStatusTip("Redo last change")
        redoAction.triggered.connect(self.editor.redo)
        editToolbar.addAction(redoAction)
        editMenu.addAction(redoAction)
        
        # Add seporator betwen 
        editMenu.addSeparator()
        
        # Add "Cur" to the "Edit" menu
        cutAction = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cutAction.setStatusTip("Cut selected text")
        cutAction.setShortcut(QKeySequence.Cut)
        cutAction.triggered.connect(self.editor.cut)
        editToolbar.addAction(cutAction)
        editMenu.addAction(cutAction)
        
        # Add "Copy" to the "Edit" menu
        copyAction = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copyAction.setStatusTip("Copy selected text")
        cutAction.setShortcut(QKeySequence.Copy)
        copyAction.triggered.connect(self.editor.copy)
        editToolbar.addAction(copyAction)
        editMenu.addAction(copyAction)
        
        # Add "Paste" to the "Edit" menu
        pasteAction = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        pasteAction.setStatusTip("Paste from clipboard")
        cutAction.setShortcut(QKeySequence.Paste)
        pasteAction.triggered.connect(self.editor.paste)
        editToolbar.addAction(pasteAction)
        editMenu.addAction(pasteAction)
        
        # Add "Select all" to the "Edit" menu
        selectAction = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        selectAction.setStatusTip("Select all text")
        cutAction.setShortcut(QKeySequence.SelectAll)
        selectAction.triggered.connect(self.editor.selectAll)
        editMenu.addAction(selectAction)
        
        # Add seporator betwen 
        editMenu.addSeparator()
        
        # Add "Wrap text to window" to the "Edit" menu
        wrapAction = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
        wrapAction.setStatusTip("Toggle wrap text to window")
        wrapAction.setCheckable(True)
        wrapAction.setChecked(True)
        wrapAction.triggered.connect(self.edit_toggle_wrap)
        editMenu.addAction(wrapAction)
        
        # A movable panel for "Format" options - redo, cut, copy, paste
        formatToolbar = QToolBar("Format")
        formatToolbar.setIconSize(QSize(16, 16))
        self.addToolBar(formatToolbar)
        
        # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        formatToolbar.addWidget(self.fonts)
        
        # QComboBox is a widget in PyQt5 which is used to choose from a list.
        self.fontsize = QComboBox()
        
        # Choose font sizes
        self.fontsize.addItems([str(s) for s in FONT_SIZES])
        
        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.fontsize.currentIndexChanged[str].connect(lambda s: self.editor.setFontPointSize(float(s)) )
        formatToolbar.addWidget(self.fontsize)
        
        # Setting "Bold" button
        self.boldAction = QAction(QIcon(os.path.join('images', 'edit-bold.png')), "Bold", self)
        self.boldAction.setStatusTip("Bold")
        self.boldAction.setShortcut(QKeySequence.Bold)
        
        # Setting "Italic" button
        self.italicAction = QAction(QIcon(os.path.join('images', 'edit-italic.png')), "Italic", self)
        self.italicAction.setStatusTip("Italic")
        self.italicAction.setShortcut(QKeySequence.Italic)
        self.italicAction.setCheckable(True)
        self.italicAction.toggled.connect(self.editor.setFontItalic)
        formatToolbar.addAction(self.italicAction)
        
        # Setting "Align left" button
        self.alignlAction = QAction(QIcon(os.path.join('images', 'edit-alignment.png')), "Align left", self)
        self.alignlAction.setStatusTip("Align text left")
        self.alignlAction.setCheckable(True)
        self.alignlAction.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        formatToolbar.addAction(self.alignlAction)
        
        # Setting "Underline" button
        self.underlineAction = QAction(QIcon(os.path.join('images', 'edit-underline.png')), "Underline", self)
        self.underlineAction.setStatusTip("Underline")
        self.underlineAction.setShortcut(QKeySequence.Underline)
        self.underlineAction.setCheckable(True)
        self.underlineAction.toggled.connect(self.editor.setFontUnderline)
        formatToolbar.addAction(self.underlineAction)
        
        # Setting "Align left" button
        self.aligncAction = QAction(QIcon(os.path.join('images', 'edit-alignment-center.png')), "Align center", self)
        self.aligncAction.setStatusTip("Align text center")
        self.aligncAction.setCheckable(True)
        self.aligncAction.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        formatToolbar.addAction(self.aligncAction)
        
        # Setting "Align right" button
        self.alignrAction = QAction(QIcon(os.path.join('images', 'edit-alignment-right.png')), "Align right", self)
        self.alignrAction.setStatusTip("Align text right")
        self.alignrAction.setCheckable(True)
        self.alignrAction.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        formatToolbar.addAction(self.alignrAction)
        
        # Setting "Justify" button
        self.alignjAction = QAction(QIcon(os.path.join('images', 'edit-alignment-justify.png')), "Justify", self)
        self.alignjAction.setStatusTip("Justify text")
        self.alignjAction.setCheckable(True)
        self.alignjAction.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        formatToolbar.addAction(self.alignjAction)
        
        # Represent each command as an action
        formatGroup = QActionGroup(self)
        
        #If this property is true, then only one button in the group can be checked at any given time. 
        #The user can click on any button to check it, and that button will replace the
        #existing one as the checked button in the group
        formatGroup.setExclusive(True)
        formatGroup.addAction(self.alignlAction)
        formatGroup.addAction(self.aligncAction)
        formatGroup.addAction(self.alignrAction)
        formatGroup.addAction(self.alignjAction)
        
        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.boldAction,
            self.italicAction,
            self.underlineAction,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]
        
        # Initialize.
        self.updateFormat()
        self.update_title()
        self.show()
    def block_signals(self, objects, b):
       
        """
            Function can stopping the button to do his assigned task.
      
        Parameters:
        objects : list
            List of PyQt5.QtWidgets.QAction
        b : bool
              Returns True when the argument x is true, False otherwise.

        Returns:
            None

        """
        for o in objects:
            o.blockSignals(b)
    def updateFormat(self):
        """
           Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        
        Parameters:
            self - current object
        
        Returns:
            None

        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        self.fonts.setCurrentFont(self.editor.currentFont())
        
        # Nasty, but we get the font-size as a float but want it was an int
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))
        
        # SetChecked method is used to change the state of check box
        self.italicAction.setChecked(self.editor.fontItalic())
        self.underlineAction.setChecked(self.editor.fontUnderline())
        self.boldAction.setChecked(self.editor.fontWeight() == QFont.Bold)
        self.alignlAction.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.aligncAction.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignrAction.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignjAction.setChecked(self.editor.alignment() == Qt.AlignJustify)
        
        self.block_signals(self._format_actions, False)

    def file_save(self):
        """
            Function can save existing files.
        Existing files can be saved directly 
        without changing path and name of image.
        If file do not have a path, function will redirect to "file_saveas" function.      
        
        Parameters:
            self - the object
        
        Returns
            None

        """
        if self.path is None:
            
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        text = self.editor.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.editor.toPlainText()

        try:
            with open(self.path, 'w',encoding="utf-8") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))
    
    def file_saveas(self):
        """
        The Save As function can save new file. 
        After click on save as botton you will see the new window
        with some option about where to save your file.
        User can provide a name for the file to be created,
        select a folder in which to place the new file, 
        and select a file format type for the file.
        
        Parameters:
            self - the object
            
        Returns:
            None
        """
        
        #getSaveFileName let you specify the default directory, filetypes and the default filename.
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)")

        if not path:
            
            # If dialog is cancelled, will return ''
            return
        text = self.editor.toHtml() if splitext(path) in HTML_EXTENSIONS else self.editor.toPlainText()
        try:
            with open(path, 'w',encoding="utf-8") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()
    def file_open(self):
        """
        The File Open function can open existing file. 
        After click on  botton you will see the new window
        with some option about from where to open file
        
        Parameters:
            self - the object
        
        Returns:
            None
        """
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)")
        try:
            
            with open(path, 'r',encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            
            # Qt will automatically try and guess the format as txt/html
            self.editor.setText(text)
            self.update_title()
            
    # Function for exception message
    def dialog_critical(self, s):
        """
        This Function show information of Exception.
        This information user can see in new open Window after catches exceptions.
        
        Parameters:
        s : str
           s    -    Exception message
           self -   the object
        
        Returns:
            None

        """
        # The QMessageBox is a dialog that shows an informational message
        dlg = QMessageBox(self)
        
        # Text for exception window
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
            
    def update_title(self):
        """
            Setting application name 
        
        Parameters:
            self - the object
       
        Returns:
            None

        """
        self.setWindowTitle("Notebook" )


    
    def edit_toggle_wrap(self):
        
        """
           This function causes words to be wrapped at the right edge of the text edit. 
        Wrapping occurs at whitespace, keeping whole words intact.
        
        Parameters:
            self - the object
       
        Returns:
            None

        """
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )
    
    def file_print(self):
        """
        Function can print text which was open or created in this app.
        After click on button "Print"user can see new window which contain some option about.
    
        Parameters:
            self - the object
        
        Returns:
            None

        """
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())
# Open image or text file 

        
def hexuuid():
    """
     Obtain a universally unique identifier (UUID) for an object.
     uuid4() generates a random UUID
    Returns:
        TYPE:long int
    """
    return uuid.uuid4().hex

# Split text
def splitext(p):
    """
        Functiom gets name of file that will be saved and 
        separates the file extension

    Parameters:
    p : str
        Name of file
    
    Returns:   
        str
    File extension.
    """
    return os.path.splitext(p)[1].lower()


#if __name__ == '__main__':

    #app = QApplication(sys.argv)
    #app.setApplicationName("Notebook")

    #window = Note()
    #app.exec_()