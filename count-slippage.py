import sys
logfile = open(sys.argv[1])

lines = logfile.readlines()

for l in lines:
    if  '|delta|' in l:
        return_code = l.strip().split()[-1]
        if '1000' in l:
            target_code = return_code
            reported_code = target_code
        else:
            if return_code != target_code and return_code != reported_code:
                reported_code = return_code
                print 'slippage from {0} to {1}'.format(target_code, return_code)
            
