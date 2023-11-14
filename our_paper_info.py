import sys
sys.path.append(".")
import pandas as pd
import pickle
import os
from concurrent.futures import ProcessPoolExecutor
def read_our_info():
    """
    this function is used to organize our published paper in the following form:
    {paper_name:{our_authors:[author1, author2,..,],"module":['1','2','3','4','5'}}
    Note that module 1, 2,3,4,5 stand for datacenter performance, datacenter energy,
    datacenter scalability, edge/serverless, and others, respectively.
    Meanwhile, both : and - in the paper title is replace by '', and all letters are transformed into lower-case.
    :return:
    """
    paper_info = {}
    start_marker, end_marker = '“','”'
    for module_name in ['1','2','3','4','5']: # mark the module related info
        with open("./paper_doc/module_"+module_name,"r") as f:
            for line in f.readlines():
                if start_marker not in line:
                    continue
                author_info = line[:line.index(start_marker)].strip()
                # transform the title name
                title = line[line.index(start_marker)+1:line.index(end_marker)].strip().replace("-"," ").replace(":"," ")
                author_list_org = author_info.split(",")[:-1]
                author_list = []
                for author in author_list_org:
                    if "and" in author.strip():  # some authors are extracted as X and Y,
                        elems = author.split("and")
                        for elem in elems:
                            if len(elem) > 1:
                                author_list.append(elem.strip())  # separate the author names
                    else:
                        author_list.append(author.strip())
                paper_info[title.lower()] = {"our_authors": author_list, "module": module_name}
    pickle.dump(paper_info, open("our_paper_info_first.pkl", "wb"))
    return paper_info


def _save_cite_file(src_file_name, target_name, src_path):
    """
    This function is used to rename a specific file.
    :param src_file_name:
    :param target_name:
    :param src_path:
    :return:
    """
    with open("./our_paper_info_first.pkl","rb") as f:
        full_paper_info = pickle.load(f)

    target_folder = "./citation_rename_info/" + src_path
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)
    try:
        for full_name in full_paper_info:
            if full_name.startswith(target_name):
                data = pd.read_excel("./citation_info/" + src_path + "/" + src_file_name)[['paper_name','authors']]
                data.to_excel(target_folder+"/"+full_name+".xlsx")
                print(target_folder+"/"+full_name+".xlsx")
    except Exception as e:
        print(e)


def rename_cite_file(year):
    """
    This function is used to rename the author-list by the full paper title
    :param year: target year
    :return:
    """
    root_path = "author-list-"+str(year)+"-notification"
    authors_list = os.listdir("./citation_info/"+root_path+'/')
    exc = ProcessPoolExecutor(max_workers=25)
    for paper_file_name in authors_list:
        partial_title = paper_file_name[paper_file_name.index("-")+1:paper_file_name.index(".xlsx")].lower().replace("-"," ")
        exc.submit(_save_cite_file,paper_file_name,partial_title,root_path)
    exc.shutdown()
year = 2021
#rename_cite_file(year)
# => acm
import requests
url = 'https://dl.acm.org/doi/10.1145/3458864.3467681'
url_head = 'https://dl.acm.org/doi/pdf/'
idx = url.find('doi')
res = requests.get(url_head + url[idx + 4:])
if (res.status_code == 200):
    with open(("./PDF/mobisys"+ '/' + 'test.pdf'), 'wb') as f:
        print("ACM Downloading PDF... ")
        f.write(res.content)
        #df.at[index, 'download'] = True