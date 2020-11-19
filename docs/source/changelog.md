# Changelog

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