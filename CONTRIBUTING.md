# Some general guidelines for contributing to this project
(by a person who is annoyingly picky about consistency and style and so forth)

This guide is indended as a reference regarding style decisions and code
clarity. To be honest, if you don't follow these guidelines it's not really a
big deal, though I might fix it myself for my own sake. I highly recommend
that you create your own similar guidelines when become a project manager
yourselves. For now, this is what I've got. I'll probably add to this later.

## Style
Style matters! It improves readability, maintainability, and overal sanity.
In general, follow PEP8 guidelines regarding Python styling for variable names
(`snake_case`), class names (`PascalCase`), etc. There's really no need to
actually read this whole documentation, but if you want the whole PEP8 spec,
it's here: https://www.python.org/dev/peps/pep-0008/.

Regarding other style choices like spaces/tabs, line length, etc: I use
[Black](https://black.readthedocs.io/en/stable/) as a style checker and
reformatter. Warning: it is uncompromising. But the benefit is that all of our
code will be consistent across the board, which I think is helpful. If you're
wondering, Black uses four spaces for indents and attempts to limit lines to
80 characters, as per PEP8. It also uses double quotes exclusively. To install
Black, use pip: `pip3 install black`. To run, simply run `black [directory or
filename]` in a terminal. If it all goes well, you should see a message saying
"All done! ✨ 🍰 ✨".

## Other Things
If a program is intended to be run as a standalone script, i.e., you run it
in the terminal, it should have an `if __name__ == "__main__"` block. This
prevents the entirety of the script running in the event that it is imported
in a different Python file, and gives an indication to future programmers
that it is intended to be run as a script and that there is a specific entry
point that "gets everything going". For more information, I like
[this](https://www.geeksforgeeks.org/what-does-the-if-__name__-__main__-do/)
article.
