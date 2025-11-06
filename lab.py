"""
6.101 Lab:
Audio Processing
"""

import os
import wave
import struct


# import typing  # optional import
# import pprint  # optional import

# No additional imports allowed!


def backwards(sound):
    """
    Returns a new sound containing the samples of the original in reverse
    order, without modifying the input sound.

    Args:
        sound: a dictionary representing the original mono sound

    Returns:
        A new mono sound dictionary with the samples in reversed order
    """
    in_samples = sound["samples"]
    rev_in_samples = in_samples[::-1]
    backwards_sound = {"rate": sound["rate"], "samples": rev_in_samples}
    return backwards_sound


def mix(sound1, sound2, p):
    """
    Returns a new sound containing the mix of two sounds.
    takes new sound samples would be given by:
            p * samples[sound1] + (1-p) * samples[sound1]

    Args:
        sound1: a dictionary representing the original mono sound
        sound2: a dictionary representing the original mono sound

    Returns:
        A new mono sound dictionary with the samples in sound1 and sound2 mixed
    """
    if (
        ("rate" not in sound1)
        or ("rate" not in sound2)
        or (sound1["rate"] != sound2["rate"])
    ):
        print("no")
        return None

    r = sound1["rate"]  # get rate
    sound_length = min(len(sound1["samples"]), len(sound2["samples"]))

    mixed_samples = []
    s1_samples, s2_samples = sound1["samples"], sound2["samples"]
    i = 0
    while i < sound_length:
        s1, s2 = p * s1_samples[i], (1 - p) * s2_samples[i]
        mixed_samples.append(s1 + s2)  # add sounds
        i += 1

    return {"rate": r, "samples": mixed_samples}  # return new sound


def echo(sound, num_echoes, delay, scale):
    """
    Compute a new sound consisting of several scaled-down and delayed versions
    of the input sound. Does not modify input sound.

    Args:
        sound: a dictionary representing the original mono sound
        num_echoes: int, the number of additional copies of the sound to add
        delay: float, the amount of seconds each echo should be delayed
        scale: float, the amount by which each echo's samples should be scaled

    Returns:
        A new mono sound dictionary resulting from applying the echo effect.
    """
    # Samples list consists of a number of sample measurements
    # Each sample measurement is recorded by repeatedly measuring air pressure
    # rate number of times

    # to introduce a delay of 1 second
    # rate measurements must be 0

    # to introduce a delay of n seconds
    # n * rate measurements must be zero

    samples_in_1delay = round(delay * sound["rate"])

    # the echoed sample with delays added
    echoed_samples = (samples_in_1delay * [0] * num_echoes) + len(sound["samples"]) * [
        0
    ]

    # first orignal sample added
    echoed_samples[: len(sound["samples"])] = sound["samples"][:]
    offset = samples_in_1delay
    for idx in range(1, num_echoes + 1):
        # add the scaled down sample
        scaled_sample = [sample * (scale**idx) for sample in sound["samples"]]
        echoed_samples[offset : offset + len(scaled_sample)] = [
            a + b
            for a, b in zip(
                echoed_samples[offset : offset + len(scaled_sample)], scaled_sample[:]
            )
        ]
        offset += samples_in_1delay
        # scale down next copy

    return {"rate": sound["rate"], "samples": echoed_samples}


def pan(sound):
    """
    Applies the "pan" effect to a Stereo Sound


    Args:
        * sound (dictionary) : a Stereo Sound represented as dictionary
            sound["rate"] gives sampling rate of the sound
            sound["left"] and sound["right"] give
            left and right samples of the sound respectively
    Returns:
        * sound (dictionary) : the orignal Stereo Sound
            with pan affect applied
            also represented as a disctionary
    """
    left_samples = sound["left"][::]
    right_samples = sound["right"][::]
    sample_len = len(left_samples)
    for idx in range(sample_len):
        left_scale = 1 - idx / (sample_len - 1)
        left_samples[idx] *= left_scale

        right_scale = idx / (sample_len - 1)
        right_samples[idx] *= right_scale

    return {"rate": sound["rate"], "left": left_samples, "right": right_samples}


def remove_vocals(sound):
    """
    Attempts to remove vocals from a Stereo sound

    Assumption:
    Some instruments were played into the left channel
     Other into the right channel

    Args:
        * sound (dictionary) : a Stereo Sound represented as dictionary
            sound["rate"]: (int) gives sampling rate of the sound
            sound["left"] (list):  and sound["right"] (list) give
            left and right samples of the sound respectively
    Returns
        * sound (dictionary) : a Mono Sound also represented as dictionary
          this sound has vocals in the input Stereo Sound removeds
    """
    left_samples = sound["left"][::]
    right_samples = sound["right"][::]
    sample_len = len(left_samples)
    no_vocal_samples = []
    for idx in range(sample_len):
        no_vocal_samples.append(left_samples[idx] - right_samples[idx])

    return {"rate": sound["rate"], "samples": no_vocal_samples}


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def load_wav(filename, stereo=False):
    """
    Given the filename of a WAV file, load the data from that file and return a
    Python dictionary representing that sound
    """
    file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    if stereo:
        left = []
        right = []
        for _ in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left.append(struct.unpack("<h", frame[:2])[0])
                right.append(struct.unpack("<h", frame[2:])[0])
            else:
                datum = struct.unpack("<h", frame)[0]
                left.append(datum)
                right.append(datum)

    if stereo:
        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = []
        for _ in range(count):
            frame = file.readframes(1)
            if chan == 2:
                left = struct.unpack("<h", frame[:2])[0]
                right = struct.unpack("<h", frame[2:])[0]
                samples.append((left + right) / 2)
            else:
                datum = struct.unpack("<h", frame)[0]
                samples.append(datum)

        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Given a dictionary representing a sound, and a filename, convert the given
    sound into WAV format and save it as a file with the given filename (which
    can then be opened by most audio players)
    """
    # make folders if they do not exist
    directory = os.path.realpath(os.path.dirname(filename))
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for left, right in zip(sound["left"], sound["right"]):
            left = int(max(-1, min(1, left)) * (2**15 - 1))
            right = int(max(-1, min(1, right)) * (2**15 - 1))
            out.append(left)
            out.append(right)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)

    car = load_wav("sounds/car.wav", stereo=True)

    write_wav(pan(car), "car_panned.wav")
