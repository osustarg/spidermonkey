import sys
import os
import tempfile
import commands
import re




def execute_testcase(testcase, executable, jsfunrun = "jsfunrun.js"):
    fd, tmpfile_name = tempfile.mkstemp()
    tempF = open(tmpfile_name, 'w')
    jsf = open(jsfunrun)
    tc  = open(testcase)
    concat = jsf.read() + "\n" + tc.read()
    tempF.write(concat)
    jsf.close()
    tc.close()
    tempF.flush()
    tempF.close()
    os.close(fd)
    cmd = '{0} -f {1}'.format(executable, tmpfile_name)
    status, out_lines = commands.getstatusoutput(cmd)
    pattern = re.compile(r"\n+")
    out =  re.sub(pattern, "\n", out_lines)
    os.remove(tmpfile_name)

    # os.system(cmd)

    return (status, out)



def main():
    testcase   = sys.argv[1]
    jsfunrun   = sys.argv[2]
    executable = sys.argv[3]
    (status, out) = execute_testcase(testcase, executable, jsfunrun)
    print('status = ', status)
    print('out = ', out)

if __name__ == '__main__':
    main()
