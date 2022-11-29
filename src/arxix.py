import arxiv
import sys
import os
import subprocess


def get_paper_source(paper_id):
    paper_folder = f"paper_files_{paper_id}"
    filename=f"paper_{paper_id}.tar.gz"
    paper = next(arxiv.Search(id_list=[paper_id]).results())
    try:
        os.makedirs(paper_folder)
    except OSError:
        return paper_folder
    os.system(f'rm -rf ./{paper_folder}/*')
    paper.download_source(filename=filename)
    os.system(f"tar -xvf {filename} -C {paper_folder}")
    os.remove(filename)
    return paper_folder


def detex(folder):
    files_as_txt = []
    for file in os.listdir(folder):
        if not file.endswith(".tex"):
            continue
        txt = subprocess.run([f"{os.getcwd()}/detex/detex", f"{os.getcwd()}/{folder}/{file}"], stdout=subprocess.PIPE).stdout
        txt_l = txt.split(b'\n')
        txt_lf = []
        for t in txt_l:
            ts = t.strip()
            if ts != b'':
                txt_lf.append(ts)
        if len(txt_lf) == 0:
            continue
        files_as_txt += txt_lf
    return files_as_txt



def get_paper_as_txt(paper_id):
    folder_name = get_paper_source(paper_id)
    return detex(folder_name)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python arxix.py [paper_id]")
        exit(-1)
    txt = get_paper_as_txt(sys.argv[1])
    print(txt)
