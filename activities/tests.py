import datetime
import json
import uuid

import pandas as pd
# import pinyin
# df = pd.read_excel('data.xlsx')
# print(dict(df.items()))
#
xl_file = pd.ExcelFile('../data.xlsx')

# dfs = {sheet_name: xl_file.parse(sheet_name)
#           for sheet_name in xl_file.sheet_names}
user_list = []
for sheet_name in xl_file.sheet_names:
    # print(str(xl_file.parse(sheet_name)).split())
    res = xl_file.parse(sheet_name).to_dict(orient='records')
    for item in res:
        # print(item)
        # new_dic = {}
        t = [1, 1, 1, 1, 1]
        t[0] = item.get('运动开始时间')
        t[1] = item.get('运动结束时间')
        t[2] = item.get('name')
        t[3] = item.get('location')
        t[4] = int(
            (
                    datetime.datetime.strptime(t[1], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(t[0],
                                                                                                       '%Y-%m-%d %H:%M:%S')
            ).total_seconds()
        )
        # new_dic['name'] = item.get('姓名')
        # new_dic['gender'] = item.get('性别')
        # new_dic['age'] = item.get('年龄')
        # new_dic['username'] = str(uuid.uuid4())[:8]
        # user_list.append(new_dic)
        user_list.append(t)

        # break
print(user_list)
exit()

    # break
# print(user_list)
values = tuple([tuple(item.values()) for item in user_list])
# print(values)
# print(dfs)


sql = """
INSERT iNTO users_user VALUES %s
""" % str(values)
print(sql)