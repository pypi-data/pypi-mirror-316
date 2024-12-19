import json
import sys

import pandas as pd
from numpy import int64


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, int64):
            return str(obj)
        return super().default(obj)


def get_dies_data(file_name) -> pd.DataFrame:
    """
    Get the data from the file, return a dataframe
    :param file_name:
    :return: dataframe
    """
    if not file_name or not file_name.endswith(".csv"):
        return None
    return pd.read_csv(file_name)


def get_testitems_data(file_name) -> pd.DataFrame:
    """
    Get the test items data
    :return: dataframe
    """
    if not file_name or not file_name.endswith(".csv"):
        return None
    return pd.read_csv(file_name)


def get_summary_data(file_name) -> pd.DataFrame:
    """
    Get the mes data
    :return: dataframe
    """
    if not file_name or not file_name.endswith(".csv"):
        return None
    return pd.read_csv(file_name)


def json_result(res, code=200, message='Success'):
    return {'data': res, 'code': code, 'message': message}


def parse_args(args) -> dict:
    args_dict = {arg.strip().split("=")[0][2:].strip(): arg.strip().split("=")[1].strip() for arg in args if
                 arg.strip().startswith("--")}
    return args_dict


def monitor_start():
    """
    Main function
    :return:
    """
    # python test.py params="{'xx':12, 'yy':['a','b','c']}" ext_params='{}'  die_file="./die.csv" test_item_file='./test_item.csv'
    args = sys.argv
    args_dict = parse_args(args)
    die_file = args_dict.get("die_file")
    test_item_file = args_dict.get("test_item_file")
    summary_file = args_dict.get("summary_file")
    params = args_dict.get("params")
    params = json.loads(params) if params else None
    ext_params = args_dict.get("ext_params")
    ext_params = json.loads(ext_params) if ext_params else None
    die_df = get_dies_data(die_file)
    test_item_df = get_testitems_data(test_item_file)
    summary_df = get_summary_data(summary_file)
    res = customize_rule(params=params, ext_params=ext_params, die_df=die_df, test_item_df=test_item_df,
                         summary_df=summary_df)
    return json.dumps(json_result(res))


# Monitor自定义规则核心逻辑， 参数包括：params（固定参数）, ext_params（扩展Json形式参数）, die_file（Die文件表csv）, test_item_file（TestItem文件表csv）
def customize_rule(params, ext_params, die_df, test_item_df, summary_df):
    """
    Customize the SBL
    :param die_df:
    返回值是一个字典，通过json_result函数封装，包含data，code，message；其中data必须包含三个字段：triggerFlag, remark, detail
    :return: {
            "data":
                {
                     triggerFlag:True or False,
                     detail:[{},{}],
                     remark:""
                },
            "code":200,
            "message":"Success"
            }
    """
    res = {}
    # 对die_df根据dieX,dieY进行分组，然后按照start_time进行排序，取最后一行，并生成新的dataframe
    die_df_grouped = die_df[['ecid', 'hbinPf', 'startTime']].groupby(['ecid']).apply(
        lambda x: x.sort_values('startTime', ascending=False).head(1)).reset_index(drop=True)
    die_total_cnt = len(die_df_grouped)
    die_pass_cnt = len(die_df_grouped[die_df_grouped['hbinPf'] == 'P'])
    # 获取summary_df第一行的'totalCnt', 'passCnt'值
    summary_total_cnt = int(summary_df.iloc[0]['totalCnt'])
    summary_pass_cnt = int(summary_df.iloc[0]['passCnt'])
    remark = []
    detail = [{"MESCount": summary_total_cnt, "InputCount": die_total_cnt},
              {"MESPassCount": summary_pass_cnt, "InputPassCount": die_pass_cnt}]
    if die_total_cnt == summary_total_cnt and die_pass_cnt == summary_pass_cnt:
        triggerFlag = True
        remark.append('Match')
    else:
        if die_total_cnt > summary_total_cnt:
            triggerFlag = False
            remark.append('inputMore')
        if die_total_cnt < summary_total_cnt:
            triggerFlag = False
            remark.append('inputLess')
        if die_pass_cnt < summary_pass_cnt:
            triggerFlag = False
            remark.append('outputMore')
        if die_pass_cnt > summary_pass_cnt:
            triggerFlag = False
            remark.append('outputLess')

    # 封装为json格式返回，必须包含这三个字段：triggerFlag, remark, detail
    res['triggerFlag'] = triggerFlag
    res['remark'] = ",".join(remark)
    res['detail'] = detail
    return res


if __name__ == "__main__":
    try:
        res = monitor_start()
    except Exception as e:
        res = json.dumps({"data": {}, "code": 500, "message": f"Error: {e}"})
    print(res)
