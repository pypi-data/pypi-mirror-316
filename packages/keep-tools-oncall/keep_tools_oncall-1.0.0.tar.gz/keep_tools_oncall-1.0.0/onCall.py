import difflib
import time

import click
import requests


bii_and_btiS = [
    {'business_infos_id': 5, 'business_types_id': 7},
    {'business_infos_id': 17, 'business_types_id': 8},
    {'business_infos_id': 75, 'business_types_id': 31},
    {'business_infos_id': 87, 'business_types_id': 32},
    {'business_infos_id': 137, 'business_types_id': 45},
    {'business_infos_id': 149, 'business_types_id': 46}
]
developer_info = []
role_idS = []


@click.group()
def oc():
    global bii_and_btiS, developer_info, role_idS
    try:
        for bAb in bii_and_btiS:
            response = requests.get(
                f"https://keep.corp.kuaishou.com/api/app_release/weekly_rule/get_rule?business_infos_id={bAb.get('business_infos_id')}&business_types_id={bAb.get('business_types_id')}")
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            # 存储研发角色信息的数据结构
            for role in data.get("data", []):
                if role.get("role_name") == "研发":
                    role_idS.append(role.get("role_id"))
                    infos = role.get("infos", [])
                    for i, info in enumerate(infos):
                        # 提取所需信息
                        if len(infos) == len(developer_info):
                            if 'idS' not in developer_info[i]:
                                developer_info[i]['idS'] = []
                            if 'polling_indexS' not in developer_info[i]:
                                developer_info[i]['polling_indexS'] = []
                            developer_info[i]['idS'].append(info.get('id'))
                            developer_info[i]['polling_indexS'].append(info.get('polling_index'))
                        else:
                            entry = {
                                'idS': [info.get('id')],
                                'rank': info.get('rank'),
                                'polling_indexS': [info.get('polling_index')],
                                'status': info.get('status'),
                                "weekly_persons": [person.get('username') for person in info.get("week_person")]
                            }
                            developer_info.append(entry)
    except requests.RequestException as e:
        print(f"请求失败: {e}")
    except ValueError as e:
        print(f"JSON 解析失败: {e}")


@click.command()
def get():
    print("值周组合信息：")
    print(developer_info)
    with open('value_week_info.txt', 'w') as f1 ,open('new_week_info.txt','w') as f2:
        for i, weekly_person in enumerate(developer_info):
            print(f"组序号: {i}")
            usernames = []
            for person in weekly_person.get('weekly_persons', []):
                print(f"  - 姓名: {person}")
                usernames.append(person)
            f1.write(f"{' '.join(usernames)}\n")
            f2.write(f"{' '.join(usernames)}\n")

def read_usernames_from_file(filename):
    username_groups = []
    with open(filename, 'r') as f:
        for line in f:
            username_groups.append(line.strip().split())
    return username_groups


import difflib

def diff_usernames(old_entries, new_entries):
    added = []
    removed = []
    modified = []
    unchanged = []
    old_usernames = [tuple(entry['weekly_persons']) for entry in old_entries]  # 将列表转换为元组
    new_entries = [tuple(entry) for entry in new_entries]  # 将列表转换为元组
    matcher = difflib.SequenceMatcher(None, old_usernames, new_entries)
    for opcode in matcher.get_opcodes():
        tag, i1, i2, j1, j2 = opcode
        if tag == 'equal':
            unchanged.extend(old_entries[i1:i2])
        elif tag == 'delete':
            for entry in old_entries[i1:i2]:
                removed.append(entry['idS'])  # 仅存储 idS
        elif tag == 'insert':
            for entry in new_entries[j1:j2]:
                added.append(list(entry))  # 存储新的用户名列表，转换回列表
        elif tag == 'replace':
            old_usernames = [old_entries[i]['weekly_persons'] for i in range(i1, i2)]
            new_usernames = [list(entry) for entry in new_entries[j1:j2]]  # 转换回列表
            if len(old_usernames) > len(new_usernames):
                # 删除多出的行
                for old_username_list in old_usernames[len(new_usernames):]:
                    # 找到 old_username_list 所在的 entry，并添加其 idS 到 removed 列表
                    for entry in old_entries:
                        if 'weekly_persons' in entry and old_username_list == entry['weekly_persons']:
                            removed.append(entry['idS'])
            elif len(old_usernames) < len(new_usernames):
                # 添加新的行
                for new_username_list in new_usernames[len(old_usernames):]:
                    added.append(new_username_list)
            for old_username_list, new_username_list in zip(old_usernames, new_usernames):
                modified.append({'old_usernames': old_username_list, 'new_usernames': new_username_list})
    return added, removed, modified, unchanged


def call_add_api(business_infos_id, rank, role_id,polling_index, status, usernames):
    url = "https://keep.corp.kuaishou.com/api/app_release/weekly_rule/add_rule"
    payload = {
        "business_infos_id": business_infos_id,
        "role_id": role_id,  # 假设 role_id 固定为 1
        "weekly_persons": {
            "week_person": usernames,
            "rank": rank,
            "polling_index": polling_index,
            "status": status
        }
    }
    headers = {
        "Cookie": "apdid=051aea13-4233-4e82-af40-a20e9e89ec86b24c9142b970914e1178b50ceca7346c:1732863310:1; weblogger_did=web_5484626072DEB3ED; hdige2wqwoino=hMNijQRZsA2CMmjxiQ4MWZCSEiamHRNFf6594385; _did=web_3919066100BD65B0; userName=chengtianran; ksCorpDeviceid=4643e02f-413d-4ef9-ab5b-598e5b5b4239; did=web_c64b74e8fb3e4025b499c5b27ce8e01f; didv=1733386601000; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1733455527; _ga=GA1.1.315375803.1733724088; _ga_H896PJ54TF=GS1.1.1733724088.1.1.1733724110.0.0.0; KEEP_CAS_USERNAME=chengtianran; SESSION=MGY3NzhlMjQtZGU0Ni00OWMwLTg2MzItZTk1Y2FlOTBlZDhm; ehid=35fIYtkZ_d_1mHJ-SfB8BzBnsEg2T9j8xj0yG; accessproxy_session=b7e95608-e5f7-4298-a7fe-34cbe5e98054; session=.eJyNjk2LwjAQhv9KGejNGm12KXjrrhXEj8PWvQVCbEYTGpPQJi4i_veNHva8lxneeYZn5g6fdcu_2-ZrX-8aWECn0J6DFnYQFiZ_lC-bQ73epoU7g-ilCCi5CAwW2byib7Pqvaxmk4yBRB-4F0E9EYNNu_4gz1IcsFPWGXe-kZ07aoPZykWbRNpZBo90a8BT8qsQ_JjTmpAe0U87N_hpH4UelYspXUhe0hcqfDyaNCZXYSIWP4h9Tldey5wuy6QbcbjqDv-jFF6T1C_OkvSgtkQJKw3yV4DHL9FMYXM.Z2GD6w.8arG2lXfzgbaIdyqdPgOncLhR5w"
    }
    try:
        response = requests.post(url, json=payload,headers=headers)
        response.raise_for_status()
        print(f"添加成功")
        print(response.text)
    except requests.RequestException as e:
        print(f"添加失败: {e}")


def call_delete_api(entry_id):
    url = f"https://keep.corp.kuaishou.com/api/app_release/weekly_rule/delete_rule?id={entry_id}"
    headers = {
        "Cookie": "apdid=051aea13-4233-4e82-af40-a20e9e89ec86b24c9142b970914e1178b50ceca7346c:1732863310:1; weblogger_did=web_5484626072DEB3ED; hdige2wqwoino=hMNijQRZsA2CMmjxiQ4MWZCSEiamHRNFf6594385; _did=web_3919066100BD65B0; userName=chengtianran; ksCorpDeviceid=4643e02f-413d-4ef9-ab5b-598e5b5b4239; did=web_c64b74e8fb3e4025b499c5b27ce8e01f; didv=1733386601000; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1733455527; _ga=GA1.1.315375803.1733724088; _ga_H896PJ54TF=GS1.1.1733724088.1.1.1733724110.0.0.0; KEEP_CAS_USERNAME=chengtianran; SESSION=MGY3NzhlMjQtZGU0Ni00OWMwLTg2MzItZTk1Y2FlOTBlZDhm; ehid=35fIYtkZ_d_1mHJ-SfB8BzBnsEg2T9j8xj0yG; accessproxy_session=b7e95608-e5f7-4298-a7fe-34cbe5e98054; session=.eJyNjk2LwjAQhv9KGejNGm12KXjrrhXEj8PWvQVCbEYTGpPQJi4i_veNHva8lxneeYZn5g6fdcu_2-ZrX-8aWECn0J6DFnYQFiZ_lC-bQ73epoU7g-ilCCi5CAwW2byib7Pqvaxmk4yBRB-4F0E9EYNNu_4gz1IcsFPWGXe-kZ07aoPZykWbRNpZBo90a8BT8qsQ_JjTmpAe0U87N_hpH4UelYspXUhe0hcqfDyaNCZXYSIWP4h9Tldey5wuy6QbcbjqDv-jFF6T1C_OkvSgtkQJKw3yV4DHL9FMYXM.Z2GD6w.8arG2lXfzgbaIdyqdPgOncLhR5w"
    }
    try:
        response = requests.get(url,headers=headers)
        response.raise_for_status()
        print(f"删除成功: {entry_id}")
    except requests.RequestException as e:
        print(f"删除失败: {e}")


def call_update_api(business_infos_id,role_id, entry_id, status, new_usernames):
    url = "https://keep.corp.kuaishou.com/api/app_release/weekly_rule/update_rule"
    payload = {
        "business_infos_id": business_infos_id,
        "role_id": role_id,
        "weekly_persons": [
            {
                "id": entry_id,
                "week_person": new_usernames,
                "status": status
            }
        ]
    }
    headers = {
        "Cookie": "apdid=051aea13-4233-4e82-af40-a20e9e89ec86b24c9142b970914e1178b50ceca7346c:1732863310:1; weblogger_did=web_5484626072DEB3ED; hdige2wqwoino=hMNijQRZsA2CMmjxiQ4MWZCSEiamHRNFf6594385; _did=web_3919066100BD65B0; userName=chengtianran; ksCorpDeviceid=4643e02f-413d-4ef9-ab5b-598e5b5b4239; did=web_c64b74e8fb3e4025b499c5b27ce8e01f; didv=1733386601000; Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1733455527; _ga=GA1.1.315375803.1733724088; _ga_H896PJ54TF=GS1.1.1733724088.1.1.1733724110.0.0.0; KEEP_CAS_USERNAME=chengtianran; SESSION=MGY3NzhlMjQtZGU0Ni00OWMwLTg2MzItZTk1Y2FlOTBlZDhm; ehid=35fIYtkZ_d_1mHJ-SfB8BzBnsEg2T9j8xj0yG; accessproxy_session=b7e95608-e5f7-4298-a7fe-34cbe5e98054; session=.eJyNjk2LwjAQhv9KGejNGm12KXjrrhXEj8PWvQVCbEYTGpPQJi4i_veNHva8lxneeYZn5g6fdcu_2-ZrX-8aWECn0J6DFnYQFiZ_lC-bQ73epoU7g-ilCCi5CAwW2byib7Pqvaxmk4yBRB-4F0E9EYNNu_4gz1IcsFPWGXe-kZ07aoPZykWbRNpZBo90a8BT8qsQ_JjTmpAe0U87N_hpH4UelYspXUhe0hcqfDyaNCZXYSIWP4h9Tldey5wuy6QbcbjqDv-jFF6T1C_OkvSgtkQJKw3yV4DHL9FMYXM.Z2GD6w.8arG2lXfzgbaIdyqdPgOncLhR5w"
    }
    print(payload)
    try:
        response = requests.post(url, json=payload,headers=headers)
        response.raise_for_status()
        print(f"更新成功: {entry_id}")
    except requests.RequestException as e:
        print(f"更新失败: {e}")


@click.command()
def update():
    global bii_and_btiS, developer_info, role_idS  # 声明全局变量
    try:
        new_entries = read_usernames_from_file('new_week_info.txt')
        added, removed, modified, unchanged = diff_usernames(developer_info, new_entries)
        for i, bAb in enumerate(bii_and_btiS):
            role_id = role_idS[i]
            business_infos_id = bAb.get('business_infos_id')
            rankCount=developer_info[-1]['rank']+1
            for entry in added:
                call_add_api(business_infos_id, rankCount, role_id,0, 1, entry)
                rankCount+=1
            for entry_idS in removed:
                    call_delete_api(entry_idS[i])
            for entry in modified:
                old_usernames = entry['old_usernames']
                new_usernames = entry['new_usernames']
                for dev_entry in developer_info:
                    if set(old_usernames) == set(dev_entry['weekly_persons']):
                        status = dev_entry['status']
                        call_update_api(business_infos_id, role_id,dev_entry['idS'][i], status, new_usernames)
                        time.sleep(1)
                        break
    except requests.RequestException as e:
        print(f"更新失败: {e}")


oc.add_command(get)
oc.add_command(update)

