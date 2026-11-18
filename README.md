# COMP211-Checkoff3
# Why NumPy Is So Fast: Python vs. C vs. NumPy

## About
I'm a student in COMP 211, and for Checkoff 3 I chose to do an AI discovery on NumPy. I picked NumPy because it aligns with what I want to get good at in the future involving machine learning and research, and NumPy is basically the base that a lot of the ML tools in Python are built on top of.

## What I explored
My starting questions were why NumPy, why not just use what's given in C or what's given in Python, and what the advantage of incorporating it is for coding and practical applications. From there the exploration went in a couple of directions:

- **Why is NumPy fast?** This led me to how Python actually stores numbers in a list compared to how NumPy stores them in an array.
- **How does Python store numbers?** Every number in a Python list is its own object somewhere in memory, and the list just holds pointers to them, while NumPy keeps the raw numbers packed right next to each other like a C array.
- **How does Python talk to C?** This led me to `ctypes`, which let me compile my own C function and call it straight from Python using the same memory a NumPy array already has.

To actually see the difference instead of just reading about it, I wrote the same dot product three ways (pure Python, my own C through `ctypes`, and NumPy) and timed them against each other.

## Key discoveries
Benchmark: dot product of two vectors with 10,000,000 numbers each, run on my laptop (Apple Silicon Mac, Python 3.15). Times change a little each run and will be different on other machines.

| Version | Time | Compared to pure Python |
|---|---|---|
| Pure Python | ~0.20–0.26 s | 1x |
| C (ctypes) | ~0.027 s | ~7–10x faster |
| NumPy (`np.dot`) | ~0.003 s | ~70–90x faster |

1. **Pure Python is slow because of how it stores and handles numbers, not because the math is hard.** Each loop step Python has to go grab two number objects from different places in memory, check what type they are, multiply them, and then make a brand new object for the result. That overhead happens 10 million times, and it adds up to most of the time.

2. **Moving the same loop into C made it around 7–10x faster.** The C code is literally the same loop, but C already knows every value is a `double` sitting next to the others in memory, so it skips all the checking Python does. Using `ctypes`, I could hand C a pointer to the NumPy array's memory directly so nothing had to be copied over.

3. **NumPy was still around 10x faster than my own C code.** This was the most surprising part to me since I assumed C would be the fastest. `np.dot` doesn't run a simple loop like mine, it hands the work to a math library (BLAS) that has been tuned for the hardware, using things like SIMD instructions that do multiple multiplications at once. Even when I compiled my C with `-O3` optimizations it only went down to about 0.019 s, so NumPy still won by about 6x. So the real advantage of NumPy is that you get C-level (and better) speed while still writing simple Python.

## Code examples
**Requirements:** Python 3, NumPy, and a C compiler (gcc or clang).

### `cstuff.c`
A plain C function `dot_product` that takes two arrays of doubles and their length and returns the dot product with a regular `for` loop.

### `numpyimpl.py`
Loads `cstuff.so` with `ctypes`, tells Python what types the C function takes and returns, and then times the dot product three ways: a pure Python loop over lists, the C function (passing it pointers to NumPy arrays), and `np.dot`.

### How to run
1. Set up a virtual environment and install NumPy:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Compile the C code into a shared library (a compiled `cstuff.so` for macOS is already in the repo, but recompile it if you're on a different machine):
   ```bash
   gcc -shared -fPIC -o cstuff.so cstuff.c
   ```
3. Run the benchmark:
   ```bash
   python numpyimpl.py
   ```

### Expected output
All three should get the same result (30,000,000.0), with pure Python the slowest and NumPy the fastest. The exact times will depend on your machine:
```
Initializing vectors of length 10,000,000...

Pure Python: 0.20127 seconds 	(Result: 30000000.0)
C (ctypes):  0.02703 seconds 	(Result: 30000000.0)
NumPy:       0.00282 seconds 	(Result: 30000000.0)
```

## Presentation
<!-- TODO: add the slides file to the repo and link it here, e.g. [Slides](slides.pdf) -->

## Resources
- [NumPy documentation](https://numpy.org/doc/stable/), mainly the parts on `ndarray` and `numpy.dot`
- [Python `ctypes` documentation](https://docs.python.org/3/library/ctypes.html)
- I explored the topic with AI (Claude), asking it to explain the concepts like I am 14 years old, picking apart my own thought process, and looking up terms it used that I didn't know yet. My full reflection on how that went is in my checkoff submission.
