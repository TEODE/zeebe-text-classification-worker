import logging, os
from dotenv import load_dotenv
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

load_dotenv() # Loading env vars
logging.basicConfig(format='%(levelname)s:%(message)s', 
   level=int(os.environ["LOGGING_LEVEL"]))

class Classifier:
   
   __instance = None
   
   @staticmethod 
   def get_instance(model: str=None):
      """ Static access method. """
      if Classifier.__instance == None:
          logging.debug("Classifier.get_instance: instanciate the singleton Classifier") 
          if model:  
            Classifier(model)
          else:
            Classifier()
      logging.debug("Classifier.get_instance: retrieve the singleton Classifier instance")
      return Classifier.__instance
   
   @staticmethod 
   def destroy_instance():
      Classifier.__instance = None
      logging.debug("Classifier.destroy_instance: destroy the singleton Classifier") 


   def __init__(self, model: str=None):
      """ Virtually private constructor. """
      if Classifier.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         """
         Hugging Face zero-shot classification pipeline
         """ 
         logging.debug("Classifier.__init__: pipeline creation...")
         self.pipeline = pipeline("zero-shot-classification", 
                        model=model,
                        tokenizer=model)
         logging.debug("Classifier.__init__: created!")   
         Classifier.__instance = self
   

   def infer(self, sequence: str, candidate_labels: str) -> str:
        """
        Hugging Face zero-shot classification inference
        """   
        if not os.environ["HYPOTHESIS_TEMPLATE"]:
         hypothesis_template = "This example is {}."
        else:
         hypothesis_template = os.environ["HYPOTHESIS_TEMPLATE"]
        
        logging.info("Classifier.infer: infering for \"" + sequence + "\"...") 
        result = self.pipeline(sequence, candidate_labels, 
            hypothesis_template=hypothesis_template)
        logging.info("Classifier.infer: label=\"" + str(result["labels"][0]) + "\" (score=" 
         + str(result["scores"][0]) + ")")

        return result