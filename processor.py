import json

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
      
  def integrity(self,exception=True)->bool:
    """
    Verifys the integrity of the metadata file and the images, ensuring that images exist and the images are not corrupted
    
    If exception=True upon an integrity violation an exception will be thrown. If false the function will return false if the file fails the integrity check or true if passing.
    """
    pass
  

if __name__=="__main__":
  processor=Processor('../metadata.json')
  
  # Example of functional program dictionary manipulation
  def remove_descriptions(metadata:dict):
    for key in metadata:
      del metadata[key]["description"]
      
      
  processor.mutate(remove_descriptions,'nodescriptions.json')