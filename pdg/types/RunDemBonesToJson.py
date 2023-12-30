import pdg
from pdg.processor import PyProcessor
from pdg import (envVar, strData, intData, floatData, resultData, hasStrData, hasIntData, hasFloatData, hasResultData, resultDataIndex, findResultData, findDirectResultData, floatDataArray, intDataArray, strDataArray, findData, findDirectData, input, workItem, kwargs)


class write_dembones_parms_to_json(PyProcessor):

    @classmethod
    def templateName(cls):
        return 'write_dembones_parms_to_json_template'

    @classmethod
    def templateBody(cls):
        return """{
            "name": "write_dembones_parms_to_json_template",
            "dataType": "genericdata",
            "parameters": [
            ]
        }"""

    def onAddInternalDependencies(self, dependency_holder, internal_items, is_static):
        return pdg.result.Success

    def onGenerate(self, item_holder, upstream_items, generation_type):
        import json
        
        # Called when this node should generate new work items from upstream items.
        #
        # self             -   A reference to the current pdg.Node instance
        # item_holder      -   A pdg.WorkItemHolder for constructing and adding work items
        # upstream_items   -   The list of work items in the node above, or empty list if there are no inputs
        # generation_type  -   The type of generation, e.g. pdg.generationType.Static, Dynamic, or Regenerate
        
        # Define the keys we expect in the work item JSON
        work_item_keys = [
            "nBones", "nInitIters", "nIters", "tolerance", "patience", "nTransIters",
            "bindUpdate", "transAffine", "transAffineNorm", "nWeightsIters", "nnz",
            "weightsSmooth", "weightsSmoothStep", "dbg"
        ]
        
        for upstream_item in upstream_items:
            new_item = item_holder.addWorkItem(parent=upstream_item)
        
            # Create a dictionary to store the work item data
            work_item_data = {}
        
            # Iterate over the keys and fetch the attribute values from the upstream item
            for key in work_item_keys:
                work_item_data[key] = new_item.attribValue(key)
        
            # Wrap the work item data in the desired structure
            json_data = {"work_item": work_item_data}
        
            # Convert the data to JSON format
            json_output = json.dumps(json_data, indent=2)
        
            # Define a file name (modify this as per your file naming convention)
            file_name = str(new_item.attribValue("dembones_json"))
        
            # Write the JSON data to a file
            with open(file_name, 'w') as f:
                f.write(json_output)
        
        return pdg.result.Success

    def onRegenerate(self, item_holder, existing_items, upstream_items, generation_type):
        return pdg.result.Success
    def onCookTask(self, work_item):
        # Called when an in process work item needs to cook. In process work items
        # are created by passing the  flag when constructing the item in
        # the Generate callback
        #
        # self              -   A reference to the current pdg.Node instance
        # work_item         -   The work item being cooked by this callback
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
    type_registry.registerNode(write_dembones_parms_to_json, pdg.nodeType.Processor, static_gen=True, label='Write Dembones Parms To Json', category='Custom')