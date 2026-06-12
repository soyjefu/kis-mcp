import pandas as pd
df = pd.read_csv('/home/soyjefu/theprepared/kis-mcp/MCP/KIS Code Assistant MCP/data.csv')
for index, row in df.iterrows():
    if pd.notna(row['description']) and 'S&P500' in row['description']:
        print(row['api_name'], row['description'])
    if pd.notna(row['args']) and 'S&P500' in row['args']:
        print(row['api_name'], row['args'])
