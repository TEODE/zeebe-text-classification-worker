import unittest
from libs.classifier import Classifier

class TestClassifier(unittest.TestCase):

    def test_sequence_fr_inference(self):
        model = "models/camembert-base-xnli"
        classifier = Classifier.get_instance(model)
        sequence = "L'équipe de France joue aujourd'hui au Parc des Princes"
        candidate_labels = ["sport","politique","science"]
        output = classifier.infer(sequence, candidate_labels)
        self.assertEqual(output["labels"][0], "sport")
        self.assertEqual(output["scores"][0], 0.8595070838928223)
        # xlm-roberta-large-xnli score = 0.7845264077186584
    
    def test_sequence_ml_inference(self):
        model = "models/xlm-roberta-large-xnli"
        # forces recreate Classifier singleton
        Classifier.destroy_instance()
        classifier = Classifier.get_instance(model)
        sequence = "L'exécutif est reparti en campagne"
        candidate_labels = ["sport","politique","science"]
        output = classifier.infer(sequence, candidate_labels)
        self.assertEqual(output["labels"][0], "politique")
        self.assertEqual(output["scores"][0], 0.95650714635849)
        # camembert-base-xnli score = 0.922779381275177

if __name__ == '__main__':
    unittest.main()        