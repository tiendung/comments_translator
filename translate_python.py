#!/usr/bin/python
'''This module provides methods for parsing comments from Python scripts.'''
import io
import re
import tokenize
import translators as ts # pip install translators


'''This is a mutiple line comment 
with # single line comment trap
'''

# Trap mutliple line comment """ """ inside a single line comment

"""Extracts a list of comments from the given Python script.

Comments are identified using the tokenize module. Does not include function,
class, or module docstrings. All comments are single line comments.

Args:
code: String containing code to extract comments from.
Returns:
Python list of common.Comment in the order that they appear in the code.
Raises:
tokenize.TokenError
"""

python_code = open('translate_python.py').read()
translated_python_code = ""

## Handle multiple line comments
mutiple_line_comment_re = r"""^\s*('''(.*?)'''|\"\"\"(.*?)\"\"\")"""
found = re.search(mutiple_line_comment_re, python_code, flags=re.S | re.MULTILINE)
while found:
    # print(found.group(), found.span(), found.start(), found.end()) # DEBUG
    comment = found.group()
    prefix = comment[:3]
    suffix = comment[-3:]

    comment = ts.translate_text(comment[3:-3], translator='google', 
        from_language='auto', to_language='vi')
    comment = prefix + comment + suffix

    translated_python_code += python_code[:found.start()] + comment
    python_code = python_code[found.end():]
    found = re.search(mutiple_line_comment_re, python_code, flags=re.S | re.MULTILINE)

translated_python_code += python_code
# print(translated_python_code) # DEBUG

## Handle single line comments
translated_python_code = translated_python_code.strip() + "\n"
tokens = tokenize.tokenize(io.BytesIO(translated_python_code.encode()).readline)
lines = translated_python_code.split("\n")
translated_python_code = ""
prev_line = 0
for toknum, tokstring, tokloc, _, _ in tokens:
    if toknum is tokenize.COMMENT:
        # print(toknum, tokstring, tokloc) # DEBUG
        line, pos = tokloc
        # print(line, pos, tokstring) # DEBUG
        tokstring = ts.translate_text(tokstring, translator='google', \
            from_language='auto', to_language='vi')

        if prev_line < line - 1:
            translated_python_code += "\n".join(lines[prev_line:line-1]) + "\n"
        translated_python_code += lines[line-1][0:pos]
        translated_python_code += tokstring + "\n"

        prev_line = line

if prev_line < len(lines):
    translated_python_code += "\n".join(lines[prev_line:len(lines)])
print(translated_python_code)