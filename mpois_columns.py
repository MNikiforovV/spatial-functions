# -*- coding: utf-8 -*-
import re

class Columns():
    def setColumns(self,csvString,columnNames):
        C = csvString.split(',')
        regexp = re.compile(r'\s*\"(.+)\"\s*', re.IGNORECASE)
        for col, v in zip(columnNames, C):
            name, colType = col
            if colType=='Logical':
                if   'T' in v: v = True 
                elif 'F' in v: v = False
                else: v = None
            if colType=='Integer':
                v = int(v)
            if colType=='Float':
                v = float(v)
            if 'Char' in colType:
                regmatch = regexp.match(v)
                if regmatch: v = regmatch.group(1)
                else: v = str(v)
            setattr(self,name,v)

def transitiveClosure(Layer, startWith, connectBy, childList):
    (child, parent) = connectBy.split('=')
    for obj in Layer:
        if getattr(obj,parent)==startWith:
            childList.append(obj)
            transitiveClosure(Layer, getattr(obj,child), connectBy, childList)
            