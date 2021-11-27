import json
import os


def caller(path,name):
	last_four=name[-4:]
	if last_four == ".csv":
		data_list=[last_four,"_"]
		return data_list
	else:
		try:
			relative_path = os.path.abspath(path)
			source = open(relative_path, "r")
			data = json.load(source)
			source.close()
			data_list = [data,name,path]
			return data_list
		except FileNotFoundError:
			for i in range(1,2):
				if FileNotFoundError==True:
					continue