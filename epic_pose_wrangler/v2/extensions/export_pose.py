import traceback
import os

from functools import partial
from maya import cmds
from epic_pose_wrangler.log import LOG
from epic_pose_wrangler.v2.model import base_extension, exceptions, pose_blender
from epic_pose_wrangler.v2.model import custom_export

from PySide2 import QtWidgets

def get_maya_name_noext():
    maya_name = cmds.file(query=True, sceneName=True, shortName=True)
    maya_name = maya_name.split('.')[0]
    return maya_name

def get_current_file_dir():
    maya_path = cmds.file(query=True, sceneName=True)
    maya_path = '/'.join(maya_path.split('/')[:-1])
    return maya_path

class ExportPose(base_extension.PoseWranglerExtension):
    __category__ = "Export"
    
    @property
    def view(self):
        if self._view is not None:
            return self._view
        
        self._view = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        self._view.setLayout(layout)
        
        # file name
        filename_layout = QtWidgets.QHBoxLayout()
        
        label = QtWidgets.QLabel("File Name:")
        filename_layout.addWidget(label)

        self.filename_field = QtWidgets.QLineEdit()
        temp_filename = get_maya_name_noext()
        self.filename_field.setPlaceholderText(temp_filename)
        filename_layout.addWidget(self.filename_field)
        self.asset_name = temp_filename
        
        layout.addLayout(filename_layout)
        
        # browser
        browser_layout = QtWidgets.QHBoxLayout()
        
        export_label = QtWidgets.QLabel("Output Dir:")
        browser_layout.addWidget(export_label)
        
        export_path_text_field = QtWidgets.QLineEdit()   
        current_dir = get_current_file_dir()
        export_path_text_field.setPlaceholderText(current_dir)
        export_path_text_field.setReadOnly(True)
        self.output_dir = current_dir
        browser_layout.addWidget(export_path_text_field)
        
        browser_btn = QtWidgets.QPushButton("Browse")
        browser_btn.clicked.connect(partial(self.browser_export_path, export_path_text_field))
        browser_layout.addWidget(browser_btn)
        
        layout.addLayout(browser_layout)  
        
        # checkbox
        horizontal_layout = QtWidgets.QHBoxLayout()
    
        fbx_checkbox = QtWidgets.QCheckBox("Export as fbx")
        fbx_checkbox.setChecked(True)
        horizontal_layout.addWidget(fbx_checkbox)
        
        json_checkbox = QtWidgets.QCheckBox("Export as json")
        json_checkbox.setChecked(False)
        horizontal_layout.addWidget(json_checkbox)
        
        layout.addLayout(horizontal_layout)

        export_btn = QtWidgets.QPushButton("Export")
        layout.addWidget(export_btn)
        export_btn.clicked.connect(partial(self.on_export, fbx_checkbox, json_checkbox))
        
        return self._view

    def on_export(self, fbx_check, json_check, *args):
        fbx_check = fbx_check.isChecked()
        json_check = json_check.isChecked()
        
        if fbx_check:
            self.export_fbx()

        if json_check:
            self.export_json()

    
    def export_fbx(self, *args):
        if self.filename_field.text() == '':       
            export_name = get_maya_name_noext()
        else:
            export_name = self.filename_field.text()
            
        output_path = f'{self.output_dir}/{export_name}'
        print(f'=> fbx output_path: {output_path}')

        cmds.file(output_path, 
                  force=True, 
                  options="v=0;", 
                  typ="FBX export", 
                  es=True, 
                  esc=(self.on_export_complete, "TEMP_EXPORT"))


    def export_json(self, *args):
        custom_export.CustomExporter(self.output_dir, self.asset_name).export()
            
            
    def on_export_complete(self, *args):
        pass
        
    
    def browser_export_path(self, text_field, *args):
        # Open dialog
        output_dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Export File Directory')
        
        # If no directory specified, exit early
        if not output_dir:
            return
            
        text_field.setText(output_dir)
        self.output_dir = output_dir
        