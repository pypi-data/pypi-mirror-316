import unittest
import json
from flatten_iterables import fi


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.data = {
            "dict": {"a": 42},
            "list": [42],
            "nested_dicts": {"a0": {"b0": 42, "b1": 23}},
            "nested_lists": [
                [
                    42,
                ],
            ],
            ...: 42,
        }

    def test_nested_dict(self) -> None:
        flat = json.dumps(fi.flatten(self.data["nested_dicts"]))
        self.assertEqual(flat, "{\"['a0']['b0']\": 42, \"['a0']['b1']\": 23}")

    def test_nested_list(self) -> None:
        flat = json.dumps(fi.flatten(self.data["nested_lists"]))
        self.assertEqual(flat, '{"[0][0]": 42}')

    def test_reference_path_representation(self) -> None:
        for k, v in fi.flatten(self.data).items():
            self.assertEqual(eval(f"{self.data}{k}"), v)


if __name__ == "__main__":
    unittest.main()
