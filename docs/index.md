---
title: Pekora
description: A command-line calculator for Discord permission values
---

# Pekora

Pekora is a command-line calculator for Discord permission values. With it, you can calculate permission values, see
detailed information about the permissions a value represents, and interactively build your own
permissions.

## Background

> Permissions are a way to limit and grant certain abilities to users in Discord. A set of base permissions can be
> configured at the guild level for different roles. When these roles are attached to users, they grant or revoke
> specific privileges within the guild.
>
> — [Discord Developer Documentation](https://discord.com/developers/docs/topics/permissions)

Behind the scenes, Discord represents sets of permissions as integers, which are equivalent to the sum of the integer
values of the individual permissions they represent. For example, the value of `read_messages` is `1024`, and the value
of `send_messages` is `2048`, so the value of a permission set containing `read_messages` and `send_messages` is:

$$
1024 + 2048 = 3072
$$

Pekora provides a human-friendly interface to perform these calculations from the comfort of your terminal. Check
out this quick example:

<div class="termy">

```console
$ pekora calc "read_messages + send_messages"
<font color="#97C981">╭─ Result ───────────────────╮</font>
<font color="#97C981">│ <font color="#5CB8C2">3072</font>                       │</font>
<font color="#97C981">╰────────────────────────────╯</font>
```

</div>

If that sounds appealing, you'll be pleased to know that Pekora can do much, much, more.

What are you waiting for? [Install Pekora](/install) today!
