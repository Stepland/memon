# `.memon`
*memo + json*

[![Docs](https://readthedocs.org/projects/memon-spec/badge/?version=latest&style=flat)](https://memon-spec.readthedocs.io/en/latest)

`.memon` is a new json-based jubeat chart set format designed to be easier to parse than existing "memo-like" formats (memo, youbeat, etc ...). The goal of this format is to allow for easier and faster creation of tools and simulators.

This repo provides a bare description of the format using draft-07 JSON Schema

## Features
- Metadata *(soon to be extended for use in games)*
    - song title
    - artist
    - music file path
    - album cover path
    - **single BPM and offset** *(ETA for multiple timing points support is 1.0.0)*
- Multiple charts per file
- Long notes

## Implementations
- A reference parser is available [here](https://github.com/Stepland/memoncpp)
- [F.E.I.S](https://github.com/Stepland/F.E.I.S.) is a GUI jubeat chart editor that supports .memon files
- [jujube](https://github.com/Stepland/jujube) is a jubeat simulator that supports .memon files
