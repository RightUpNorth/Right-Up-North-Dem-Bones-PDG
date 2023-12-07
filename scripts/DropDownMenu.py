import hou
import os
import json

def update_dropdown_menu(hda, folder_path):
    dropdown_items = []
    # Ensure folder exists
    if not os.path.isdir(folder_path):
        return

    # Read JSON files and gather data
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                item = data.get('name', 'Default Name')  # Adjust based on your JSON structure
                dropdown_items.append(item)

    # Find the dropdown menu parameter in your HDA
    dropdown_param = hda.parm('your_dropdown_param_name')  # Replace with your parameter's name

    # Update the dropdown menu items
    if dropdown_param:
        menu_items = []
        for item in dropdown_items:
            menu_items.extend([item, item])  # Menu requires (token, label) pairs
        dropdown_param.setMenuItems(menu_items)
        dropdown_param.setMenuLabels(dropdown_items)

# Usage example
node = hou.pwd()  # Get the current Houdini node
folder_path = '/path/to/your/json/files'  # Replace with your folder path
update_dropdown_menu(node, folder_path)