# Building Permissions

You can interactively build permissions with `pekora make`.

<div class="termy">

```console
$ pekora make

• Choose some permissions. Type to search. 
┌────────────────────────────────────────────────────┐
│<font color="#B67EBD">❯</font>   41/41 (0)                                       │
│<font color="#73ADF8">❯ Create Instant Invite</font>                             │
│  Kick Members                                      │
│  Ban Members                                       │
│  Administrator                                     │
│  Manage Channels                                   │
│  Manage Server                                     │
│  Add Reactions                                     │
└────────────────────────────────────────────────────┘

// This is an interactive prompt in the terminal, but I can't show you that here.
```

</div>

If you want to start the process with a set of permissions already pre-selected, you can pass a Discord permission
flag, integer value, or Pekora permission group to `pekora make`'s `--from` option.

That's pretty much it. Simple enough.