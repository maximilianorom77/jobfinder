from unittest import TestCase
from jobfinder import trees
from jobfinder.trees import BinaryTree


class TestTree(TestCase):

    def test_new(self):
        tree = trees.new()
        self.assertIsInstance(tree, BinaryTree)

    def test_insert(self):
        tree = trees.new()
        element = 1
        tree_2 = trees.insert(tree, element)
        self.assertIsInstance(tree, BinaryTree)
        self.assertIsNot(tree, tree_2)
