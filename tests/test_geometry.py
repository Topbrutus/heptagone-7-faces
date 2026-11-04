"""Tests des invariants du prisme heptagonal ouvert, sans GUI."""
import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generateur_7_cotes_7_faces import N, Prisme7FacesApp

class Var:
    def __init__(self, value): self.value=value
    def get(self): return self.value

def calculate(r="10", h="10"):
    app=Prisme7FacesApp.__new__(Prisme7FacesApp)
    app.radius_var=Var(r)
    app.height_var=Var(h)
    app.rotation_var=Var("0")
    app.precision_var=Var(40)
    return app.calculate()

class GeometryTests(unittest.TestCase):
    def test_topology(self):
        d=calculate()
        self.assertEqual(N,7)
        self.assertEqual((len(d["bottom"]),len(d["top"]),len(d["faces"])),(7,7,7))
        self.assertEqual(14-21+len(d["faces"]),0)
        self.assertTrue(all(len(f)==4 for f in d["faces"]))
    def test_perimeter(self):
        d=calculate("4.2","3.5")
        s=8.4*math.sin(math.pi/7)
        self.assertAlmostEqual(float(d["side_length"]),s,places=12)
        self.assertAlmostEqual(float(d["perimeter"]),7*s,places=12)
        for ring in (d["bottom"],d["top"]):
            for i in range(7):
                p,q=ring[i],ring[(i+1)%7]
                self.assertAlmostEqual(math.dist(tuple(map(float,p)),tuple(map(float,q))),s,places=12)
    def test_faces_area(self):
        d=calculate("2.2","6.7")
        self.assertAlmostEqual(float(d["lateral_area"]),float(d["perimeter"]*d["H"]),places=12)
        for i,face in enumerate(d["faces"]):
            self.assertEqual(tuple(face[0]),tuple(d["bottom"][i]))
            self.assertEqual(tuple(face[1]),tuple(d["bottom"][(i+1)%7]))
            self.assertEqual(tuple(face[2]),tuple(d["top"][(i+1)%7]))
            self.assertEqual(tuple(face[3]),tuple(d["top"][i]))
    def test_invalid(self):
        for r,h in (("0","10"),("10","-2"),("-1","1")):
            with self.assertRaises(ValueError): calculate(r,h)
if __name__=="__main__": unittest.main()
