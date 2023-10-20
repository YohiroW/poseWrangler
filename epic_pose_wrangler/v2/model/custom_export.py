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
    
    
    def get_output_dir(self):
        return self.output_dir
    
    
    def get_asset_name(self):
        return self.asset_name
    
    
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
       
        
    def export_fbx(self, fbx_name):  
        path = f'{self.output_dir}/{fbx_name}'
        
        cmds.file(path, 
            force=True, 
            options="v=0;", 
            typ="FBX export", 
            es=True, 
            esc=(self.on_export_complete, "TEMP_EXPORT"))
        pass
    
    
    def on_export_complete(self, *args):
        print('=> export complete!')    
        pass
        

    def batch_export_fbx(self):
        rbf_api = main.UERBFAPI(view=False)
        context = rbf_api.get_context()
        
        if context is not None:
            for solver in context.solvers:
                self.bake_and_export(solver)               
        pass
    
    
    def bake_and_export(self, solver):
        suffix = '_UERBFSolver'
        solver_str = str(solver)
        name = solver_str.replace(suffix, '')
        
        # pose_list = solver.poses()
        # for pose in pose_list:
        #     print(f'=> pose: {pose}')
        #     pass
              
        # bake to timeline
        print(f'=> baking {solver_str} to timeline...')
        from epic_pose_wrangler.v2.extensions import bake_poses
        bake_poses.bake_poses_to_timeline(start_frame=0, anim_layer=None, solver=solver, view=False)

        # and..export to fbx
        print(f'=> exporting {solver_str} to fbx...')
        fbx_name = self.asset_name + '_' + name
        self.export_fbx(fbx_name)
        
        pass
    