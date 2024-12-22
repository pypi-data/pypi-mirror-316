# libbash

**NOTE: This project is mostly functional, however there are a few minor bugs with the Bash source code causing issues with our API. Take a look at `test.py` to see which tests we are currently not testing because they will fail!**

`libbash` can be installed via pip: https://pypi.org/project/libbash/

## API

*The `libbash` module contains the following functions.*

`bash_to_ast` takes as input a file containing a bash script. It returns a `list` of `Command`s (see AST Classes below) representing the AST of the script. This function will throw an Exception if the script is invalid.

`ast_to_json` takes as input a `list` of `Command`s and returns a list of json-style object's representing the `Command`s (we say that a json-style object is either a `map` from `str` to json-style object or a `str`, `int`, `null`, or `list` of json-style object).

`ast_to_bash` takes as input a list of `Command`s and a filename and writes pretty-prints the script to the file. This function does not preserve line numbers, spacing, or other stylistic components.

`==` the equality operator has been implemented in the `Command` class. This operator ignores stylistic fields stored in the AST, and considers two `Commands` to be equal if they are structurally equal. In most cases, a round-trip from `ast_to_bash` to `bash_to_ast` will result in the same script, but this is not guaranteed. In a few occasional cases, this round trip will wrap certain commands in a `Group` command, which doesn't change the functionality of the script but does change the AST.

`run_tests` runs a testing suite on the above functions. If this fails, please consider creating a *New Issue* or making a *Pull Request* to fix the bug.

## Command Objects

*The `libbash.bash_command` module contains the classes which comprise our representation of a Bash command*

This library chooses to represent the AST of a bash script as a list of `Command` objects. To best understand what these objects look like, users are encouraged to understand the classes defined in [this directory](./libbash/bash_command). A great starting place to look at is the `Command` class in [command.py](./libbash/bash_command/command.py) class.

## Limitations

For a Bash parser to be completely correct, it would actually need to execute the entire script! Consider the following script:

```
current_hour=$(date +"%H")

if [ "$current_hour" -lt 12 ]; then
    alias while=random_string
else
    echo "It's after noon, no alias will be created."
fi

counter=1
while [ $counter -le 5 ]; do
    echo "Counter: $counter"
    ((counter++))
done
```

Whether `while` is aliased or not depends on the time of day that the script is run, and this affects the functionality of the `while` loop. This is because alias expansion is done
*before* parsing in Bash. As this example shows, determining alias expansions is not possible without executing a Bash script. Therefore, one can not expect any uses of `alias` or
other programs that change the script before parse-time to be reflected.

## Additional Documents

- [Difficulties Encountered During Development](https://docs.google.com/document/d/1Jn4z_QSTCoth_HvBtGE_DkAR0Z8O4B9eRKOKeV8njas/edit?usp=sharing) (just some notes I took)
- [Bash Source Code Parsing Outline](https://docs.google.com/document/d/1qZ4OX3BBX7esKu_wB-GmGvgEL5VFEFFTtifKwQdwTDw/edit?usp=sharing) (a brief guide on how parsing works in the Bash source)
