import pandas as pd
import json


# 从JSON文件中读取数据
with open('page.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

search_results = data['searchResults']

# 将"searchResults"键的值转换为一个DataFrame
df = pd.DataFrame(search_results)

# 找出包含字典的列
dict_cols = [col for col in df.columns if df[col].apply(type).eq(dict).any()]

# 展平这些列
for col in dict_cols:
    col_df = pd.json_normalize(df[col])
    col_df.columns = [f"{col}_{subcol}" for subcol in col_df.columns]
    df = df.drop(col, axis=1).join(col_df)

# 打印展平后的DataFrame
print(df)
df.to_csv('flattened_search_results.csv', index=False)
