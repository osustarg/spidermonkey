import random
import sys
import os
import runtestcase as RT






def compare_dirs(reduced_dir, unreduced_dir,executable):
    reduced_files   = [f for f in os.listdir(reduced_dir)   if os.path.isfile(os.path.join(reduced_dir, f)) and f.endswith('fmin')]
    unreduced_files = [f for f in os.listdir(unreduced_dir) if os.path.isfile(os.path.join(unreduced_dir, f)) and f.endswith('full')]
    print(len(reduced_files), len(unreduced_files))

    for unred in unreduced_files:
        red = unred.replace('.full', '.fmin')
        if red in reduced_files:
            print (red, unred)
            red_file = os.path.join(reduced_dir, red)
            unred_file = os.path.join(unreduced_dir, unred)
            (unred_status, unred_out) = RT.execute_testcase(unred_file, executable)
            (red_status, red_out) = RT.execute_testcase(red_file, executable)
            print("****************UNREDUCED*******************")
            print(unred_out)
            print("**************** REDUCED *******************")
            print(red_out)
            print("============================================")

            if red_out == unred_out and unred_status == red_status:
                "same output"
        else:
            pass

            # print('not found')


import abc
abstractstaticmethod = abc.abstractmethod


class TESTRESULT:
    FAIL = 0
    PASS = 1


class DD(object):
    @abstractstaticmethod
    def pre(deltas):
        """ what should be done to deltas"""
        pass

    # @abstractstaticmethod
    # def post(partition, deltas):
    #     """what should happens after delta"""

class CLASSICDD(DD):
    @staticmethod
    def pre(deltas):
        return deltas

    @staticmethod
    def post(partition, deltas):
        pass


class RANDOMDD(DD):
    @staticmethod
    def pre(deltas):
        # print 'DELTA:', deltas
        newlist = deltas[:]
        random.shuffle(newlist)
        return newlist

    @staticmethod
    def post(partition, deltas):
        pass

def test(deltas):
    import tempfile
    fd, tmp_filename = tempfile.mkstemp()
    tempF = open(tmp_filename, 'w')
    strippeddeltas = map(lambda s: s.strip(), deltas)
    test_text  = '\n'.join(strippeddeltas)
    tempF.write(test_text)
    tempF.flush()
    tempF.close()
    os.close(fd)
    (status, out) = RT.execute_testcase(tmp_filename, executable)
    print "result status", status
    os.remove(tmp_filename)
    if status != 0:
        return TESTRESULT.FAIL
    else:
        return TESTRESULT.PASS

def split(deltas, n):
    delta_ln = len(deltas)
    if n > delta_ln:
        raise ArithmeticError
    binsize = delta_ln / n
    newdelta = []
    i = 0
    while i < delta_ln:
        bi = 0
        newbin = []
        while bi < binsize and i < delta_ln:
            newbin.append(deltas[i])
            bi += 1
            i += 1
        newdelta.append(newbin[:])
    return newdelta




def ddmin(deltas, DD):
    n = 2
    firstCondition  = False
    secondCondition = False
    while True:
        ln = len(deltas)
        print("delta size: {0}, n: {1}, delte: ".format(ln, n, deltas))
        deltas = DD.pre(deltas)
        if n > ln:
            return deltas
        for temp_delta in split(deltas,n):
            if test(temp_delta) == TESTRESULT.FAIL:
                n = 2
                deltas = temp_delta
                firstCondition = True
                break

        if not firstCondition:
            for d in split(deltas, n):
                inverse_delta = filter(lambda s: s != d, deltas)
                inverse_delta_list = reduce(lambda x,y: x+y, inverse_delta)
                if test(inverse_delta_list) == TESTRESULT.FAIL:
                    n = max(n-1, 2)
                    deltas = inverse_delta_list
                    secondCondition = True
                    break

        if not (firstCondition or secondCondition):
            if n >= ln:
                return deltas
            if n < ln:
                n = min(ln, 2*n)


import argparse







def main1():
    reduced_dir = sys.argv[1]
    unreduced_dir = sys.argv[2]
    executable = sys.argv[3]
    compare_dirs(reduced_dir, unreduced_dir, executable)



def to_testcase(reduced_delta, testcase_basename,  method):
    testcase_text = '\n'.join(reduced_delta)
    filename = testcase_basename + '.' + method
    with open(filename, 'w') as newfile:
        newfile.write(testcase_text)
        newfile.close()



def slippage():
    unreduced_files = [f for f in os.listdir(unreduced_dir) if os.path.isfile(os.path.join(unreduced_dir, f)) and f.endswith('full')]
    unreduced_files =["/tmp/unreduced/tests/tc96123.full"]
    for unred in unreduced_files[:100]:
        unred_file = os.path.join(unreduced_dir, unred)
        print unred_file
        deltas = open(unred_file).readlines()
        for m in ['classic', 'random']:
            if m == 'classic':
                reduced_delta = ddmin(deltas, CLASSICDD)
            if m == 'random':
                reduced_delta = ddmin(deltas, RANDOMDD)
            testcase_basename = unred
            reduced_tc = to_testcase( reduced_delta, testcase_basename, m)






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Slippage analysis.')
    # parser.add_argument('--compare_out',
    #                       help='compares the output of reduced and unreduced test cases')
    # parser.add_argument('--classic',
    #                      help='Runs classic delta debugging')

    # parser.add_argument('--random',
    #                      help='Runs randomized delta debugging')
    #
    # parser.add_argument('--testcase', help='path to thet SpiderMonkey test case.')
    parser.add_argument('--unreduced', help='path to thet SpiderMonkey unreduced test case.')
    parser.add_argument('--exe', help='path to thet SpiderMonkey executable ("js").')
    args  = parser.parse_args()
    unreduced_dir = args.unreduced
    executable = args.exe

    slippage()
