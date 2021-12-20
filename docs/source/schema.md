# Schema
This page gives a top-down view of how a memon file is structured


## Root

```json
{
    "version": "x.y.z",
    "metadata": {},
    "timing": {},
    "data": {}
}
```
This is the root / top level structure of a memon file.

It's a json object with the following keys :

- **version**
    - string, required
    - Indicates the schema version this memon file uses, follows [semver](https://semver.org/). If a memon file does not have this key it's probably following the pre-semver format
- **metadata**
    - object, optional
    - Contains the [metadata object](#metadata)
- **timing**
    - object, optional
    - Contains the default / fallback [timing object](#timing)
    - See [](other-things.md#multiple-timing-objects) for more details on the behavior this should have
- **data**
    - object, required
    - Contains the [data object](#data)


## Metadata

```json
{
    "title": "",
    "artist": "",
    "audio": "",
    "jacket": "",
    "preview": {},
}
```
Contains information that applies to the whole set of charts

- **title**
    - string, optional
    - Song title
- **artist**
    - string, optional
- **audio**
    - string, optional
    - Path to the music file, *relative* to the memon file.
- **jacket**
    - string, optional
    - Relative path to the jacket / album cover / album art to be shown in music select for example. usually a square image.
- **preview**
    - object or string, optional
    - Contains either a [preview object](#preview) or a path to a bms-style preview file


## Preview

```json
{
    "start": 0.0,
    "duration": 0.0,
}
```

Describes the part of the music file that's meant to be played on loop when previewing this song at the music select screen

- **start**
    - number or string, required
    - In seconds, start of the loop
    - Positive
    - Strings allowed for easier decimal representation preservation
- **duration**
    - number or string, required
    - In seconds, duration of the loop
    - Strictly positive
    - Strings allowed for easier decimal representation preservation


## Timing

```json
{
    "offset": 0,
    "resolution": 240,
    "bpms": []
}
```

Describes the relationship between seconds in the audio file and symbolic time (time measured in beats)

- **offset**
    - number or string, optional
    - If the key is missing, defaults to 0
    - In seconds, time at which the first beat occurs in the music file.
      
      For instance, if the first beat occurs at 0.15 seconds in the audio file, the offset should be the number literal `0.15`, or the string `"0.15"` if the tools used can't keep a clean decimal representation when using json number literals.
- **resolution**
    - integer, optional
    - Greater than 0, always an integer
    - If the key is missing, defaults to 240
    - Number of ticks in a beat for the bpm events defined in this timing object, if some bpm events define a beat using a single integer, this is the implicit fraction denominator to use to convert the integer number of ticks to a fractional number of beats.
- **bpms**
    - array, optional
    - If the key is missing, defaults to

        ```json
        [{"beat": 0, "bpm": 120}]
        ```

    - Array of [BPM events](#bpm)

Timing objects can appear in multiple places in a memon file. The section [](other-things.md#multiple-timing-objects) explains how to deal with them.

## BPM

```json
{
    "beat": 0,
    "bpm": 120
}
```

Defines a change in tempo measured in beats per minutes happening at a specific symbolic time (measured in beats)

- **beat**
    - [symbolic time](#symbolic-time), required
    - Beat at which the tempo changes
- **bpm**
    - number or string
    - Song tempo at the given beat, in Beats per Minute.
    - Striclty positive
    - Strings allowed for easier decimal representation preservation


## Data

```json
{
    "BSC": {},
    "ADV": {},
    "...": {},
    "My cool chart": {}
}
```

The data object maps difficulty names to [chart objects](#chart).

Keys in this object are not fixed, they can be any string.

By convention, `"BSC"`, `"ADV"` and `"EXT"` are to be understood as the usual 3 levels found in jubeat. Other values are "edits" or bonus charts.

When sorting, difficulties may be presented in that order :

    BSC ➔ ADV ➔ EXT ➔ (everything else in alphabetical order)


## Chart

```json
{
    "level": 10.3,
    "resolution": 240,
    "timing": {},
    "notes": []
}
```

- **level**
    - number or string, optional
    - Chart level, can be an integer or a decimal value, or even a string holding a decimal number
- **resolution**
    - integer, optional
    - Greater than 0, always an integer
    - If the key is missing, defaults to 240
    - Number of ticks in a beat for all the notes in the chart, see [](#symbolic-time)
- **timing**
    - [Timing object](#timing), optional
    - Chart-specific timing information
    - See [](other-things.md#multiple-timing-objects) for more details on the behavior this should have
- **notes**
    - array, required
    - Array of [tap notes](#tap-note) and [long notes](#long-note) that make up the chart


## Tap Note

```json
{
    "n": 0,
    "t": 3600,
}
```

A classic note.

- **n**
    - number, required
    - Integer between 0 and 15 inclusive
    - The note position, given this way :
      ```
      0  1  2  3
      4  5  6  7
      8  9  10 11
      12 13 14 15
      ```
- **t**
    - [Symbolic Time](#symbolic-time), required
    - Beat at which the note occurs


## Long Note

```json
{
    "n": 0,
    "t": 3600,
    "l": 10000,
    "p": 5
}
```

A classic long note, with a tail

- **n** : same as in a [tap note](#tap-note)
- **t** : same as in a [tap note](#tap-note)
- **l**
    - [Symbolic Time](#symbolic-time), required
    - If a number, strictly positive
    - If an array, `l[0]` and `l[1]` cannot both be zero at the same time
    - Long note duration in ticks or beats
- **p**
    - number, required
    - Integer between 0 and 11 inclusive
    - Tail starting position, relative to note position, counting from 0 to 11, spiraling out, clockwise, starting one square above the note
    
      Here the possible values have been laid out visually, `"■"` marks the note :
      ```
             8
             4
             0
      11 7 3 ■ 1 5 9
             2
             6
            10
      ```
    
      For example, `"p": 7` produces the following long note :
      ```
      ▷—■
      ```
    
      and `"p": 10` gives :
      ```
      ■
      |
      |
      △
      ```


## Symbolic Time

Either an integer like `0` or an array like `[0, 2, 3]`.

Represents a time point (or a duration) measured in *beats*


### As a number

- integer greater or equal to 0
- Time measured in *ticks* :

  Ticks are fractions of the beat.
  Using ticks implies a *resolution* is defined somewhere else in the file.
  The resolution defines how many ticks are in a beat.
  In other words if the resolution is 240, a tick lasts for 1/240th of a beat.
  
  For more info about measuring time in ticks, see [bmson's docs](https://bmson-spec.readthedocs.io/en/master/doc/index.html#terminologies) (their docs refers to ticks as *pulses*).


### As an array

- The array **MUST** have length 3
- The first and second elements are integers greater or equal to 0
- The third element is an integer greater than 0
- The array reprensents a time in beats as a [mixed number](https://en.wikipedia.org/wiki/Fraction#Mixed_numbers)

    If `a` is the array in question and we use the bracket notation for array access, the value represented by the array is the following :
    
    ```
    a[0] + (a[1] / a[2])
    ```

    For instance `[1, 2, 3]` represents 1 + 2/3, `[0, 1, 20]` represents 0 + 1/20.

    As it currently is, the schema allows for improper fractions (0 + 5/1) and non-reduced fractions (0 + 2/4)