import unittest

from src.model import Model

class TestModel(unittest.TestCase):
    
    def test_load_model_empty_object(self):
        model = Model()
        try:
            model.load_model("test/test_files/empty_object.obj")
        except Exception as e:
            self.assertNotEqual(e.message, "")

if __name__ == '__main__':
    unittest.main()