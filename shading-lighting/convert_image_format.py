import bpy
import os

main_path = r'C:\Users\Luke\Desktop\Test Export\dds'
output_path = r'C:\Users\Luke\Desktop\Test Export\png'
existing_files = os.listdir(output_path)


for root, dirs, files in os.walk(main_path):
    for file in files:
        if file.endswith('.dds'):

            file_name = (os.path.splitext(file)[0] + ".PNG")        
            if file_name in existing_files:
                continue
            
            file_path = os.path.join(root,file)
            image = bpy.data.images.load(file_path)
            image.file_format = 'PNG'        
            filepath =  os.path.join(output_path, file_name)
            image.save_render(filepath)
            
            bpy.data.images.remove(image)
