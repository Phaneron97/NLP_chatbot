import unittest
import numpy as np
from vectordb import VectorDB

class TestVectorDB(unittest.TestCase):

    def setUp(self):
        self.vectordb = VectorDB()

    def test_add_item(self):
        item = ("Sample text", "Section 1", "file1.pdf")
        vector = np.array([1, 2, 3])
        
        self.vectordb.add_item(item, vector)
        
        self.assertIn(item, self.vectordb.data)
        self.assertTrue(np.array_equal(self.vectordb.data[item], vector))

    def test_search(self):
        item1 = ("Sample text 1", "Section 1", "file1.pdf")
        vector1 = np.array([1, 2, 3])
        item2 = ("Sample text 2", "Section 2", "file2.pdf")
        vector2 = np.array([4, 5, 6])
        
        self.vectordb.add_item(item1, vector1)
        self.vectordb.add_item(item2, vector2)
        
        query_vector = np.array([1, 2, 3])
        
        best_match = self.vectordb.search(query_vector)
        
        self.assertEqual(best_match, item1)

    def test_search_no_items(self):
        query_vector = np.array([1, 2, 3])
        
        best_match = self.vectordb.search(query_vector)
        
        self.assertIsNone(best_match)

    def test_search_tie(self):
        item1 = ("Sample text 1", "Section 1", "file1.pdf")
        vector1 = np.array([1, 0, 0])
        item2 = ("Sample text 2", "Section 2", "file2.pdf")
        vector2 = np.array([0, 1, 0])
        
        self.vectordb.add_item(item1, vector1)
        self.vectordb.add_item(item2, vector2)
        
        query_vector = np.array([1, 1, 0])
        
        best_match = self.vectordb.search(query_vector)
        
        # In case of a tie, we expect the first item to be returned
        self.assertEqual(best_match, item1)

if __name__ == "__main__":
    unittest.main()
