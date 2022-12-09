import numpy as np
from gpt3Handler import get_top_response
from arxix import get_paper_as_txt_and_abstract
import sys
from tqdm import tqdm
from time import sleep
MAX = 15

def main():
    if len(sys.argv) <= 1:
        print("Usage: python main.py [paper_source]")
        exit(1)

    paper_id = sys.argv[1]
    pars,abstract = get_paper_as_txt_and_abstract(paper_id)

    np.random.shuffle(pars)

    questions = [(abstract,get_top_response(abstract))]
    counter = 0
    bar = tqdm(pars)
    for par in bar:
        if counter >= MAX:
            break
        question = get_top_response(par)
        sleep(5) # I hate rate limits
        if question.useful:
            counter += 1
            questions.append((par, question))
        bar.set_description(f"Found {counter} pars")
        bar.refresh()

    for i,(par, question) in tqdm(enumerate(questions)):
        print(f"{i}.{par}")
    print("=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>=>")
    for i,(par, question) in enumerate(questions):
        print(f" useful = {question.useful_reason} \item {question.questions}")


if __name__ == '__main__':
    main()
