import os

class TextFileService:
    def save_file(self, folder_path, file_name, content):
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, "w") as file:
            file.write(content)
            
        return file_path
    
    def delete_file(self, folder_path, file_name):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            os.remove(file_path)
            return True
        else:
            return False
        
    def get_file_content(self, source_path, file_name = None):
        '''
        source_path = folder or file path where the content is stored;
        file_name = in case source_path is a folder, the file name can be specified here;
        '''
        file_path = source_path
        
        if file_name is not None:
            file_path = os.path.join(source_path, file_name)
        
        with open(file_path, "r") as file:
            return file.read()