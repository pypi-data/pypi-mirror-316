import unittest

from src.nget import nget


class TestNGet(unittest.TestCase):
    def test_get_nested_dict_value(self):
        data = {"a": {"b": {"c": "value"}}}
        self.assertEqual(nget(data, ["a", "b", "c"]), "value")

    def test_get_nested_list_value(self):
        data = [[["value"]]]
        self.assertEqual(nget(data, [0, 0, 0]), "value")

    def test_get_nested_value_with_default(self):
        data = {"a": {"b": {}}}
        self.assertEqual(nget(data, ["a", "b", "c"], "default"), "default")

    def test_key_error(self):
        data = {"a": {"b": {}}}
        with self.assertRaises(KeyError):
            nget(data, ["a", "b", "c"])

    def test_index_error(self):
        data = [[[]]]
        with self.assertRaises(IndexError):
            nget(data, [0, 0, 1])

    def test_type_error(self):
        data = {"a": "value"}
        with self.assertRaises(TypeError):
            nget(data, ["a", "b"])

    def test_empty_keys(self):
        data = {"a": {"b": {"c": "value"}}}
        self.assertEqual(nget(data, []), data)

    def test_empty_structure(self):
        data = {}
        self.assertEqual(nget(data, ["a", "b", "c"], "default"), "default")

    def test_nonexistent_key_with_default(self):
        data = {"a": {"b": {"c": "value"}}}
        self.assertEqual(nget(data, ["a", "x"], "default"), "default")

    def test_nonexistent_index_with_default(self):
        data = [[["value"]]]
        self.assertEqual(nget(data, [0, 1], "default"), "default")

    def test_mixed_keys_and_indices(self):
        data = {"a": [{"b": "value"}]}
        self.assertEqual(nget(data, ["a", 0, "b"]), "value")

    def test_nested_none_value(self):
        data = {"a": {"b": None}}
        self.assertIsNone(nget(data, ["a", "b"]))

    def test_nested_false_value(self):
        data = {"a": {"b": False}}
        self.assertFalse(nget(data, ["a", "b"]))

    def test_nested_zero_value(self):
        data = {"a": {"b": 0}}
        self.assertEqual(nget(data, ["a", "b"]), 0)


if __name__ == "__main__":
    unittest.main()
