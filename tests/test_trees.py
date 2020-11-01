"""
Tests for the jobfinder.trees module
"""
from unittest import TestCase
from jobfinder.trees import BinaryTree


class TestBinaryTree(TestCase):
    """
    Tests for the BinaryTree class
    """

    def test_insert_find_element(self):
        """
        After inserting element we can find it
        """
        tree = BinaryTree()
        element = 1
        tree.insert(element)
        found = tree.find(element)
        self.assertEqual(found, True)
        found = tree.find(element + 1)
        self.assertEqual(found, False)
