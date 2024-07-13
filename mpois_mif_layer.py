# -*- coding: utf-8 -*-
import re
from sys import stdin

from mpois_point import Point 
from mpois_polyline import Polyline
from mpois_multipline import MultiPline
from mpois_region import Region 

class MifLayer():
    def __init__(self):
        self.objects = []
        self.columnNames = []
        self.header = []
    def __len__(self):
        """ Возвращает количество объектов в слое
        """
        return len(self.objects)
    def __getitem__(self,i):
        """ Возвращает i-ый объект слоя
        """
        return self.objects[i]

    def addObject(self, newObj):
        self.objects.append(newObj)

    def __syntaxColumns(self,F, line):
        """ Синтаксический разбор описания таблицы
        """
        regexp = re.compile(r'^\s*Columns\s+(\d+)\s*$',  re.IGNORECASE)
        regmatch = regexp.match(line)
        if not regmatch: raise ValueError
        regexp = re.compile(r'^\s*(\S+)\s+(\S+)\s*$',  re.IGNORECASE)
        for i in range(int(regmatch.group(1))):
            nextColumn = F.readline();
            regmatch = regexp.match(nextColumn);
            if not regmatch: raise ValueError
            self.columnNames.append((regmatch.group(1),regmatch.group(2)))
       
    def __syntaxCordPair(self,F):
        """ Синтаксический разбор координат (пара x,y)
            F - объект типа "файл", откуда читаем MIF
        """
        nextLine = F.readline();
        regexp = re.compile(r'^\s*(-*\d+\.*\d*).*\s+(-*\d+\.*\d*)\s*$')
        regmatch = regexp.match(nextLine)
        if regmatch:
            x = float(regmatch.group(1))
            y = float(regmatch.group(2))
            return Point(x, y)
        else:
            raise ValueError

    def __syntaxPoint(self, F, line):
        """ Синтаксический разбор объекта типа "Точка"
            F - объект типа "файл", откуда читаем MIF
            line - текущая строка в MIF-файле
        """
        regexp = re.compile(r'\s*Point\s+(-*\d+\.*\d*).*\s+(-*\d+\.*\d*).*',  
                            re.IGNORECASE)
        regmatch = regexp.match(line)
        if regmatch:
            x = float(regmatch.group(1))
            y = float(regmatch.group(2))
            self.objects.append(Point(x, y))
        else:
            raise ValueError

    def __syntaxPolyline(self, F, line):
        """ Синтаксический разбор объекта типа "Полилиния"
            F - объект типа "файл", откуда читаем MIF
            line - текущая строка в MIF-файле
        """
        # Обычная одинарная полилиния
        regexp = re.compile(r'^\s*Pline\s+(\d+)\s*$',  re.IGNORECASE)
        regmatch = regexp.match(line)
        if regmatch:
            vertexQuant = int(regmatch.group(1))
            vertexList = []
            for i in range(vertexQuant):
                vertexList.append(MifLayer.__syntaxCordPair(self,F))
            self.objects.append(Polyline(*vertexList))
        # Составная полилиния
        regexp = re.compile(r'^\s*Pline\s+Multiple\s+(\d+)\s*$', re.IGNORECASE)
        regmatch = regexp.match(line)
        if regmatch:
            newMultiPline = MultiPline()
            for i in range(int(regmatch.group(1))):
                vertexQuant = int(F.readline());
                vertexList = []
                for i in range(vertexQuant):
                    vertexList.append(MifLayer.__syntaxCordPair(self,F))
                newMultiPline.addPart(Polyline(*vertexList))
            self.objects.append(newMultiPline)

    def __syntaxRegion(self, F, line):
        """ Синтаксический разбор объекта типа "Полигон"
            (в MapInfo и MIF-файлах площадные объекты называются регионами)
            F - объект типа "файл", откуда читаем MIF
            line - текущая строка в MIF-файле
        """
        regexp = re.compile(r'^\s*Region\s+(\d+)\s*$',  re.IGNORECASE)
        regmatch = regexp.match(line)
        if not regmatch: raise ValueError
        newRegion = Region() 
        for i in range(int(regmatch.group(1))):
            vertexQuant = int(F.readline());
            vertexList = []
            for i in range(vertexQuant):
                vertexList.append(MifLayer.__syntaxCordPair(self,F))
            newRegion.addBorder(*vertexList)
        self.objects.append(newRegion)

    clauseHandlers = {  re.compile(r'\s*Region.*', re.IGNORECASE): __syntaxRegion,
                        re.compile(r'\s*Pline.*',  re.IGNORECASE): __syntaxPolyline,
                        re.compile(r'\s*Point.*',  re.IGNORECASE): __syntaxPoint,
                        re.compile(r'\s*Columns.*',re.IGNORECASE): __syntaxColumns,
                     }
    def loadFromFile(self, F):
        while True:
            nextLine = F.readline();
            if not nextLine: break
            for regexp in MifLayer.clauseHandlers:
                if regexp.match(nextLine):
                    handler = MifLayer.clauseHandlers[regexp]
                    handler(self, F, nextLine)

    def loadColumns(self, F):
        for obj in self.objects:
            nextLine = F.readline();
            if not nextLine: raise ValueError
            obj.setColumns(nextLine, self.columnNames)

def openMIF(mifFileName, midFileName=None):
    # Load spatial objects
    mifFile = open(mifFileName)
    newLayer = MifLayer()
    newLayer.loadFromFile(mifFile)
    mifFile.close()
    # Load header of MIF
    mifFile = open(mifFileName)
    regexp = re.compile(r'\s*Columns.*', re.IGNORECASE)
    while True:
        nextLine = mifFile.readline()
        if not nextLine: break
        if regexp.match(nextLine): break
        newLayer.header.append(nextLine)
    mifFile.close()
    # Load attributes
    if midFileName:
        midFile = open(midFileName)
        newLayer.loadColumns (midFile)
        midFile.close()
    return newLayer

def writeMIF(MIF,mifFileName, midFileName=None):
    mifFile = open(mifFileName, 'w')
    for line in MIF.header: mifFile.write(line)
    mifFile.write("Columns ") 
    mifFile.write(str(len(MIF.columnNames)))
    mifFile.write("\n")
    for col in MIF.columnNames:
        for i in (0,1):
            mifFile.write(" ")
            mifFile.write(col[i])
        mifFile.write("\n")    
    mifFile.write("Data\n\n")
    for obj in MIF.objects: mifFile.write(str(obj))
    mifFile.close()
    # Write atributes to MID-file
    re_char    = re.compile(r'Char', re.IGNORECASE)
    re_logical = re.compile(r'Logical', re.IGNORECASE)
    if midFileName:
        midFile = open(midFileName, 'w')
        for obj in MIF.objects:
            midLine = None
            for col in MIF.columnNames:
                val = getattr(obj, col[0])
                if re_char.match(col[1]): val = '"' + val + '"' 
                if re_logical.match(col[1]): 
                    if val: val = 'T'
                    else:   val = 'F'                 
                if midLine: midLine = midLine + ',' + str(val)
                else:       midLine = str(val)
            midFile.write(midLine)
            midFile.write('\n')
        midFile.close()

#------------------------------------------------------------------------------
if __name__ == '__main__':
    myLayer=openMIF('points.MIF', 'points.MID')
    query = [x for x in myLayer if 
               x.AMENITY=='post_office'
            ]
    print (len(query))



