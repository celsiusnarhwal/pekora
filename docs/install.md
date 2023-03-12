# Installing Pekora

### With pipx <small>recommended</small> { #with-pipx data-toc-label="With pipx" }

[Install pipx](https://pypa.github.io/pipx/installation/), then run:

```bash
pipx install pekora
```

### With Homebrew <small>macOS and Linux only</small> { #with-homebrew data-toc-label="With Homebrew" }

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

### With pip <small>or other Python package managers</small>[^1] { #with-pip data-toc-label="With pip" }

Just because you can doesn't mean you should. But you definitely can.

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

### With Git <small>please reconsider</small>[^1] { #with-git data-toc-label="With git" }

Cloning Pekora from GitHub and building it from source is, technically speaking, an option.

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