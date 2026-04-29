import unittest
from src.wheel.generator import WheelGenerator

class TestWheel(unittest.TestCase):
    def test_gen(self):
        gen = WheelGenerator([1,2,3,4,5,6], 6)
        self.assertEqual(len(gen.generate_full_wheel()), 1)
