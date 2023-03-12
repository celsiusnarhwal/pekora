# Calculating Permissions

You can calculate permissions with `pekora calc`. You already saw an example of this in the [introduction](/).

!!! note inline end
    By the way, these animated command prompts are used throughout the documentation. The formatting might look off
    if you're on a mobile device. Sorry!

<div class="termy">

```console
$ pekora calc "read_messages + send_messages"
<font color="#97C981">╭─ Result ───────────────────╮</font>
<font color="#97C981">│ <font color="#5CB8C2">3072</font>                       │</font>
<font color="#97C981">╰────────────────────────────╯</font>
```

</div>


`pekora calc` takes a special kind of math-like expression called a **Pekora expression**. Pekora expressions can
contain three types of values: **permission values**, **operators**, and **comparators**.

!!! tip
    You don't have to quote a Pekora expresssion that only contains one value. `pekora calc "3072"`, for instance, 
    is just as valid as `pekora calc 3072`.

## Permission Values

A permission value is any value that represents a Discord permissions. Permision values can be **Discord permission
flags**, **integers**, or **Pekora permission groups**.

### Discord permission flags

A Discord permission flag is a `snake_case` string that represdents a single permission. `read_messages` and
`send_messages`, as you've surely realized by now, are examples of Discord permission flags. Other flags include
`add_reactions`, `attach_files`, and `manage_messages`. If you're acquainted with Discord's permissions system (as
any Pekora user should be!), the names of these flags should be ringing bells.

<details>
<summary>All supported flags</summary>
<p>Pekora supports all flags listed below. Pekora tries to maintain parity with Discord in this regard; if you notice
something's missing, <a href="https://github.com/celsiusnarhwal/pekora/issues/new">open an issue</a>.</p>
    <ul><li><code>create_instant_invite</code></li>
    <li><code>kick_members</code></li>
    <li><code>ban_members</code></li>
    <li><code>administrator</code></li>
    <li><code>manage_channels</code></li>
    <li><code>manage_guild</code></li>
    <li><code>add_reactions</code></li>
    <li><code>view_audit_log</code></li>
    <li><code>priority_speaker</code></li>
    <li><code>stream</code></li>
    <li><code>view_channel</code></li>
    <li><code>read_messages</code></li>
    <li><code>send_messages</code></li>
    <li><code>send_tts_messages</code></li>
    <li><code>manage_messages</code></li>
    <li><code>embed_links</code></li>
    <li><code>attach_files</code></li>
    <li><code>read_message_history</code></li>
    <li><code>mention_everyone</code></li>
    <li><code>external_emojis</code></li>
    <li><code>use_external_emojis</code></li>
    <li><code>view_guild_insights</code></li>
    <li><code>connect</code></li>
    <li><code>speak</code></li>
    <li><code>mute_members</code></li>
    <li><code>deafen_members</code></li>
    <li><code>move_members</code></li>
    <li><code>use_voice_activation</code></li>
    <li><code>change_nickname</code></li>
    <li><code>manage_nicknames</code></li>
    <li><code>manage_roles</code></li>
    <li><code>manage_permissions</code></li>
    <li><code>manage_webhooks</code></li>
    <li><code>manage_emojis</code></li>
    <li><code>manage_emojis_and_stickers</code></li>
    <li><code>use_slash_commands</code></li>
    <li><code>use_application_commands</code></li>
    <li><code>request_to_speak</code></li>
    <li><code>manage_events</code></li>
    <li><code>manage_threads</code></li>
    <li><code>create_public_threads</code></li>
    <li><code>create_private_threads</code></li>
    <li><code>external_stickers</code></li>
    <li><code>use_external_stickers</code></li>
    <li><code>send_messages_in_threads</code></li>
    <li><code>start_embedded_activities</code></li>
    <li><code>moderate_members</code></li></ul>
</details>

### Integers

Integers are, well, integers. Like we covered in the [introduction](/), any set of Discord permissions can be
represented as an integer. You can use these integers in Pekora expressions.

!!! example "Technical Note"
    Behind the scenes, Discord permission flags and Pekora permission groups are converted to integers before a
    Pekora expression is evaluated.

<div class="termy">

```console
$ pekora calc "1024 + 2048"

<font color="#97C981">╭─ Result ───────────────────╮</font>
<font color="#97C981">│ <font color="#5CB8C2">3072</font>                       │</font>
<font color="#97C981">╰────────────────────────────╯</font>

$ pekora calc "3072 + embed_links + attach_files"

<font color="#97C981">╭─ Result ───────────────────╮</font>
<font color="#97C981">│ <font color="#5CB8C2">52224</font>                      │</font>
<font color="#97C981">╰────────────────────────────╯</font>
```

</div>

### Pekora permission groups

Pekora permission groups are shorthands for predefined sets of permissions. You can use them in Pekora expressions
with the syntax `pekora.<group>`, where `<group>` is the name of the desired Pekora permission group.

<div class="termy">

```console
$ pekora calc "pekora.text"

<font color="#97C981">╭─ Result ───────────────────╮</font>
<font color="#97C981">│ <font color="#5CB8C2">534723950656</font>               │</font>
<font color="#97C981">╰────────────────────────────╯</font>

$ pekora calc "(pekora.text - 3072) + create_instant_invite"

<font color="#97C981">╭─ Result ───────────────────╮</font>
<font color="#97C981">│ <font color="#5CB8C2">534723947585</font>               │</font>
<font color="#97C981">╰────────────────────────────╯</font>
```

</div>

A handful of Pekora permission groups exist. You can see them all and the permissions they include by expanding the
dropdown below.

<details>
<summary>All Pekora permission groups</summary>

<details>
    <summary><code>pekora.advanced</code></summary>
        <ul>
            <li>
            <code>administrator</code>
            </li>
        </ul>
</details>

<details>
    <summary><code>pekora.all</code></summary>
    <ul>
        <li><code>create_instant_invite</code></li>
        <li><code>kick_members</code></li>
        <li><code>ban_members</code></li>
        <li><code>administrator</code></li>
        <li><code>manage_channels</code></li>
        <li><code>manage_guild</code></li>
        <li><code>add_reactions</code></li>
        <li><code>view_audit_log</code></li>
        <li><code>priority_speaker</code></li>
        <li><code>stream</code></li>
        <li><code>view_channel</code></li>
        <li><code>read_messages</code></li>
        <li><code>send_messages</code></li>
        <li><code>send_tts_messages</code></li>
        <li><code>manage_messages</code></li>
        <li><code>embed_links</code></li>
        <li><code>attach_files</code></li>
        <li><code>read_message_history</code></li>
        <li><code>mention_everyone</code></li>
        <li><code>external_emojis</code></li>
        <li><code>use_external_emojis</code></li>
        <li><code>view_guild_insights</code></li>
        <li><code>connect</code></li>
        <li><code>speak</code></li>
        <li><code>mute_members</code></li>
        <li><code>deafen_members</code></li>
        <li><code>move_members</code></li>
        <li><code>use_voice_activation</code></li>
        <li><code>change_nickname</code></li>
        <li><code>manage_nicknames</code></li>
        <li><code>manage_roles</code></li>
        <li><code>manage_permissions</code></li>
        <li><code>manage_webhooks</code></li>
        <li><code>manage_emojis</code></li>
        <li><code>manage_emojis_and_stickers</code></li>
        <li><code>use_slash_commands</code></li>
        <li><code>use_application_commands</code></li>
        <li><code>request_to_speak</code></li>
        <li><code>manage_events</code></li>
        <li><code>manage_threads</code></li>
        <li><code>create_public_threads</code></li>
        <li><code>create_private_threads</code></li>
        <li><code>external_stickers</code></li>
        <li><code>use_external_stickers</code></li>
        <li><code>send_messages_in_threads</code></li>
        <li><code>start_embedded_activities</code></li>
        <li><code>moderate_members</code></li>
    </ul>
</details>

<details>
    <summary><code>pekora.all_channel</code></summary>
        <ul>
            <li><code>create_instant_invite</code></li>
            <li><code>manage_channels</code></li>
            <li><code>add_reactions</code></li>
            <li><code>priority_speaker</code></li>
            <li><code>stream</code></li>
            <li><code>view_channel</code></li>
            <li><code>send_messages</code></li>
            <li><code>send_tts_messages</code></li>
            <li><code>manage_messages</code></li>
            <li><code>embed_links</code></li>
            <li><code>attach_files</code></li>
            <li><code>read_message_history</code></li>
            <li><code>mention_everyone</code></li>
            <li><code>external_emojis</code></li>
            <li><code>connect</code></li>
            <li><code>speak</code></li>
            <li><code>mute_members</code></li>
            <li><code>deafen_members</code></li>
            <li><code>move_members</code></li>
            <li><code>use_voice_activation</code></li>
            <li><code>manage_roles</code></li>
            <li><code>manage_webhooks</code></li>
            <li><code>use_slash_commands</code></li>
            <li><code>request_to_speak</code></li>
            <li><code>manage_threads</code></li>
            <li><code>create_public_threads</code></li>
            <li><code>create_private_threads</code></li>
            <li><code>external_stickers</code></li>
            <li><code>send_messages_in_threads</code></li>
        </ul>
</details>

<details>
    <summary><code>pekora.general</code></summary>
        <ul>
            <li><code>manage_channels</code></li>
            <li><code>manage_guild</code></li>
            <li><code>view_audit_log</code></li>
            <li><code>view_channel</code></li>
            <li><code>view_guild_insights</code></li>
            <li><code>manage_roles</code></li>
            <li><code>manage_webhooks</code></li>
            <li><code>manage_emojis</code></li>
        </ul>
</details>

<details>
    <summary><code>pekora.membership</code></summary>
    <ul>
        <li><code>create_instant_invite</code></li>
        <li><code>kick_members</code></li>
        <li><code>ban_members</code></li>
        <li><code>change_nickname</code></li>
        <li><code>manage_nicknames</code></li>
    </ul>
</details>

<details>
    <summary><code>pekora.none</code></summary>
    <p>No permissions.</p>
</details>

<details>
    <summary><code>pekora.stage</code></summary>
    <ul>
        <li><code>request_to_speak</code></li>
    </ul>
</details>

<details>
    <summary><code>pekora.stage_moderator</code></summary>
    <ul>
        <li><code>mute_members</code></li>
        <li><code>move_members</code></li>
        <li><code>request_to_speak</code></li>
    </ul>
</details>

<details>
    <summary><code>pekora.text</code></summary>
    <ul>
        <li><code>add_reactions</code></li>
        <li><code>send_messages</code></li>
        <li><code>send_tts_messages</code></li>
        <li><code>manage_messages</code></li>
        <li><code>embed_links</code></li>
        <li><code>attach_files</code></li>
        <li><code>read_message_history</code></li>
        <li><code>mention_everyone</code></li>
        <li><code>external_emojis</code></li>
        <li><code>use_slash_commands</code></li>
        <li><code>manage_threads</code></li>
        <li><code>create_public_threads</code></li>
        <li><code>create_private_threads</code></li>
        <li><code>external_stickers</code></li>
        <li><code>send_messages_in_threads</code></li>
    </ul>
</details>

<details>
    <summary><code>pekora.voice</code></summary>
    <ul>
        <li><code>priority_speaker</code></li>
        <li><code>stream</code></li>
        <li><code>connect</code></li>
        <li><code>speak</code></li>
        <li><code>mute_members</code></li>
        <li><code>deafen_members</code></li>
        <li><code>move_members</code></li>
        <li><code>use_voice_activation</code></li>
    </ul>
</details>

</details>

!!! example "Technical Note"

    Pekora uses [Pycord](https://pycord.dev) for permission resolution. Each Pekora permission group corresponds to
    a method of the [`discord.Permissions`](https://docs.pycord.dev/en/stable/api/data_classes.html#permissions) class.

## Operators

Pekora, being a calculator, naturally supports a range of mathematical operations.

### Addition (`+`)

The addition operator adds two permission values together. Given the expression $A + B$, the resulting value will
represent all permissions that are in **either** $A$ or $B$.

!!! tip

    You can also use the union (`|`) operator.

### Subtraction (`-`)

The subtraction operator calculates the difference between two permission values. Given the expression $A -B$, the
resulting value will represent all permissions that are in $A$ but **not** in $B$.

### Intersection (`&`)

The intersection operator calculates the intersection[^1] between two permission values. Given the expression $A \& B$,
the resulting value will represent all permissions that are in **both** $A$ and $B$.

### Parentheses (`()`)

Pekora supports the use of parantheses to group parts of an expression together. They work exactly as you would expect.

!!! warning "Unsupported operations"
    Multiplication (`*`), division (`/`), and modulo (`%`) operations are not supported.
    
    Getting a little into the technical quirks of Pekora being a Python program, matrix multiplication (`@`) and 
    assignment (`=`) operations are also not supported.

[^1]: [https://en.wikipedia.org/wiki/Intersection_(set_theory)](https://en.wikipedia.org/wiki/Intersection_(set_theory))

## Comparators

Pekora supports the use of standard mathematical comparators[^2] to compare permission values with each other.

[^2]: These are technically called "relational operators". Pekora refers to them as "comparators".

!!! info

    So far, you've only seen Pekora expressions evalute to integers. However, Pekora expressions with comparators
    evaluate to either `True` or `False`.

### Equality (`==`)

The equality operator checks if two permission values are equal. Given the expression $A == B$, the resulting value will
be `True` if the permissions in $A$ are the same as those in $B$, and `False` otherwise.

### Inequality (`!=`)

The inequality operator checks if two permission values are not equal. Given the expression $A \neq B$, the resulting
value will be `True` if the permissions in $A$ are different than those in $B$ and `False` otherwise.

!!! warning "Equality comparators are lone wolves"

    If you use an equality (`==`) or inequality (`!=`) comparator in a Pekora expression, it must be the **only** 
    comparator in that expression.

### Greater Than (`>`)

The greater than operator checks if one permission value is a strict superset of another. Given the expression $A > B$,
the resulting value will be `True` if $A$ contains all the permissions in $B$ and at least one permission not in $B$,
and `False` otherwise.

#### Greater Than or Equal To (`>=`)

Given the expression $A \geq B$, the resulting value will be `True` if either $A > B$ or $A == B$ are
`True`, and `False` otherwise.

### Less Than (`<`)

The less than operator checks if one permission value is a strict subset of another. Given the expression $A < B$,
the resulting value will be `True` if all permissions in $A$ are also in $B$ and $B$ contains at least one permission
not in $A$, and `False` otherwise.

#### Less Than or Equal To (`<=`)

Given the expression $A \leq B$, the resulting value will be `True` if either $A < B$ or $A == B$ are
`True`, and `False` otherwise.

!!! tip "Combining comparators"

    You can use multiple `<`, `>`, `<=`, and `>=` comparators in a single Pekora expression (e.g. $A < B \leq C$).
    There's no limit to the number of comparators you can use.