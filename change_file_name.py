import os

data = r"C:\Users\msi\OneDrive - acsp.ac.th\Desktop\Text Classification\data"
folders = os.listdir(data)
print(folders)

#Change Name
for n, fol in enumerate(folders):
        #print(n, fol)
        folder = fr"C:\Users\msi\OneDrive - acsp.ac.th\Desktop\Text Classification\data\{fol}"
        files = os.listdir(folder)
        for i, file in enumerate(files):
                os.rename(os.path.join(folder, file), os.path.join(folder, ''.join([f'{(i+1):03d}', '.txt'])))
