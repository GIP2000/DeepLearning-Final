import numpy as np
from gpt3Handler import get_top_response
from arxix import get_paper_as_txt_and_abstract
import sys


MAX = 5

def main():
    if len(sys.argv) <= 1:
        print("Usage: python main.py [paper_source]")
        exit(1)

    paper_id = sys.argv[1]
    pars,abstract = get_paper_as_txt_and_abstract(paper_id)
    # print(abstract)

    np.random.shuffle(pars)

    questions = [(abstract,get_top_response(abstract))]
    for par in pars[0:5]:
        print("starting next")
        question = get_top_response(par)
        questions.append((par,question))

    for i,(par, question) in enumerate(questions):
        print(f"{i}. input: {par}\n{question.strip()}")


if __name__ == '__main__':
    main()
