![memon logo](logo/memon-logo_packed__broken_line.svg)

*memo + json*

[![Docs](https://readthedocs.org/projects/memon-spec/badge/?version=latest&style=flat)](https://memon-spec.readthedocs.io/en/latest)

`.memon` is a new json-based jubeat chart set format designed to be easier to parse than existing "memo-like" formats (memo, youbeat, etc ...). The goal of this format is to allow for easier and faster creation of tools and simulators.

This repo provides [a description of the format](schema.json) using [draft 2020-12 JSONSchema](https://json-schema.org/)

Documentation is available [here](https://memon-spec.readthedocs.io/en/latest).

The documentation goes over the format in a more human-friendly way and gives some more information for those willing to create programs that read or write memon files

## Features
- Multiple charts per file
- Long notes
- BPM Changes
- Per-chart and Per-file timing
- Hakus (Beats Markers)
- Metadata
    - song title
    - artist
    - music file path
    - album cover path

## Projects that use memon
- [jujube](https://github.com/Stepland/jujube), a jubeat simulator
- [F.E.I.S](https://github.com/Stepland/F.E.I.S.), a GUI jubeat chart editor
- [jubeatools](https://github.com/Stepland/jubeatools), a CLI tool to convert between many different jubeat chart formats
- [memoncpp](https://github.com/Stepland/memoncpp), a C++ parser