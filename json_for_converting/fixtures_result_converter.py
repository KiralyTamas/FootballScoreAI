import csv
import file_caller

def convert_header(data_list, delim):
    with open(data_list[0], "w", newline='') as file:
        csv_file = csv.writer(file)
        for number in data_list[1]:
            header = []
            for i in number.keys():
                if isinstance(number[i], dict):
                    for j in number[i].keys():
                        header.append(str(i)+delim+str(j))
                header.append(i)
                if isinstance(number[i], dict):
                    header.remove(i)
        csv_file.writerow(header)
        for number in data_list[1]:
          content = []
          for i in number.keys():
            content.append(number[i])
            if isinstance(number[i], dict):
                content.remove(number[i])
                for j in number[i]:
                    content.append(str(number[i][j]))
          csv_file.writerow(content)

convert_header(file_caller.caller(), "_")
