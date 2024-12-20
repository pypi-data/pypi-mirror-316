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
        
    def get_file_content(self, folder_path, file_name):
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, "r") as file:
            return file.read()