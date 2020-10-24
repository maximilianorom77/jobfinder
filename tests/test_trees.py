"""
Tests for the jobfinder.trees module
"""
from unittest import TestCase
from jobfinder import trees
from jobfinder.trees import BinaryTree


class TestBinaryTree(TestCase):
    """
    Tests for the BinaryTree class
    """

    def test_new(self):
        """
        New must return instance of type BinaryTree
        """
        tree = trees.new()
        self.assertIsInstance(tree, BinaryTree)

    def test_insert_new_object(self):
        """
        Insert must return a new object
        """
        tree = trees.new()
        element = 1
        tree_2 = trees.insert(tree, element)
        self.assertIsNot(tree, tree_2)

    def test_insert_find_element(self):
        """
        After inserting element we can find it
        """
        tree = trees.new()
        element = 1
        tree_2 = trees.insert(tree, element)
        found = trees.find(tree_2, element)
        self.assertEqual(found, True)
        found = trees.find(tree_2, 2)
        self.assertEqual(found, False)
