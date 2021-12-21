# Other things to look out for

[JSON Schema](https://json-schema.org/) is great but by itself, a schema can't describe *everything* that makes a memon file "valid". The json schema file given in the github repository is meant to serve as a *reference* rather than a direct implementation, so some bits are left to be handled by the people adding memon compatibility into their software.

So, here are a few things to look out for or to keep in mind when reading or writing memon files :


## Notes

The note schema is fairly minimal. It does its best to eliminate most invalid notes by restricting the possible values of each key. However it still allows for the following false positives (notes that are conscidered valid by the schema but shouldn't) :


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

## Timing objects

### Duplicate BPMs

If there are several different bpms hapenning at the same beat in the `bpms` array, the last one is used.

For example, in this case :

```json
{
    "bpms": [
        {"beat": 0, "bpm": 120},
        {"beat": 0, "bpm": 124}
    ]
}
```

The BPM on beat zero is set to 124

### Duplicate HAKUs

The schema allows of duplicate hakus, implementations should deduplicate hakus by beat.


(multiple-timing-objects)=
### Multiple Timing Objects

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

Neither charts nor the root timing object define `resolution`, so the default value (`240` as specified in the schema) is used instead.

The timing object in `BSC` does not define `offset` so it uses the value `0.84` from the timing object at the root of the file instead.

`ADV` defines its own `offset` so it gets used instead of all the others