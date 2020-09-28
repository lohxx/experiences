import os


def get_dirs(files: os.DirEntry, all_children_looked: int=0, rec_dir: os.DirEntry=None):
	"""
	Olha diretorios de forma recursiva.

	Args:
		files (List): lista com todos os arquivos que existem no diretorio.
		all_children_looked (int, optional): contagem de diretorios que já foram olhados. Defaults to 0.
		rec_dir (os.DirEntry, optional): diretorio que vai ser olhado recursivamente. Defaults to None.
	"""

	files = list(files)
	dirs = [f for f in files if f.is_dir()]

	if rec_dir:
		dirs = [rec_dir]

	def look_inside_dir(dir):
		if os.listdir(dir.path):
			for i in list(os.scandir(dir.path)):
				if i.is_file():
					print(f'{file.name}/{i.name}')
				else:
					get_dirs(os.scandir(i), rec_dir=i)

	while all_children_looked < len(dirs):
		file = dirs[all_children_looked]
		print(f'{file.name}/')

		all_children_looked += 1
		look_inside_dir(file)


main_root = os.getcwd()
looked_dirs = []
get_dirs(os.scandir(main_root))
