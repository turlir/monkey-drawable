import sys
import argparse
import os
import fnmatch
import glob
import re
from PIL import Image # pillow.readthedocs.org/en/3.0.x/installation.html

class fromItem:
    def __init__(self, path, w, h):
        self.path = path
        self.name = os.path.basename(path)
        self.width = w
        self.height = h
        self.area = w * h

        temp = self.name.split(".")
        self.resolution = temp[len(temp) - 1]

    def __str__(self):
        return '{0:25s} {1:2d}x{1:1d}'.format(self.name, self.width, self.height)

    def __gt__(self, other): # >
        return ((self.area) > (other.area))

    def __truediv__(self, other):
        return ((self.area) / (other.area))

class fromAnalyzer:

    def __init__ (self, debug):
        self.debug = debug

    def findStorage (self, fromd, regex):
        # проверим что есть в хранилище
        p = fromd + '/' + regex
        if(self.debug): print("full searching ", p)

        temp = glob.glob(p)

        if(self.debug):
            print("find")
            for str in temp: print(str)

        return temp

    def filterStorage (self, lst):
        # фильтр
        filtred = []
        for item in lst:
            if(os.path.isfile(item)):
                filtred.append(item)
        if(self.debug):
            print("filtred")
            for str in filtred: print(str)

        return filtred

    def sortFilesByName (self, lst):
        temp = sorted(lst, key=len)
        if(self.debug):
            print("sorted")
            for str in temp: print(str)

        return temp


    def analyzeFrom (self, fromd, regex):
        self.fromd = fromd
        self.regex = regex

        if(not os.path.isdir(fromd)):
            print(fromd, "not a directory")
            sys.exit()

        list_target_file = self.findStorage(fromd, regex)

        if(len(list_target_file) == 0):
            print("file not found")
            sys.exit()

        filtred_target_file = self.filterStorage(list_target_file)
        sorted_target_file = self.sortFilesByName(filtred_target_file)

        from_item = []
        for str in sorted_target_file:
            im = Image.open(str)
            t = fromItem(str, im.size[0], im.size[1])

            from_item.append(t)

        is_size_invalid = False
        for i in range(0, len(from_item)-1):
            b = from_item[i] > from_item[i+1]
            is_size_invalid = (is_size_invalid + b)
        if(is_size_invalid):
            print("source size is invalid")

        return from_item

class toAnalyzer:

    def __init__ (self, debug):
        self.debug = debug

    def findDir (self, to):
        # найдем целевые папки
        p = to + "/drawable*"
        if(self.debug): print("full searching ", p)

        temp = glob.glob(p)

        if(self.debug):
            print("find")
            for str in temp: print(str)

        return temp

    def filter (self, lst):
        # фильтр
        filtred = []
        prog = re.compile(".*drawable-[^ldpi]*dpi")
        for item in lst:
            if(os.path.isdir(item) and prog.match(item)):
                filtred.append(item)
        if(self.debug):
            print("filtred to")
            for str in filtred: print(str)

        return filtred

    def getCoeff (self, str):
        q = ["", "ldpi", "mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"]
        splited = str.split('-')
        if(len(splited) == 2): #drawable-?dpi
            return q.index(splited[1])
        elif (len(splited) == 1): # simple drawable
            return 0
        else: # error
            return -1

    def sorted (self, lst):
        mapped = map(lambda x: str(os.path.normpath(x)), lst)
        nl = sorted(mapped, key = lambda x: self.getCoeff(x))

        return nl

    def analyzeTo(self, to, dest):
        self.to = to
        self.dest = dest

        if(not os.path.isdir(to)):
            print(to, "not a directory")
            sys.exit()

        finded = self.findDir(to)
        filtered = self.filter(finded)
        sorted = self.sorted(filtered)

        return sorted

class oneRule:

    def __init__(self, from_list, to_list, dest):
        self.fromList = from_list
        self.toList = to_list
        self.dest = dest

    def work(self):
        print("one-by-one rule worked \n")
        if(len(self.fromList) != len(self.toList)):
            print("invalid count one rule")
            sys.exit()

        g = list(map(lambda x: str(x + "/" + self.dest), self.toList))

        for i in range(0, len(self.fromList)):
            s = '{0} - {1}'.format(self.fromList[i].name, g[i])
            print(s)

        return dict(zip(self.fromList, g))

class dpiRule:
    def __init__(self, from_list, to_list, dest):
        self.fromList = from_list
        self.toList = to_list
        self.dest = dest

    def work(self):
        print("dpi rule worked \n")

        first_basename = os.path.basename(self.toList[0])
        if(first_basename == "drawable"):
            self.toList.remove(self.toList[0])
        else:
            print("dir drawable is not find")

        if(len(self.fromList) != len(self.toList)):
            print("invalid count dpi rule")
            sys.exit()

        g = list(map(lambda x: str(x + "/" + self.dest), self.toList))

        for i in range(0, len(g)):
            s = '{0} - {1}'.format(self.fromList[i].name, g[i])
            print(s)

        return dict(zip(self.fromList, g))

class sizeRule:
    def __init__(self, from_list, to_list, dest):
        self.fromList = from_list
        self.toList = to_list
        self.dest = dest

    def work(self):
        print("size rule worked \n")

        first_basename = os.path.basename(self.toList[0])
        if(first_basename == "drawable"):
            self.toList.remove(self.toList[0])
        else:
            print("dir drawable is not find")

        self.fromList = sorted(self.fromList, key = lambda x: x.area)

        if(len(self.fromList) != len(self.toList)):
            print("invalid count size rule")
            sys.exit()

        g = list(map(lambda x: str(x + "/" + self.dest), self.toList))

        for i in range(0, len(g)):
            s = '{0} - {1}'.format(self.fromList[i].name, g[i])
            print(s)

        return dict(zip(self.fromList, g))
