# COMP211-Checkoff3
# NumPy: Scientific Computing & Memory Architecture

## About
I'm Xander Pak, and for COMP 211 Checkoff 3 I chose to do an AI discovery on NumPy since it aligns with what I want to get good at in the future involving machine learning and research. NumPy is basically the base that a lot of the data science tools in Python like Pandas, SciPy, scikit-learn, and TensorFlow are built on.

## What I explored
My initial questions were why NumPy, and why not just use what's given in C or just given in Python. That led me to how Python actually stores numbers compared to NumPy, and then to how Python can call C code using `ctypes`. To actually see the difference, I wrote the same dot product three ways (pure Python, my own C through `ctypes`, and NumPy) and timed them on two vectors of 10 million numbers each.

## Key discoveries
| Version | Time | Speedup |
|---|---|---|
| Pure Python | 0.212 s | 1x |
| C (ctypes) | 0.023 s | ~9x |
| NumPy (`np.dot`) | 0.0018 s | ~118x |

1. **Pure Python is slow because of how it stores numbers.** Every number is a 24-byte object on the heap instead of 8 bytes like in C, so every loop step Python has to unbox the numbers, check their types, and make a new object for the result, and it does that 10 million times.
2. **ctypes lets C use NumPy's memory without copying it.** Since a NumPy `float64` is laid out the same as a C `double`, Python can just hand C the starting address of the array and C reads straight from it.
3. **NumPy beat my own C code by about 13x.** This surprised me the most since I thought C would be the fastest. My C loop does one add at a time where each add waits on the one before it, while NumPy uses a BLAS library with SIMD that does multiple multiplications at once and keeps multiple running totals.

Overall I feel the biggest takeaway is that NumPy is basically a Python front door to compiled C, so you get to write simple Python but still get C speed or better.

## Code examples
Requirements: Python 3, NumPy, and a C compiler (`cc`, gcc, or clang).

- `cstuff.c` is a simple C dot product function using a `for` loop.
- `numpyimpl.py` loads the compiled C with `ctypes` and times the dot product in pure Python, C, and NumPy.

To run it:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cc -shared -fPIC -O2 -o cstuff.so cstuff.c
python numpyimpl.py
```

All three should print the same result (30000000.0), with Python the slowest and NumPy the fastest. The exact times will be different depending on the machine.

## Presentation
[Slides](slides.pdf)

## Resources
- [NumPy documentation](https://numpy.org/doc/stable/)
- [Python ctypes documentation](https://docs.python.org/3/library/ctypes.html)
- I also explored the topic with AI (Claude) by asking it to explain things like I am 14 years old and to pick apart my thought process when I got something wrong.
