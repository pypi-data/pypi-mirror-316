
import pandas as pd
# 创建一个DataFrame
def text_json_list(data:str):
    try:
        data = data
        df = pd.DataFrame(data)
        df.to_csv('output.csv', index=False)
        return df
    except:
        print('数据错误!')


