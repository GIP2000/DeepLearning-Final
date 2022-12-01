import arxiv
import sys
import os
import subprocess

def get_paper_source_and_abstract(paper_id: str):
    paper_folder = f"paper_files_{paper_id}"
    filename=f"paper_{paper_id}.tar.gz"
    paper = next(arxiv.Search(id_list=[paper_id]).results())
    try:
        os.makedirs(paper_folder)
    except OSError:
        return paper_folder, paper.summary
    os.system(f'rm -rf ./{paper_folder}/*')
    paper.download_source(filename=filename)
    os.system(f"tar -xvf {filename} -C {paper_folder}")
    os.remove(filename)
    return paper_folder, paper.summary


def detex(folder: str) -> [str]:
    files_as_txt = []
    for file in os.listdir(folder):
        if not file.endswith(".tex"):
            continue
        txt = subprocess.run(["pandoc","--from","latex","--to","plain","--no-highlight","--katex",f"{os.getcwd()}/{folder}/{file}"]
                             , stdout=subprocess.PIPE).stdout
        txt_l = txt.split(b'\n\n')
        txt_lf = []
        for t in txt_l:
            ts = t.strip()
            if ts != b'' and len(ts.split(b' ')) > 10:
                txt_lf.append(str(ts))
        if len(txt_lf) == 0:
            continue
        files_as_txt += txt_lf
    return files_as_txt



def get_paper_as_txt_and_abstract(paper_id) -> ([str], str):
    folder_name, abstract = get_paper_source_and_abstract(paper_id)
    return detex(folder_name), abstract

# fake unit tests
if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python arxix.py [paper_id]")
        exit(-1)
    txt = get_paper_as_txt_and_abstract(sys.argv[1])
    print(txt)
