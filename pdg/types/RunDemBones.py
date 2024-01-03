import os
import pdg
from pdg.processor import PyProcessor
from pdg import (envVar, strData, intData, floatData, resultData, hasStrData, hasIntData, hasFloatData, hasResultData, resultDataIndex, findResultData, findDirectResultData, floatDataArray, intDataArray, strDataArray, findData, findDirectData, input, workItem, kwargs)


class RunDemBones(PyProcessor):
    @classmethod
    def templateName(cls):
        return 'pythonprocessor1_template'


    @classmethod
    def templateBody(cls):
        return """{
            "name": "pythonprocessor1_template",
            "dataType": "genericdata",
            "parameters": [
            ]
        }"""


    def onAddInternalDependencies(self, dependency_holder, internal_items, is_static):
        return pdg.result.Success


    def onGenerate(self, item_holder, upstream_items, generation_type):
        # Called when this node should generate new work items from upstream items.
        #
        # self             -   A reference to the current pdg.Node instance
        # item_holder      -   A pdg.WorkItemHolder for constructing and adding work items
        # upstream_items   -   The list of work items in the node above, or empty list if there are no inputs
        # generation_type  -   The type of generation, e.g. pdg.generationType.Static, Dynamic, or Regenerate
        
        def set_attrs(self, work_item):
            # Construct the command with subprocess options
            command = [f"'{os.environ.get('DemBonesExe')}'"]

            # Required attributes
            abc_file = work_item.attribValue("abc_files")
            command.append(f"-a='{abc_file}'")
        
            fbx_file = work_item.attribValue("fbx_files")  # Used for init file
            command.append(f"-i='{fbx_file}'")
        
            out_file = work_item.attribValue("out_files")  # Used for output file
            command.append(f"-o='{out_file}'")
        
            nBones = work_item.attribValue("nBones")
            if nBones:
                command.append(f"-b={nBones}")
        
            nInitIters = work_item.attribValue("nInitIters")
            if nInitIters:
                command.append(f"--nInitIters={nInitIters}")
        
            nIters = work_item.attribValue("nIters")
            if nIters:
                command.append(f"-n={nIters}")
        
            tolerance = work_item.attribValue("tolerance")
            if tolerance:
                command.append(f"--tolerance={tolerance}")
        
            patience = work_item.attribValue("patience")
            if patience:
                command.append(f"--patience={patience}")
        
            nTransIters = work_item.attribValue("nTransIters")
            if nTransIters:
                command.append(f"--nTransIters={nTransIters}")
        
            bindUpdate = work_item.attribValue("bindUpdate")
            if bindUpdate:
                command.append(f"--bindUpdate={bindUpdate}")
        
            transAffine = work_item.attribValue("transAffine")
            if transAffine:
                command.append(f"--transAffine={transAffine}")
        
            transAffineNorm = work_item.attribValue("transAffineNorm")
            if transAffineNorm:
                command.append(f"--transAffineNorm={transAffineNorm}")
        
            nWeightsIters = work_item.attribValue("nWeightsIters")
            if nWeightsIters:
                command.append(f"--nWeightsIters={nWeightsIters}")
        
            nnz = work_item.attribValue("nnz")
            if nnz:
                command.append(f"-z={nnz}")
        
            weightsSmooth = work_item.attribValue("weightsSmooth")
            if weightsSmooth:
                command.append(f"--weightsSmooth={weightsSmooth}")
        
            weightsSmoothStep = work_item.attribValue("weightsSmoothStep")
            if weightsSmoothStep:
                command.append(f"--weightsSmoothStep={weightsSmoothStep}")
        
            dbg = work_item.attribValue("dbg")
            if dbg:
                command.append(f"--dbg={dbg}")
        
            log = work_item.attribValue("log")
            if log:
                command.append(f"--log={log}")

            work_item.setStringAttrib("Command", " ".join(command))

            # Set the command line that this work item will run
            work_item.setCommand(" ".join(command))

        
        if upstream_items:
            # If there are upstream items, generate new items from them
            for upstream_item in upstream_items:
                # Create a new work item based on the upstream item
                new_item = item_holder.addWorkItem(index=upstream_item.index,
                                                   parent=upstream_item)
                # Set the item's attributes based on the parameters
                set_attrs(self, new_item)
        return pdg.result.Success


    def onRegenerate(self, item_holder, existing_items, upstream_items, generation_type):
        print("Regenerate DemBones CMD trigger")
        return pdg.result.Success


    def onCookTask(self, work_item):
        # Called when an in process work item needs to cook. In process work items
        # are created by passing the  flag when constructing the item in
        # the Generate callback
        #
        # self              -   A reference to the current pdg.Node instance
        # work_item         -   The work item being cooked by this callback

        # Register the output file, so it can be tracked and managed
        # work_item.addOutputFiles([work_item.attribValue("out_files")], "file")

        return pdg.result.Success


    def onConfigureNode(self, node_options):
        node_options.serviceName = ''
        node_options.isAlwaysRegenerate = False
        node_options.isDirtyOnRegenerate = False
        node_options.isDirtyOnIncomplete = False
        node_options.requiresGeneratedInputs = False
        node_options.requiresSceneFile = False
        return pdg.result.Success


def registerTypes(type_registry):
    type_registry.registerNode(RunDemBones, pdg.nodeType.Processor, static_gen=True, label='Run Dem Bones', category='Right Up North')