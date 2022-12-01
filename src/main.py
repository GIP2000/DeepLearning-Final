import numpy as np
from gpt3Handler import get_top_response,get_all_responses
from arxix import get_paper_as_txt_and_abstract
import sys


MAX = 5

def main():
    if len(sys.argv) <= 1:
        print("Usage: python main.py [paper_source]")
        exit(1)

    paper_id = sys.argv[1]
    pars,abstract = get_paper_as_txt_and_abstract(paper_id)

    np.random.shuffle(pars)

    questions = [(abstract,[a for a in get_all_responses(abstract)])]
    for par in pars[0:5]:
        question = [a for a in get_all_responses(par)]
        questions.append((par,question))

    for i,(par, question) in enumerate(questions):
        print(f"{i}. input: {par}\n{'<>'.join(question)}")


if __name__ == '__main__':
    main()
