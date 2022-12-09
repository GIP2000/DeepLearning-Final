import numpy as np
from gpt3Handler import get_top_response, rank_prompt
from arxix import get_paper_as_txt_and_abstract
import sys
from tqdm import tqdm
from time import sleep

def main():
    if len(sys.argv) <= 1:
        print("Usage: python main.py [paper_source]")
        exit(1)

    paper_id = sys.argv[1]
    pars,_ = get_paper_as_txt_and_abstract(paper_id)

    np.random.shuffle(pars)

    # Not seeding with abstract just becasue it should be in there we can add it back later
    questions = []
    size = 0
    bar = tqdm(pars)
    for par in bar:
        if size >= 2000:
            print("BROKE EARLY too many questions to choose from.")
            break
        question = get_top_response(par)
        sleep(5) # I hate rate limits
        if question.useful:
            size += len(" ".join(question.questions))
            questions.append((par, question))
        bar.set_description(f"len = {size} / 2000: count {len(questions)}")
        bar.refresh()

    ranking = rank_prompt(questions).split("\n")
    for q in ranking:
        print(f"1. {q}")


if __name__ == '__main__':
    main()
