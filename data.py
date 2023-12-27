import pandas as pd

file_path = 'algorithms.csv'

pd.set_option('display.max_rows', None)


df = pd.read_csv(file_path)

min_index = df['avg_guesses'].idxmin()
min_row = df.loc[min_index]
print("\nAlgorithm with lowest average guesses:")
print(min_row)

print(df)
