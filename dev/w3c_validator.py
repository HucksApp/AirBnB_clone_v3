#!/usr/bin/python3
"""
W3C validator for Holberton School

For HTML and CSS files.

Based on 2 APIs:

- https://validator.w3.org/nu/
- http://jigsaw.w3.org/css-validator/validator


Usage:

Simple file:

```
./w3c_validator.py index.html
```

Multiple files:

```
./w3c_validator.py index.html header.html styles/common.css
```

All errors are printed in `STDERR`

Return:
Exit status is the # of errors, 0 on Success

References

https://developer.mozilla.org/en-US/

"""
import sys
import requests



def __print_stdout(msg):
    """Print message in STDOUT
    """
    sys.stdout.write(msg)


def __print_stderr(msg):
    """Print message in STDERR
    """
    sys.stderr.write(msg)


def __validate_html(file_path):
    """Start analyse of HTML file
    """
    data = open(file_path, "rb").read()
    headers = {'Content-Type': "text/html; charset=utf-8"}
    url = "https://validator.w3.org/nu/?out=json"
    r = requests.post(url, headers=headers, data=data)
    res = []
    messages = r.json().get('messages', [])
    for m in messages:
        res.append(f"[{file_path}:{m['lastLine']}] {m['message']}")
    return res


def __validate_css(file_path):
    """Start analyse of CSS file
    """
    data = {'output': "json"}
    files = {'file': (file_path, open(file_path, 'rb'), 'text/css')}
    url = "http://jigsaw.w3.org/css-validator/validator"
    r = requests.post(url, data=data, files=files)
    res = []
    errors = r.json().get('cssvalidation', {}).get('errors', [])
    for e in errors:
        res.append(f"[{file_path}:{e['line']}] {e['message']}")
    return res


def __run_analysis(file_path):
    """Start analyse of a file and print the result
    """
    errors_stat = 0
    try:
        result = None
        if file_path.endswith('.css'):
            result = __validate_css(file_path)
        else:
            result = __validate_html(file_path)

        if len(result) > 0:
            for msg in result:
                __print_stderr("{}\n".format(msg))
                errors_stat += 1
        else:
            __print_stdout("{}: OK\n".format(file_path))

    except Exception as e:
        __print_stderr("[{}] {}\n".format(e.__class__.__name__, e))
    return  errors_stat


def __files_stats():
    """Loop that analyses for each file from input arguments
    """
    nb_errors = 0
    for file_path in sys.argv[1:]:
        nb_errors += __run_analysis(file_path)

    return nb_errors


if __name__ == "__main__":
    """Main
    """
    if len(sys.argv) < 2:
        __print_stderr("usage: w3c_validator.py file1 file2 ...\n")
        exit(1)

    """execute tests, then exit. Exit status = numbers of errors (0 on success)
    """
    sys.exit(__files_stats())