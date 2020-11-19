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

**version**
- string, required
- Indicates the schema version in use in this document

**metadata**
- object, required
- Contains the [metadata object](#metadata)

**data**
- object, required
- Contains the [data object](#data)


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

**song title**
- string, required

**artist**
- string, required

**music path**
- string, optional
- Path to the music file, *relative* to the memon file.
    
**album cover path**
- string, optional
- Path the jacket / album cover / album art to be shown in music select for example. usually a square image

**BPM**
- number, required
- Song tempo in Beats per Minute.

**offset**
- number, required
- In seconds, opposite of the time position of the first beat in the music file. For instance, if the first beat occurs at 0.15 seconds, `offset̀` should be -0.15

**preview**
- object, optional
- If present, contains a [preview object](#preview)

**preview path**
- string, optional
- Path to a preview file to be played on loop at the music select screen. Alternative to the music sample described by `"preview"`.


## Preview

```json
{
    "position": 0.0,
    "length": 0.0,
}
```

Describes the part of the music file that's meant to be played on loop when previewing this song at the music select screen

**position**
- number, required
- In seconds, start of the loop

**length**
- number, required
- In seconds, duration of the loop


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
    "notes" : []
}
```

**level**
- number, required
- Chart level, can be an integer or a decimal value

**resolution**
- integer, required
- Number of ticks in a beat, denominator of all beat fractions

**notes**
- array, required
- Array of [tap notes](#tap-note) and [long notes](#long-note)


## Tap Note

```json
{
    "n": 0,
    "t": 3600,
}
```

A classic note

**n**
- integer, required
- Between 0 and 15
- The note position, given this way :
  ```
   0  1  2  3
   4  5  6  7
   8  9 10 11
  12 13 14 15
  ```

**t**
- integer, required
- Greater or equal to 0
- Note timing in ticks


## Long Note

```json
{
    "n": 0,
    "t": 3600,
    "l": 10000,
    "p": 7
}
```

A classic long note, with a tail

**n** and **t** are the same as in a [tap note](#tap-note)

**l**
- integer, required
- Greater than 0
- Long note duration ("l" as in length ?!), in ticks

**p**
- integer, required
- Between 0 and 11 inclusive
- Tail starting position, relative to note position, counting from 0 to 11, couting spiraling out, clockwise, starting one square above the note

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