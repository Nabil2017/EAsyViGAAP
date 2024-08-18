
import os

for file_num in range(1, 1000):
    file_name = 'file{}.fasta'.format(file_num)

    try:
        with open(file_name, 'r') as file:
            content = file.read()
            symbol_index = content.find('+')
            if symbol_index != -1:
                content = content[:symbol_index]


        file_base_name = os.path.splitext(file_name)[0]


        content = content.replace("@reference", ">{}".format(file_base_name))


        print(content)


        new_file_name = 'file{}_assembly.fasta'.format(file_num)
        with open(new_file_name, 'w') as new_file:
            new_file.write(content)

    except Exception as e:

        break

print("Processing complete.")
