from queue import Empty
import pandas as pd
import os
import pickle

sheet_list = ['ieee_2022', 'ieee_2021', 'acm_2021']


def remove_prefix(name):
    if name[:3] == "Dr.":
        return name[4:]
    elif name[:5] == "Prof.":
        return name[6:]
    return name


def reverse(name):
    name_list = name.strip().split(' ')
    tmp = name_list[0]
    for i in range(len(name_list) - 1):
        name_list[i] = name_list[i + 1]
    name_list[len(name_list) - 1] = tmp
    return ' '.join(name_list)

def get_fellow_by_module(target_year):
    fellows = []

    for sheetname in sheet_list:
        reader = pd.read_excel("./fellow_list.xlsx", sheet_name=sheetname)
        for i in range(reader.shape[0]):
            name = remove_prefix(reader['name'][i]).replace('\n', '').replace('\xa0', ' ')
            if sheetname == 'acm_2021':
                name = reverse(name)
            fellows.append(name)

    authors_list = os.listdir('./citation_rename_info/author-list-'+target_year+'-notification/')
    with open("./our_paper_info_first.pkl", "rb") as f:
        our_paper_info = pickle.load(f)

    module_dict = {}
    # use a separate dict to store the citation info
    for k in range(5):
        module_dict['module_'+str(k+1)] = {'fellows': [], 'paper_name': [],"our_paper_name":[]}

    for list in authors_list:
        #result_dict = {'fellows': [], 'paper_name': []}
        print(list)
        if list.startswith("~$"):
            continue
        reader = pd.read_excel('./citation_rename_info/author-list-' + target_year + '-notification/' + list)
        # 1. check the module this paper belongs to
        module = our_paper_info[list[:list.index(".xlsx")]]["module"]

        # 2. check all the citation papers
        for i in range(reader.shape[0]):
            if reader['authors'][i] == "No information":
                pass
                # result_dict['fellows'].append("")
            else:
                author_list = reader['authors'][i].strip().split(', ')
                result = []

                if not set(author_list).isdisjoint(our_paper_info[list[:list.index(".xlsx")]]["our_authors"]):
                    continue
                for author in author_list:
                    if author in fellows: # find out the fellow authors
                        result.append(author)

                if len(result) == 0:
                    pass
                    # result_dict['fellows'].append("")
                else: # our paper $list$ is cited by a fellow in his/her paper as $reader['paper_name'][i]$
                    module_dict['module_'+module]['paper_name'].append(reader['paper_name'][i])
                    module_dict['module_'+module]['fellows'].append(", ".join(result))
                    module_dict['module_' + module]['our_paper_name'].append(list[:list.index(".xlsx")])
    target_folder = './fellow_results/by_module/fellow-list-' + target_year + '-notification/'
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)
    for module_name in module_dict:
        pd.DataFrame(module_dict[module_name]).to_excel(target_folder+module_name+".xlsx")
        print(target_folder+module_name+".xlsx")

def get_fellow_by_list():
    fellows = []
    target_year = '2021'
    for sheetname in sheet_list:
        reader = pd.read_excel("./fellow_list.xlsx", sheet_name=sheetname)
        for i in range(reader.shape[0]):
            name = remove_prefix(reader['name'][i]).replace('\n', '').replace('\xa0', ' ')
            if sheetname == 'acm_2021':
                name = reverse(name)
            fellows.append(name)

    authors_list = os.listdir('./citation_rename_info/author-list-2021/')
    with open("./our_paper_info_first.pkl", "rb") as f:
        our_paper_info = pickle.load(f)

    for list in authors_list:
        result_dict = {'fellows': [], 'paper_name': []}
        print(list)
        if list.startswith("~$"):
            continue
        reader = pd.read_excel('./citation_rename_info/author-list-' + target_year + '/' + list)
        for i in range(reader.shape[0]):
            # result_dict['paper_name'].append(reader['paper_name'][i])
            if reader['authors'][i] == "No information":
                pass
                # result_dict['fellows'].append("")
            else:
                author_list = reader['authors'][i].strip().split(', ')
                result = []

                if not set(author_list).isdisjoint(our_paper_info[list[:list.index(".xlsx")]]["our_authors"]):
                    continue
                for author in author_list:
                    if author in fellows:
                        print("----",author)
                        print(author,author_list,our_paper_info[list[:list.index(".xlsx")]]["our_authors"])
                        result.append(author)

                if len(result) == 0:
                    pass
                    # result_dict['fellows'].append("")
                else:
                    result_dict['paper_name'].append(reader['paper_name'][i])
                    result_dict['fellows'].append(", ".join(result))

        if not os.path.isdir('./fellow-list-' + target_year + '/'):
            os.mkdir('./fellow-list-' + target_year + '/')
        writer = pd.ExcelWriter('./fellow-list-' + target_year + '/' + list[:-5] + '.xlsx')
        pd.DataFrame(result_dict).to_excel(excel_writer=writer)
        writer.save()
        writer.close()

target_year="2021"
get_fellow_by_module(target_year)
