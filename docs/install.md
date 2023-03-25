---
icon: fontawesome/solid/download
description: Learn how to install Pekora
---

# Installing Pekora

### :simple-pypi: With pipx <small>recommended</small> { #with-pipx data-toc-label="With pipx" }

[Install pipx](https://pypa.github.io/pipx/installation/), then run:

```bash
pipx install pekora # (1)!
```

1. If you prefer, you can also run Pekora ephemerally without installing it:
   ```bash
   pipx run pekora
   ```
   You'll have to do this *every* time you want to use Pekora, though.

### :simple-homebrew: With Homebrew <small>macOS and Linux only</small> { #with-homebrew data-toc-label="With Homebrew" }

[Homebrew](https://brew.sh) users can install Pekora from the [Houkago Tea Tap](https://github.
com/celsiusnarhwal/homebrew-htt).

```bash
brew tap celsiusnarhwal/htt
brew install pekora # (1)!
```

1. Alternatively, you can do:
   ```bash
   brew install celsiusnarhwal/htt/pekora
   ```

### :fontawesome-brands-python: With pip <small>or other Python package managers</small> { #with-pip data-toc-label="With pip" }

Just because you can doesn't mean you should. But you definitely can.[^1]

=== "pip"

    ```bash
    pip install pekora
    ```

=== "Poetry"

    ```bash
    poetry add pekora
    ```

=== "PDM"

    ```bash
    pdm add pekora
    ```

### :fontawesome-brands-git-alt: With Git <small>please reconsider</small> { #with-git data-toc-label="With git" }

Cloning Pekora from GitHub and building it from source is, technically speaking, an option.[^1]

[Install Poetry](https://python-poetry.org/docs/#installation), then clone Pekora's repository:

=== "Git"

    ```bash
    git clone https://github.com/celsiusnarhwal/pekora
    ```

=== "GitHub CLI"

    ```bash
    gh repo clone celsiusnarhwal/pekora
    ```

You'll have to install Pekora's dependencies yourself:

```bash
cd pekora && poetry install --only main
```

[^1]: Please don't open any issues or ask for any support if you choose to install Pekora this way.
