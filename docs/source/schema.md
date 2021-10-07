# Schema
This page gives a top-down view of how a memon file is structured


## Root

```json
{
    "version": "x.y.z",
    "metadata": {},
    "data": {}
}
```
This is the root / top level structure of a memon file.

It's a json object with the following keys :

- **version**
    - string, required
    - Indicates the schema version this memon file uses, follows [semver](https://semver.org/). If a memon file does not have this key it's probably following the pre-semver format
- **metadata**
    - object, required
    - Contains the {ref}`metadata object <metadata>`
- **data**
    - object, required
    - Contains the {ref}`data object <data>`


(metadata)=
## Metadata

```json
{
    "song title": "",
    "artist": "",
    "music path": "",
    "album cover path": "",
    "BPM": 120.0,
    "offset": 0.0,
    "preview": {},
    "preview path": "",
}
```
Contains information that applies to the whole set of charts

- **song title**
    - string, required
- **artist**
    - string, required
- **music path**
    - string, optional
    - Path to the music file, *relative* to the memon file.
- **album cover path**
    - string, optional
    - Relative path to the jacket / album cover / album art to be shown in music select for example. usually a square image
- **BPM**
    - number, required
    - Song tempo in Beats per Minute.
- **offset**
    - number, required
    - In seconds, opposite of the time position of the first beat in the music file. For instance, if the first beat occurs at 0.15 seconds in the audio file, `offset̀` should be -0.15
- **preview**
    - object, optional
    - If present, contains a {ref}`preview object <preview>`
- **preview path**
    - string, optional
    - Path to a preview file to be played on loop at the music select screen. Alternative to the music sample described by `preview`.

(preview)=
## Preview

```json
{
    "position": 0.0,
    "length": 0.0,
}
```

Describes the part of the music file that's meant to be played on loop when previewing this song at the music select screen

- **position**
    - number, required
    - In seconds, start of the loop
- **length**
    - number, required
    - In seconds, duration of the loop

(data)=
## Data

```json
{
    "BSC": {},
    "ADV": {},
    "...": {},
    "My cool chart": {}
}
```

The data object maps difficulty names to {ref}`chart objects <chart>`.

Keys in this object are not fixed, they can be any string.

By convention, `"BSC"`, `"ADV"` and `"EXT"` are to be understood as the usual 3 levels found in jubeat. Other values are "edits" or bonus charts.

When sorting, difficulties may be presented in that order :

    BSC ➔ ADV ➔ EXT ➔ (everything else in alphabetical order)

(chart)=
## Chart

```json
{
    "level": 10.3,
    "resolution": 240,
    "notes" : []
}
```

- **level**
    - number, required
    - Chart level, can be an integer or a decimal value
- **resolution**
    - number, required
    - Greater than 0, always an integer
    - Number of ticks in a beat, denominator of all beat fractions. Usually 240
- **notes**
    - array, required
    - Array of {ref}`tap notes <tap-note>` and {ref}`long notes <long-note>` that make up the chart

(tap-note)=
## Tap Note

```json
{
    "n": 0,
    "t": 3600,
}
```

A classic note

- **n**
    - number, required
    - Integer between 0 and 15 inclusive
    - The note position, given this way :
      ```
      0  1  2  3
      4  5  6  7
      8  9 10 11
      12 13 14 15
      ```
- **t**
    - number, required
    - Integer greater or equal to 0
    - Note timing in ticks.

    It can be seen as the numerator of the beat fraction.

    A tick is a fraction of the beat, its duration is defined as 1/ the chart's resolution.
    For example if the resolution is 240, a tick lasts for 1/240th of a beat.

    For more info about measuring time in ticks ticks, see [bmson's docs](https://bmson-spec.readthedocs.io/en/master/doc/index.html#terminologies) (their docs refers to ticks as *pulses*).

(long-note)=
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

**n** and **t** are the same as in a {ref}`tap note <tap-note>`

- **l**
    - number, required
    - Integer greater than 0
    - Long note duration ("l" as in length ?!), in ticks
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