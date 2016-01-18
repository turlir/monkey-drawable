# -*- coding: UTF-8 -*-
# папка назначения есть аргумент to - то, куда будут разложены файлы
# хранилище есть аргумент fromd - то, откуда будет скопированы файлы

from helper import *
import shutil

def parseArg ():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fromd", default = os.getcwd())
    parser.add_argument("-t", "--to", required = True)
    parser.add_argument("-r", "--rule", required = False)
    parser.add_argument("-s", "--source", required = True)
    parser.add_argument("-d", "--dest", required = False)
    parser.add_argument("--debug", default = False, required = False, action='store_true')
    args = parser.parse_args()

    return args

def one(from_list, to_list, dest):
    r = oneRule(from_list, to_list, dest)

    return r.work()

def dpi(from_list, to_list, dest):
    r = dpiRule(from_list, to_list, dest)

    return r.work()

def size(from_list, to_list, dest):
    pass

def copy(func, from_list, to_list, dest):
    # fromList - toList
    # что копировать - куда копировать
    comprasion = func(from_list, to_list, dest)

    print("-------------------- \n")

    keys = list(comprasion.keys())
    values = list(comprasion.values())

    raw_copy(keys, values)

def raw_copy(keys, values):
    q = 0
    yes_all = True

    while(q < len(keys)):
        fromd = keys[q]
        to = values[q]

        tod = to + "." + fromd.resolution
        if(os.path.exists(tod) & yes_all):
            print(tod)
            i = input("Replace? 1 - yes, 2 - no, 3 - yes all ")
            if(i == str("1")):
                shutil.copy(fromd.path, tod)
            elif(i == str("3")):
                yes_all = False
                shutil.copy(fromd.path, tod)
            elif(i == str("2")):
                pass
            else:
                print("error input")
                q-=1
        else:
            shutil.copy(fromd.path, tod)
            print("copied")

        q+=1

if __name__ == "__main__":
    args = parseArg()

    fromd = args.fromd
    to = args.to
    source = args.source
    debug = args.debug
    dest = args.dest
    rule = args.rule

    if(debug):
        print('fromd = ', fromd)
        print('to = ', to)
        print('source = ', source)
        print('dest = ', dest)
        print("rule = ", rule)

    rules = {
        "one" : one,
        "dpi" : dpi,
        "size" : size
    }

    if(rule == None): rule = "one"
    if(rule not in rules):
        print("invalid rule")
        sys.exit()

    print("--------------------")

    fa = fromAnalyzer(debug)
    from_list = fa.analyzeFrom(fromd, source)

    print("source\n")
    for i in range(0, len(from_list)):
        item = from_list[i]
        c = item.area / from_list[0].area
        print("{0:25s}{1:10d}x{2:1d} {3:10f}".format(item.name, item.width, item.height, c))

    print("--------------------")

    print("target\n")
    ta = toAnalyzer(debug)
    to_list = ta.analyzeTo(to, dest)
    for i in to_list:
        print(i)

    print("--------------------")

    comprasion_func = rules[rule]

    copy(comprasion_func, from_list, to_list, dest)