import glob
import pandas as pd

extension = 'csv'
all_filenames = [i for i in glob.glob('./translations/*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f, header=None) for f in all_filenames], axis=0, ignore_index=True)
combined_csv.to_csv("translations.csv", index=False, encoding='utf-8-sig', header=None)

print(f'combined {all_filenames}')