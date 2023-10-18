import os
import json
from collections import OrderedDict
from maya import cmds
from epic_pose_wrangler.v2 import main

class CustomExporter:
    
    def __init__(self, output_dir, asset_name):
        self.output_dir = output_dir
        self.asset_name = asset_name
        self.node = None
        pass
    
    def set_output_dir(self, output_dir):
        self.output_dir = output_dir
    
    
    def set_asset_name(self, asset_name):
        self.asset_name = asset_name
    
    
    def setRBFNode(self, rbf_node):
        self.node = rbf_node
    
    
    def export(self):
        if not self.node:
            rbf_api = main.UERBFAPI(view=False)
            context = rbf_api.get_context()
            if context is not None:
                #data = []
                # for solver in context.solvers:
                #     data.append(solver.data())
                # self.export_json(data)
                self.export_json(rbf_api)
        else:
            self.export_json(self.node)
            
            
    def export_json(self, rbf_api):
        rbf_api.serialize_to_file(f'{self.output_dir}/{self.asset_name}.json', None)
    