'''
Created on Apr 22, 2013

@author: moz

astparser
Parses the xml output in data/astparser.py

'''
import xml.etree.ElementTree as etree
import sys

FileToProcess = "data/ast-data.xml"


def ProcessStatement(stat, counter):
    StatementType = stat.attrib['tokenValue']
    
    if StatementType == '{':
        # omitted - it looks bad :-)
        #print >> sys.stderr, "%s%s"%('.'*counter, StatementType)

        nextcstat = stat.find('compoundStatement')
        ProcessCompoundStatement(nextcstat, counter+1)
        return
    
    # if statements, contains statements.
    if StatementType == 'if':
        print >> sys.stderr, "%s%s"%('.'*counter, StatementType)
        
        ifstat = stat.find('ifStatement')
        
        # statements in if statement
        for substat in ifstat.findall('statement'):
            ProcessStatement(substat, counter+1)        
            
        # else clause (if exists)
        elscl = ifstat.find('elseClause')
        print >> sys.stderr, "%s%s"%('.'*counter, 'else')

        for substat in elscl.findall( 'statement'):
            ProcessStatement(substat, counter+1)        

        return
    
    print >> sys.stderr, "%s%s \t(unknown statement)"%('.'*counter, StatementType)
    

def ProcessCompoundStatement(cs, counter):
    for i in cs:
        if i.tag == 'statement':
            ProcessStatement(i, counter)
            continue
        
        if i.tag == 'declaration':
            decl = i.attrib['tokenValue']
            print >> sys.stderr, "%s%s \t(function call)"%('.'*counter, decl) 
            continue
               

def ExtractFunctions( filename ):
    print >> sys.stderr, "Reading compounds in file %s" % filename
    tree = etree.parse(filename)
    root = tree.getroot()

    # find all function declarations
    for fctdef in root.iter('functionDefinition'):
        #print >> sys.stderr, fctdef.tag, fctdef.attrib
        
        fct = fctdef.find( 'functionDeclarator')
        print >> sys.stderr, "Function name: %s"%fct.attrib['tokenValue']
        
        # process "compoundStatements" (recursively)
        for cs in fctdef.findall('compoundStatement'):
            counter = 1           
            ProcessCompoundStatement(cs, counter)

if __name__ == '__main__':
    ExtractFunctions(FileToProcess)
    
    pass