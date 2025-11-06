# 🎧 MIT 6.101 – Audio Processing Lab (Fall 2025)

This repository contains my completed implementation of the **Audio Processing Lab** from [MIT 6.101: Fundamentals of Programming](https://py.mit.edu/fall25/labs/audio_processing).

All functionality has been fully implemented and verified:
- ✅ All provided **pytest** tests passed  
- ✅ **Pylint score:** 10/10  
- ✅ Organized structure with clear test and sound directories  

---

## 🧩 Overview

The Audio Processing Lab explores how digital audio is represented and manipulated using Python.  
Students implement several sound transformations using fundamental list and dictionary operations to model discrete-time signals.

---

## 🧠 Core Concepts

- Digital representation of sound samples  
- Sampling rate and amplitude scaling  
- Audio transformations (echo, reversal, mixing, speed adjustment)  
- File I/O for `.wav` data  
- Functional programming: immutability and pure functions  

---

## 🛠️ Implemented Features

| Function | Description |
|-----------|-------------|
| `load_wav(filename)` | Loads a `.wav` file and returns a sound dictionary. |
| `save_wav(sound, filename)` | Writes a sound dictionary to a `.wav` file. |
| `reverse(sound)` | Reverses the sound samples. |
| `mix(sound1, sound2, p)` | Blends two sounds by ratio `p`. |
| `echo(sound, num_echoes, delay, scale)` | Adds an adjustable echo effect. |
| `speed_up(sound, factor)` | Speeds up playback by the given factor. |
| `apply_gain(sound, factor)` | Adjusts volume without distortion. |
| `combine(sound1, sound2)` | Concatenates two sounds. |

All functions are **pure**, producing new sound objects rather than modifying existing ones.

---

## 📁 Directory Structure

<pre> audio_processing_lab/
│
├── .pytest_cache/ # Cached test data
├── .ruff_cache/ # Ruff linter cache (if used)
├── pycache/ # Compiled Python files
│
├── sounds/ # (Optional) Example .wav files for experimentation
├── test_inputs/ # Test input files provided by MIT
├── test_outputs/ # Expected output files for pytest comparison
│
├── lab.py # Main implementation file
├── test.py # Test suite (provided by MIT)
├── pylintrc # Custom linting configuration
└── README.md # Project documentation </pre>

---

## ✅ Testing and Linting


Run all provided tests:

<pre>pytest test.py </pre>


Expected output:

<pre>================== 100% tests passed ==================</pre>


Run Pylint:

<pre>pylint lab.py</pre>


Expected output:

<pre>Your code has been rated at 10.00/10</pre>


## ▶️ Example Usage
from lab import load_wav, echo, save_wav

sound = load_wav("sounds/input.wav")
processed = echo(sound, num_echoes=3, delay=0.4, scale=0.6)
save_wav(processed, "sounds/output_echo.wav")

## 📦 Requirements

Python 3.10+

pytest (for testing)

pylint (for code quality)

Install all dependencies:

pip install pytest pylint

🧾 License

This repository follows MIT’s educational fair-use guidelines.
All implementation work is my own unless explicitly attributed.
