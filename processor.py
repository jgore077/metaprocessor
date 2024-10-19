import json
import os
from PIL import Image

class Processor():
  def __init__(self,metadata_path):
    self.metadata_path=metadata_path
    with open(metadata_path,'r',encoding='utf-8') as file:
      self.metadata=json.loads(file.read())

  def mutate(self,mutate_function,output_path):
    mutate_function(self.metadata)
    if output_path==self.metadata_path:
      raise FileExistsError("Cannot overwrite initial metadata file")
    with open(output_path,'w',encoding='utf-8') as outputfile:
      outputfile.write(json.dumps(self.metadata,indent=4))

  def validate_image(self, entry:dict, ignore_exception:bool)->bool:
    image_path = entry['file_path']
    absolute_path = os.path.abspath("../"+image_path)
    if os.path.exists(absolute_path):
      try:
        image = Image.open(absolute_path)
        image.verify()
      except Exception:
        if ignore_exception==False: 
          print(f"Image {absolute_path} is corrupted") 
        return False
    else:
      if ignore_exception==False:
        raise FileNotFoundError(f"Image path {absolute_path} does not exist")
      return False
    return True
    
  def validate_metadata(self, entry:dict, ignore_exception:bool)->bool:
      return True
  
  def integrity(self,ignore_exception=False)->bool:
    """
    Verifys the integrity of the metadata file and the images, ensuring that images exist and the images are not corrupted
    
    If ignore_exception=False upon an integrity violation an exception will be thrown. If true the function will return false if the file fails the integrity check or true if passing.
    """
    for entry in self.metadata.values():
      if not self.validate_image(entry, ignore_exception):
        return False
      if not self.validate_metadata(entry, ignore_exception):
        return False
    return True
  

if __name__=="__main__":
  processor=Processor('../metadata.json')
  
  # Example of functional program dictionary manipulation
  # def remove_descriptions(metadata:dict):
  #   for key in metadata:
  #     del metadata[key]["description"]
      
      
  # processor.mutate(remove_descriptions,'nodescriptions.json')
  processor.integrity()