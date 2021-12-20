# Other things to look out for

[JSON Schema](https://json-schema.org/) is great but by itself, a schema can't describe *everything* that makes a memon file "valid". The json schema file given in the github repository is meant to serve as a *reference* rather than a direct implementation, so some bits are left to be handled by the people adding memon compatibility into their software.

So, here are a few things to look out for or to keep in mind when reading or writing memon files :

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

(marker-animation-overlap)=
### Marker Animation Overlap

Due to the duration of a marker animation, two notes whose hitboxes don't overlap can however happen too close to one another to allow both marker animations to appear separately. Most official jubeat charts avoid this (with some notable exceptions like [Polaris ADV](https://remywiki.com/Polaris#Trivia)).

Since this is mostly an implicit rule that's not strictly followed by official charts, parsers should **allow** notes with overlapping marker animation.


## Decimal values

If possible, non-integer values like `bpm` or `offset` should be manipulated using a [Decimal Data Type](https://en.wikipedia.org/wiki/Decimal_data_type) to preserve their original decimal representation. I think no one likes to see the BPM they defined as a clean `195.3` in the editor be stored as a messy `195.3000030517578125` in the file. If doing this is too hard with your language / library of choice, keep in mind that `1.0.0` allows strings instead :

- **Valid**
    
    ```json
    { "bpm" : 195.3 }
    ```

- **Valid since 1.0.0**
  
    ```json
    { "bpm": "195.3" }
    ```

## Multiple timing objects

memon version 1.0.0 introduced [timing objects](schema.md#timing) in two different places in the file, either at the root or in a chart.

All the keys in a timing object are optional, this is to allow for a chart to only redefine what is different from the default timing object.

In other words the timing object at the root acts as a fallback.

In general, when deciding what timing information applies to a given chart, timing objects should be searched in that order *for every key* :

- Chart-specific timing object
- Root timing object
- Default values defined by the schema

For instance in the following file :

```json
{
    "version": "1.0.0",
    "timing": {
        "offset": 0.84
    },
    "data": {
        "BSC": {
            "timing": {
                "bpms": [{"beat": 0, "bpm": 200}]
            },
            "notes": []
        },
        "ADV": {
            "timing": {
                "offset": 0.31,
                "bpms": [{"beat": 0, "bpm": 100}]
            },
            "notes": []
        },
    }
}
```

Neither `BSC` nor `ADV` define `resolution` in their timing info so the implicit default is used instead for both charts.

`BSC` defines no chart-specific `offset` so it uses the value `0.84` from the timing object at the root of the file instead.

`ADV` defines its own `offset` so it gets used instead of all the others