"""
Unit tests for RegistryHolder and BlueNode.

Author: Kevin Fu
"""

import unittest

from gtsfm.ui.registry import RegistryHolder, BlueNode

class FakeImageLoader(BlueNode):
    """Test class."""

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._input_gray_nodes = ["Raw Images"]
        self._output_gray_nodes = ["Internal Data"]
        self._parent_plate = ""

class FakeOutputGTSFM(BlueNode):
    """Test class."""

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._input_gray_nodes = ["Internal Data"]
        self._output_gray_nodes = ["GTSFM Output"]
        self._parent_plate = "Processor"

class FakeOutputCOLMAP(BlueNode):
    """Test class."""

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._input_gray_nodes = ["Internal Data"]
        self._output_gray_nodes = ["COLMAP Output"]
        self._parent_plate = "Processor"

class TestRegistryUtils(unittest.TestCase):
    def test_registry_holder(self):
        """
        Ensure registry holder has at least the test case classes above. (Since
        classes are added to the registry when defined, more classes will exist
        than just these test classes.)
        """

        registry = RegistryHolder.REGISTRY

        expected_result = {
            "FakeImageLoader": FakeImageLoader,
            "FakeOutputGTSFM": FakeOutputGTSFM,
            "FakeOutputCOLMAP": FakeOutputCOLMAP,
            "BlueNode": BlueNode,
        }

        for cls_name, cls_type in expected_result.items():
            self.assertTrue(cls_name in registry)
            self.assertEqual(registry[cls_name], cls_type)

    def test_blue_node(self):
        """Verify that BlueNode stores data correctly."""

        expected_fake_image_loader_repr = "FakeImageLoader:\n\t input_gray_nodes: ['Raw Images'],\n\t output_gray_nodes: ['Internal Data'],\n\t parent_plate: \n"

        # the __repr__() in BlueNode depends on the @property methods, so this
        # verifies both work correctly
        self.assertEqual(repr(FakeImageLoader()), expected_fake_image_loader_repr)

if __name__ == "__main__":
    unittest.main()
