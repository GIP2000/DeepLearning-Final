def make_latex(input: [str]) -> str:
    return "\n".join(["\item " + s for s in input])

def put_into_latex(questions: [str], output_file: str):
    output_str = "\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{lineno}\n\\title{Quiz \#31415}\n\\author{Fake Chris}\n\linenumbers[314]\n\\begin{document}\n\maketitle\n\huge\n\\begin{enumerate}\n" + make_latex(questions) + "\end{enumerate}\n\end{document}"
    with open(output_file, 'w') as f:
        f.write(output_str)





