# -*- coding: UTF-8 -*-

from helper import *
import shutil

def parseArg ():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fromd", default = os.getcwd(), help = "Задает директорию, в которой следует искать файлы изображений.")
    parser.add_argument("-t", "--to", required = True, help = "Задает директорию, в которой следует искать drawable-папки (res).")
    parser.add_argument("-r", "--rule", required = False, help = "Задает стратегию сопоставления имя_изображения-целевая папка.")
    parser.add_argument("-s", "--source", required = True, help = "Задает регулярное выражение (имена исходных файлов).")
    parser.add_argument("-d", "--dest", required = False, help = "Задает имя конечного файла.")
    parser.add_argument("--debug", default = False, required = False, action='store_true', help = "Переход в отладочный режим, файлы скопированы не будут.")
    args = parser.parse_args()

    return args

def one(from_list, to_list, dest):
    r = oneRule(from_list, to_list, dest)

    return r.work()

def dpi(from_list, to_list, dest):
    r = dpiRule(from_list, to_list, dest)

    return r.work()

def size(from_list, to_list, dest):
	r = sizeRule(from_list, to_list, dest)

	return r.work()

def copy(func, from_list, to_list, dest, debug):
    # fromList - toList
    # что копировать - куда копировать
    comprasion = func(from_list, to_list, dest)

    print("-------------------- \n")

    keys = list(comprasion.keys())
    values = list(comprasion.values())

    if(not debug): raw_copy(keys, values)

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

    copy(comprasion_func, from_list, to_list, dest, debug)
