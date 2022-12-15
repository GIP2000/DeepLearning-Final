import numpy as np
from gpt3Handler import get_top_response, rank_prompt
from arxix import get_paper_as_txt_and_abstract
import sys
from tqdm import tqdm
from time import sleep
from make_into_latek import put_into_latex
from random import randint
import re

def get_values(paper_id):

    if randint(1,15) == 5:
        return["Don't write your name. Did you read the paper? Be honest."]

    pars,abstract = get_paper_as_txt_and_abstract(paper_id)
    print(pars)

    np.random.shuffle(pars)

    # Not seeding with abstract just becasue it should be in there we can add it back later
    questions = []
    n_q = 0
    size = 0
    bar = tqdm(pars)
    for par in bar:
        if size >= 2000:
            print("BROKE EARLY too many questions to choose from.")
            break
        question = get_top_response(par, abstract)
        # sleep(5) # I hate rate limits
        if question.useful:
            size += len(" ".join(question.questions))
            n_q += len(question.questions)
            questions.append((par, question))
        bar.set_description(f"len = {size} / 2000: count {n_q}")
        bar.refresh()

    ranking = rank_prompt(questions).split('\n');
    print(ranking)
    ranking = [re.split('\d+ ?\.', q) for i,q in enumerate(ranking) if q != '']
    return [q[1] for i,q in enumerate(ranking)]

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("Usage: python main.py [paper_source] [output_file]")
        exit(1)
    paper_id = sys.argv[1]
    output_file = sys.argv[2]
    vals = get_values(paper_id)
    put_into_latex(vals, output_file)
