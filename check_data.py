import os

data = os.path.dirname(os.path.realpath(__file__)) + '\data'
folders = os.listdir(data)
print(folders)

sum_all = 0

for n, fol in enumerate(folders):
        folder = data + fr"\{fol}"
        files = os.listdir(folder)
        count = 0
        for i, file in enumerate(files):
            count+=1
        sum_all += count
        print(f"{fol}: {count}")

print(f"All Data: {sum_all}")

