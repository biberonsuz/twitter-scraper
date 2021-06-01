import os
from textblob import TextBlob

for d in os.listdir('teargas'):
	if os.path.isdir(os.path.join('teargas', d)):
		lang_contents = os.listdir(f'teargas/{d}')
		for file in lang_contents:
			if file.endswith(".txt"):
				file_path = os.path.join(f'teargas/{d}', file)

				lines_seen = set()  # holds lines already seen
				infile = open(file_path, "w+")
				for line in infile:
				    if line in lines_seen:  #duplicate
				        infile.replace(line, '')
				infile.close()
				print(f'{file_path} complete')
# tr.set_from_lang('ar')
# tr.set_to_lang('en')
# tr.translate()

# tr.set_text('text_to_translate')