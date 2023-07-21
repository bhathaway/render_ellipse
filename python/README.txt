  Run everything in one place, which is the same directly this README.txt lives in.

  To run unit tests:
  `python3 -m unittest discover`

  To run scripts in the "bin" directory:
  `python3 -m bin.make_ellipse -X 3 -Y 5 -A 30`
  `python3 -m bin.make_spiral_squares -S 15 -E 10 -A 0 -T 30`
  and so on.

  To test the pybind11 version of the module, for the time being copy it from build/cpp/*.so to
  tests folder, then run each test individually with `python3 ./test_polgon.py`, etc.
