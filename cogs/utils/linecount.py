import codecs
import os
import pathlib


def linecount():
    path_to_search = "./"
    total = 0
    file_amount = 0
    for path, subdirs, files in os.walk(path_to_search):
        for name in files:
            if name.endswith(".py"):
                file_amount += 1
                with codecs.open(path_to_search + str(pathlib.PurePath(path, name)), "r", "utf-8") as f:
                    for l in list(f)[20:]:
                        if l.strip().startswith("#") or len(l.strip()) == 0:
                            pass
                        else:
                            total += 1

    avg = round(total / file_amount, 2)

    return f"I am made of {total:,} lines of Python, spread across {file_amount:,} files! That's an average of about" \
        f" {avg:,} lines per file."
linecount()
