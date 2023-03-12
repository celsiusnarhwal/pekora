---
description: Get detailed information about a permission
---

# Reading Permissions

You use `pekora read` to get detailed information about the permissions a value represents.

<div class="termy">

```console

$ pekora read 66061056

┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Flag                 ┃ Name               ┃ Value    ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ priority_speaker     │ Priority Speaker   │ 256      │
│ stream               │ Video              │ 512      │
│ connect              │ Connect            │ 1048576  │
│ speak                │ Speak              │ 2097152  │
│ mute_members         │ Mute Members       │ 4194304  │
│ deafen_members       │ Deafen Members     │ 8388608  │
│ move_members         │ Move Members       │ 16777216 │
│ use_voice_activation │ Use Voice Activity │ 33554432 │
└──────────────────────┴────────────────────┴──────────┘
                 Derived from: 66061056        
                 
// Note: It will look prettier than this in your actual terminal.

```

</div>

Like `pekora calc`, `pekora read` accepts Discord permission flags, integer valeus, and Pekora permission groups. 

`pekora read`'s output is separated into three categories:

- **Flag**: The name of the permission in the Discord API.
- **Name**: The user-facing name of the permission.
- **Value**: The integer value of the permission.


## Filtering the Output



!!! tip inline end "Filtering multiple categories"
    You can pass multiple categories to `--include` or `--exclude` by specifying the respective option multiple times.

You can filter the output of `pekora read` with the `--include` and `--exclude` options. The `--include` options 
lets you specify what categories should be included, implicitly excluding everything else; the `--exclude` options
lets you specify what categories should be excluded.

Both options take the same argument: one of `flag`, `name`, or `value`, based on the category you want to include 
or exclude.

!!! tip "Aliases and shorthands"
    You can use `--with` and `--without` in place of `--include` and `--exclude`, if you like.

    Also, you can use `-i` as shorthand for `--include`/`--with`, and `-e` and `-x` as shorthand for `--exclude`/`--without`.

!!! warning
    `--include` and `--exclude` *aren't* mutually exclusive, but if you pass the same category to both, `--exclude`
    will take precedence.

## Using JSON

If tables aren't your thing, `pekora read` can alternatively produce its output as JSON. All you have to do is pass
the `--json` option.

<div class="termy">

```console
$ pekora read 66061056 --json

{
  "derived_from": 66061056,
  "permissions": [
    {
      "flag": "priority_speaker",
      "name": "Priority Speaker",
      "value": "256"
    },
    {
      "flag": "stream",
      "name": "Video",
      "value": "512"
    },
    {
      "flag": "connect",
      "name": "Connect",
      "value": "1048576"
    },
    {
      "flag": "speak",
      "name": "Speak",
      "value": "2097152"
    },
    ...
```

</div>

!!! tip
    `--include` and `--exclude` work with JSON-formatted output, too.

## Using Calculations

You can use the output of `pekora calc` as input to `pekora read`.

<div class="termy">

```console
$ pekora calc "embed_links + use_external_emojis" -r | pekora read -

┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Flag            ┃ Name                     ┃ Value       ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ embed_links     │ Embed Links              │ 16384       │
│ external_emojis │ Use External Emoji       │ 262144      │
│ manage_threads  │ Manage Threads and Posts │ 17179869184 │
└─────────────────┴──────────────────────────┴─────────────┘
                 Derived from: 17180147712   
```

</div>

`pekora calc`'s `-r`, or `--raw`, option tells it to output its without any fancy formatting. The `-` argument to 
`pekora read` tells it to use the output of the previous command as its input.

!!! danger

    `pekora calc -r` is **mandatory** when piping its output to `pekora read`.
