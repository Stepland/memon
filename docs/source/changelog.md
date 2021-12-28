# Changelog

## v1.0.0

*(Merged with the changes from v1.0.0-rc.1 to be less confusing)*

### Overview
- BPM changes
- Per-chart + per-file timing
- `resolution` is made mostly obsolete by two things :
    - It's implicitly 240 if the key is missing
    - Beat fractions not covered by the resolution can be written using the new 3-int tuple mixed number form
- HAKUs (Beat markers)

### Details
- **Added**
    - Symbolic times such as `t` and `l` in notes can also now be expressed as a tuple of 3 ints representing a mixed number
    - Decimal numbers such as the offset or the bpm can now also be stored as strings to make it easier to preserve clean decimal notations
- **Changed**
    - In note objects :
        - `l` and `p` are now optional for tap notes
        - `p` now uses the 6-notation
    - `metadata` is now optional
    - In the metadata object :
        - `preview` can now also be a string, replacing `preview path`
        - Renamed `song title` to `title`
        - Renamed `music path` to `audio`
        - Renamed `album cover path` to `jacket`
        - All keys are now optional
    - In the preview object :
        - Renamed `position` to `start`
        - Renamed `length` to `duration`
    - In the chart object :
        - `level` can now also be a decimal number, either as a number literal or as a string
        - `level` is now optional
        - `level` can now be negative, it was mistakenly restricted to being positive in `v1.0.0-rc.1` as a part of turning it into a decimal value
        - `resolution` is now optional
        - `resolution` now has an implicit default value of 240 in case the key is missing from the chart object
    - Timing information is now stored in dedicated timing objects, one at the root of the memon file to act as a fallback, and one for each chart for per-chart timing info
    - In the timing object :
        - `offset` changed sign, it's now the time at which the first beat occurs in the audio file, instead of its opposite
        - `offset` now has an implicit default value of 0 in case no timing object in the file defines it
        - BPM changes can now be stored in the `bpms` array !
        - `hakus` allow storing special background bounce patterns
- **Removed**
    - In the metadata object :
        - `preview path` is now replaced with the polymorphic `preview`
        - `offset` is now replaced by the offset in timing objects
        - `BPM` is now replaced by the bpms in timing objects
- **Schema bugs**
    - `#/$defs/positiveDecimal` allowed for negative number literals, not anymore


## v0.3.0
- **Added**
    - `metadata.preview path` allows audio preview files to be specified

- **Changed**
    - Key requirements in the metadata object have been relaxed to only enforce `song title`, `artist`, `BPM` and `offset`

## v0.2.0
- **Added**
    - `metadata.preview` allows defining a section of the music file to be used as preview

## v0.1.0
- **Added**
    - `version` is now mandatory

- **Changed**
    - Renamed `metadata.jacket path` to `metadata.album cover path`
    - `data` is no longer an array of charts but an mapping of difficulty names to charts

- **Removed**
    - Chart objects no longer needs a `dif_name` key, its difficulty name is now given by its key in the data object