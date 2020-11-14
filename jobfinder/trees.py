"""
The module to define trees
"""
from jobfinder.jobs import Job


class BinaryTree:
    """
    Standard binary tree
    """
    node = None

    def __init__(self, filters):
        self.left = None
        self.right = None
        self.value = None

    def insert(self, element: Job) -> 'BinaryTree':
        return self

    def find(self, element: Job):
        return True
