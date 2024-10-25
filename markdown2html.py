#!/usr/bin/python3
"""
    a script markdown2html.py that takes an argument 2 strings:

    First argument is the name of the Markdown file
    Second argument is the output file name
    Requirements:

    If the number of arguments is less than 2:
    print in STDERR Usage: ./markdown2html.py README.md README.html and exit 1
    If the Markdown file doesn’t exist: print in STDER
    Missing <filename> and exit 1
    Otherwise, print nothing and exit 0
"""


if __name__ == "__main__":
    from sys import argv, stderr, exit
    if len(argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=stderr)
        exit(1)
    try:
        with open(argv[1]) as md_file:
            md = list(md_file)
    except FileNotFoundError:
        print("Missing {}".format(argv[1]), file=stderr)
        exit(1)
    ul_visited = False
    ol_visited = False
    para_visited = False
    with open(argv[2], 'w') as html_file:
        for line in md:
            line_split = line.split()
            try:
                if line_split[0]:
                    targ_num = len(line_split[0])
                    text = line[targ_num + 1: -1]
            except IndexError:
                if ol_visited:
                    html_file.write('</ol>\n')
                    ol_visited = False
                if ul_visited:
                    html_file.write('</ul>\n')
                    ul_visited = False
                if para_visited:
                    html_file.write('</p>\n')
                    para_visited = False
                continue
            if line.startswith('#'):
                if ol_visited:
                    html_file.write('</ol>\n')
                    ol_visited = False
                if ul_visited:
                    html_file.write('</ul>\n')
                    ul_visited = False
                if para_visited:
                    html_file.write('</p>\n')
                    para_visited = False
                out = '<h{}>{}</h{}>\n'.format(targ_num, text, targ_num)
                html_file.write(out)
            if line.startswith('-'):
                if ol_visited:
                    html_file.write('</ol>\n')
                    ol_visited = False
                if para_visited:
                    html_file.write('</p>\n')
                    para_visited = False
                if not ul_visited:
                    html_file.write('<ul>\n')
                    ul_visited = True
                out = '<li>{}</li>\n'.format(text)
                html_file.write(out)
            if line.startswith('*'):
                if ul_visited:
                    html_file.write('</ul>\n')
                    ul_visited = False
                if para_visited:
                    html_file.write('</p>\n')
                    para_visited = False
                if not ol_visited:
                    html_file.write('<ol>\n')
                    ol_visited = True
                out = '<li>{}</li>\n'.format(text)
                html_file.write(out)
            if not line.startswith(('#', '-', '*')):
                if ul_visited:
                    html_file.write('</ul>\n')
                    ul_visited = False
                if ol_visited:
                    html_file.write('</ol>\n')
                    ol_visited = False
                if not para_visited:
                    html_file.write('<p>\n')
                    para_visited = True
                if line_split[0][0].isupper():
                    html_file.write(line)
                else:
                    html_file.write('<br />\n{}'.format(line))
        if ul_visited:
            html_file.write('</ul>\n')
        if ol_visited:
            html_file.write('</ol>\n')
        if para_visited:
            html_file.write('</p>\n')
