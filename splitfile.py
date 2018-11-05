text = '#3_dma0_robust_3rd_2.log'
infile = open(text, 'r')
i = 0
lines = infile.readlines(100000000)
while(lines):
    open('outlog%d.log' % (i), 'w').writelines(lines)
    i = i + 1
    lines = infile.readlines(100000000)
