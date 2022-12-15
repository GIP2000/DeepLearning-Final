from random import randint
def make_latex(input: [str]) -> str:
    return "\n".join(["\item " + s for s in input])

def put_into_latex(questions: [str], output_file: str):
    pim = randint(1,1_000_000)
    output_str = "\documentclass{article}\n\\usepackage[inline]{enumitem}\n\\usepackage{baked}\n\\usepackage[left=1.5in, right=2in, top=0.45in, bottom=0.45in]{geometry}\n\\begin{document}\nECE-467, Deep Learning - Quiz $" + str(pim) + "\pi$\\begin{enumerate}\n" + make_latex(questions) + "\n\end{enumerate}\n\end{document}"
    with open(output_file, 'w') as f:
        f.write(output_str)





