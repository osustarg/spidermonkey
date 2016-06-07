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
    FAIL = 0;
    PASS = 1


class DD(object):
    @abstractstaticmethod
    def pre(deltas):
        """ what should be done to deltas"""
        pass

    @abstractstaticmethod
    def post(partition, deltas):
        """what should happens after delta"""


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
        newlist = deltas[:]
        random.shuffle(newlist)
        return newlist

    @staticmethod
    def post(partition, deltas):
        pass



def test(deltas):
    fd, tmp_filename = tempfile.mkstemp()
    tempF = open(tmp_filename, 'w')
    test_text  = '\n'.join(deltas)
    tempF.write(test_text)
    tempF.flush()
    tempF.close()
    os.close(fd)
    status, out = RT.runtestcase(tempF, executable)
    os.remove(temp_filename)
    if status != 0:
        return TESTRESULT.FAIL
    else:
        return TESTRESULT.PASS



def ddmin(deltas, DD):
    n = 2
    firstCondition  = False
    secondCondition = False
    while True:
        ln = len(deltas)
        pre_deltas = DD.pre(deltas)

        if n > ln:
            return deltas
        for temp_delta in pre_deltas:
            if test(temp_delta) == TESTRESULT.FAIL:
                n = 2
                deltas = DD.post(temp_delta)
                firstCondition = True
                break

        if not firstCondition:
            for d in pre_deltas:
                inverse_delta = filter(lambda s: s != d, deltas)
                if test(inverse_delta) == TESTRESULT.FAIL:
                    n = max(n-1, 2)
                    deltas = DD.post(inverse_delta)
                    secondCondition = True
                    break

        if not (firstCondition or secondCondition):
            if n >= ln:
                return delta
            if n < ln:
                n = min(ln, 2*n)




parser = argparse.ArgumentParser(description='Slipage analysis.')
parser.add_argument('--compare_out',
                      help='compares the output of reduced and unreduced test cases')
parser.add_argument('--classic',
                     help='Runs classic delta debugging')

parser.add_argument('--random',
                     help='Runs randomized delta debugging')

parser.add_argument('--testcase', help='path to thet SpiderMonkey test case.')





def main():
    reduced_dir = sys.argv[1]
    unreduced_dir = sys.argv[2]
    executable = sys.argv[3]
    compare_dirs(reduced_dir, unreduced_dir, executable)




def slippage():
    unreduced_dir = sys.argv[2]




if __name__ == '__main__':
    main()
