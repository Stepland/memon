# Validation

This page explains a few things to look out for when reading/writing memon files.

## Notes

The note schema is fairly minimal. It does its best to eliminate most invalid notes by restricting the possible values of each key. However it still allows for the following false positives (notes that are conscidered valid by the schema but shouldn't) :

### Off-Screen Tails

The encoding convention for long note tails in versions `0.y.z` of the format allows for some invalid notes. Nothing in the raw json schema prevents you from writing such a note :

```json
{ "n": 0, "t": 0, "l": 240, "p": 11 }
```

All the numbers are within the intervals defined in the schema, however this would correspond to a long note that would look like this :

```
▷——■□□□
   □□□□
   □□□□
   □□□□
```

Notice the tail starting outside the screen.

Parsers should **reject** such notes


### Uniqueness

The schema itself does not prevent the following cases from happening in the array of notes that make up the chart :

*Duplicate Notes*
```json
[
    { "n": 0, "t": 0 },
    { "n": 0, "t": 0 }
]
```

*A Tap Note and a Long Note on the same square at the same time*
```json
[
    { "n": 0, "t": 0 },
    { "n": 0, "t": 0, "l": 240, "p": 9 }
]
```

Parsers should only keep one note for each `(n, t)` couple


### Hitbox Overlap

*(This describes **hitbox** overlap, for marker animation overlap see {ref}`marker-animation-overlap`)*

This set of notes has another problem, but at first glance it's unclear why :

```json
[
    { "n": 0, "t": 0, "l": 10, "p": 5 },
    { "n": 0, "t": 5 }
]
```

The problem becomes obvious when the data is plotted on a timeline :

```
ticks       0   1   2   3   4   5   6   7   8   9   10  11  ...
note 1      █━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━█
note 2                          █
```

Here note 2 happens *during* note 1, on the same square. The "temporal" hitboxes overlap. This makes note 2 impossible to hit correctly without releasing note 1 first.

This variant can also happen :
```json
[
    { "n": 0, "t": 0, "l": 5, "p": 5 },
    { "n": 0, "t": 3, "l": 5, "p": 5 },
]
```
```
ticks       0   1   2   3   4   5   6   7   8   9   10  11  ...
note 1      █━━━━━━━━━━━━━━━━━━━█
note 2                  █━━━━━━━━━━━━━━━━━━━█
```

Here, two long notes overlap on the same square

To clarify, a long note *lasts* for the amount of ticks specified by its `L` key, this means there **cannot** be another note on the same square from `T` to `T+L`, inclusive.

Parsers should **reject** charts with these kinds of overlapping notes.

(marker-animation-overlap)=
### Marker Animation Overlap

Due to the duration of a marker animation, two notes whose hitboxes don't overlap can however happen too close to one another to allow both marker animations to appear separately. Most official jubeat charts avoid this (with some notable exceptions like [Polaris ADV](https://remywiki.com/Polaris#Trivia)).

Since this is mostly an implicit rule that's not strictly followed by official charts, parsers should **allow** notes with overlapping marker animation.


## Decimal values

If possible, non-integer values like `BPM` or `offset` should be manipulated using a [Decimal Data Type](https://en.wikipedia.org/wiki/Decimal_data_type) to preserve their original decimal representation. I think no one likes to see the BPM they defined as a clean `195.3` in the editor be stored as a messy `195.3000030517578125` in the file.

Be careful that the serialized values in the resulting file must still be *number litterals*, not strings.

- **Good**
  ```json
  { "BPM" : 195.3 }
  ```
- **Bad**
  ```json
  { "BPM": "195.3" }
  ```

This is not that easy. Python's standard module `json`, for instance, allows *deserializing* (reading) numbers in a json file as `decimal.Decimal` instances, but has no easy way of *serializing* (writing) `decimal.Decimal` instances as a json number litteral that respects the original representation.

A possible solution is to use the [simplejson](https://pypi.org/project/simplejson/) module as a near drop-in replacement for `json` and use the `use_decimal` options