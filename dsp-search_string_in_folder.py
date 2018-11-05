import re
import glob
txtpattern = ''
# mod = r'fail|Fail'
mod = r'(\d\d:\d\d:\d\d):99\s[ap]m\sweek=(\d)\n.*\1:00\s[ap]m\sweek=\2'
pattern = re.compile(mod)
txtnamelist = glob.glob('*.log')
result_csv = ''
for name in txtnamelist:
    context = open(name).read()
    if pattern.search(context):
        result = '%s, fail=1\n' % (name)
        print(result)
        result_csv = result_csv + result
    else:
        result = '%s\n' % (name)
        print(result)
if result_csv:
	open('result.csv', 'a').write(result_csv)
