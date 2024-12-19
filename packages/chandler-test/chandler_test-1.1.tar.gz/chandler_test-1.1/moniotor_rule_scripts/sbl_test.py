import json
import sys

import pandas as pd


def get_dies_data(file_name) -> pd.DataFrame:
    """
    Get the data from the file, return a dataframe
    :param file_name:
    :return: dataframe
    """
    return pd.read_csv(file_name)


def get_testitems_data() -> pd.DataFrame:
    """
    Get the test items data
    :return: dataframe
    """
    return pd.read_csv("./data/test_items.csv")


def json_result(res, code=200, message='Success'):
    return {'data': res, 'code': code, 'message': message}


def monitor_start():
    """
    Main function
    :return:
    """
    # python test.py params="{'xx':12, 'yy':['a','b','c']}" ext_params='{}'  die_file="./die.csv" test_item_file='./test_item.csv'
    args = sys.argv
    # 根据参数的key获取对应的value
    args_dict = {arg.strip().split("=")[0][2:].strip(): arg.strip().split("=")[1].strip() for arg in args if
                 arg.strip().startswith("--")}
    die_file = args_dict.get("die_file")
    params = args_dict.get("params")
    params = json.loads(params)
    die_df = get_dies_data(die_file)
    res = customize_sbl(params, die_df)
    return res


# Monitor自定义规则核心逻辑， 参数包括：params（固定参数）, ext_params（扩展Json形式参数）, die_file（Die文件表csv）, test_item_file（TestItem文件表csv）
def customize_sbl(params, die_df):
    """
    Customize the SBL
    :param die_df:
    :return: {
                 triggerFlag:True or False,
                 detail:[{},{}],
                 remark:""
            }
    """
    copy_params = params.copy()
    res = {}
    # 对die_df先按照hbinPf列进行过滤，然后按照hbinNum列进行分组，统计每个组的数据量，并计算每个组的占比
    group_counts = die_df.query("hbinPf=='F'").groupby('hbinNum').size()
    group_proportions = group_counts / group_counts.sum()
    triggerFlag = False
    sbl_remark = ''
    sbl_detail = []
    # 根据每个组的占比和params中设置的阈值，判断是否超过阈值，如果超过，返回False，否则返回True
    for group, proportion in group_proportions.items():
        group = str(group)
        if group not in params:
            continue

        del copy_params[group]

        if params.get(group) is not None:
            if proportion > params.get(group):
                triggerFlag = True
                sbl_detail.append({'Group': group, 'Proportion': proportion, 'Threshold': params.get(group),
                                   'Execution Remark': 'FAIL',
                                   'Detail Description': f"{group} is triggered. Actual value {proportion}, threshold {params.get(group)}."})
                sbl_remark = sbl_remark + (f"{group}" if sbl_remark == '' else f" ,{group}")
            else:
                sbl_detail.append({'Group': group, 'Proportion': proportion, 'Threshold': params.get(group),
                                   'Execution Remark': 'PASS', 'Detail Description': ""})
        else:
            sbl_detail.append(
                {'Group': group, 'Proportion': proportion, 'Threshold': params.get(group), 'Execution Remark': 'PASS',
                 'Detail Description': f"{group} is not found."})

    for group in copy_params:
        sbl_detail.append(
            {'Group': group, 'Proportion': proportion, 'Threshold': params.get(group), 'Execution Remark': 'PASS',
             'Detail Description': f"{group} is not found."})

    # 封装为json格式返回
    res['triggerFlag'] = triggerFlag
    res['remark'] = '' if sbl_remark == '' else 'Trigger Bin: ' + sbl_remark
    res['detail'] = sbl_detail

    return json.dumps(json_result(res))


if __name__ == "__main__":
    print(monitor_start())
