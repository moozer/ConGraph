'''
Created on 3 Apr 2013

@author: moz

Basic program that processes doxygens xml output.
- input: doxygen xml (as in all xml files from the "basedir" directory)
- output: .dot data of connected files in file specified in "FilesGraphDotFilename" var

to use the output run something like this on the command line
- fdp -Tpng -o output.png FileIncludes.dot
(it is ugly, and some parameters need to be tweaked...)

'''
import os.path
import xml.etree.ElementTree as etree
import glob
import sys
import xml.etree.ElementTree

BaseDir = "/nobackup/moz/Downloads/sdcard_fix/doc/doxygen/xml"
FilesGraphDotFilename = "FileIncludes.dot"

def ReadCompound( c ):
    RetDict = {}
    RetDict['Label'] = c[0].text
    RetDict['Id'] = c.attrib['id'].replace('-', '_')
    RetDict['Kind'] = c.attrib['kind']
    RetDict['IncludedCount'] = len(c.findall('includedby'))
    
    IncList = []
    for i in c.findall('includes'):
        try:
            if i.attrib['local'] == 'yes':
                IncList.append(i.attrib['refid'].replace('-', '_'))
        except KeyError:
            print >> sys.stderr, "Key error in compound %s includes entry %s - skipping"%(RetDict['Label'], i.text)

    RetDict['IncludeList'] = IncList
    return RetDict

def ExtractFileRelation(filename, MaxIncCount = -1, MaxIncCountId = "none"):
    print "// %s" % "Reading compounds in file %s" % filename
    tree = etree.parse(filename)
    root = tree.getroot()

    for c in root.findall("compounddef"):
        NodeInfo = ReadCompound(c)
        print "// %s" % NodeInfo
        
        if NodeInfo['Kind'] != 'file':
            print >> sys.stderr, " %s not a file-- skipping"%NodeInfo['Label']
            continue

        if NodeInfo['IncludedCount'] == 0 and len( NodeInfo['IncludeList']) == 0:
            print >> sys.stderr, " %s not include and includes nothing -- skipping"%NodeInfo['Label']
            continue
        
            
        print 'node [shape = circle,width=1]; "%s";' % ( NodeInfo['Id'])
        
        # todo: We want some visual thing to say if we have a high IncludedCount
        #print "node [shape = circle,width=%d,fixedsize=true]; %s;" % (NodeInfo['IncludedCount'] + 1, NodeInfo['Id'])
        for inc in NodeInfo['IncludeList']:
            print '"%s" -> "%s";' % (NodeInfo['Id'], inc)
            
        if NodeInfo['IncludedCount'] > MaxIncCount:
            MaxIncCount = NodeInfo['IncludedCount']
            MaxIncCountId = NodeInfo['Id']
            
        print "" # output candy
    return MaxIncCount, MaxIncCountId

DigraphHeader = '''digraph Files {
    label = "Listing files by includes";
    rankdir = LR;
'''
DigraphFooter = '''
}
'''    
    
if __name__ == '__main__':
    
    #RelDotFile = open( FilesGraphDotFilename, 'w+' )
    RelDotFile = sys.stdout
    
    print >> RelDotFile, "// %s"%"Parsing xml files from %s"%BaseDir

    print >> RelDotFile, DigraphHeader
    MaxIncCount, MaxIncCountId = -1, "none"
    
    for filename in glob.glob(os.path.join(BaseDir, '*.xml')):
        try:
            MaxIncCount, MaxIncCountId = ExtractFileRelation(filename, MaxIncCount, MaxIncCountId )
        except xml.etree.ElementTree.ParseError:
            print >> sys.stderr, "malformed xml in file %s - skipping"%filename
    
    print >> RelDotFile, 'graph [ranksep=3, root="%s"];'%MaxIncCountId
    print >> RelDotFile, DigraphFooter
