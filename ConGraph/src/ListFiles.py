'''
Created on 3 Apr 2013

@author: moz






'''
import os.path
import xml.etree.ElementTree as etree
import glob
import sys
import xml.etree.ElementTree

BaseDir = "/nobackup/moz/Downloads/sdcard_fix/doc/doxygen/xml"


def ReadCompound( c ):
    RetDict = {}
    RetDict['Label'] = c[0].text
    RetDict['Id'] = c.attrib['id']
    RetDict['Kind'] = c.attrib['kind']
    RetDict['IncludedCount'] = len(c.findall('includedby'))
    
#    print "- Readable name: %s" % RetDict['Label']
#    print "- Kind: %s" % RetDict['Kind']
#    print "- Id: %s" % RetDict['Id']
#    print "- Included count: %d" % RetDict['IncludedCount']
#    print "- Includes"
    IncList = []
    for i in c.findall('includes'):
        try:
            if i.attrib['local'] == 'yes':
                IncList.append(i.attrib['refid'])
        except KeyError:
            print >> sys.stderr, "Key error in compound %s includes entry %s - skipping"%(RetDict['Label'], i.text)
#        else:
#            print "-- skipping non-local %s" % i.text
    
#    print "-- %s" % IncList
    RetDict['IncludeList'] = IncList
    return RetDict

def ReadFile(filename):
    print "// %s" % "Reading compounds in file %s" % filename
    tree = etree.parse(filename)
    root = tree.getroot()
    for c in root.findall("compounddef"):
        NodeInfo = ReadCompound(c)
        print "// %s" % NodeInfo
        
        if NodeInfo['IncludedCount'] == 0 and len( NodeInfo['IncludeList']) == 0:
            print >> sys.stderr, " %s not include and includes nothing -- skipping"%NodeInfo['Label']
            continue
            
        print "node [shape = circle,width=1,fixedsize=true]; %s;" % ( NodeInfo['Id'])
        
        # todo: We want some visual thing to say if we have a high IncludedCount
        #print "node [shape = circle,width=%d,fixedsize=true]; %s;" % (NodeInfo['IncludedCount'] + 1, NodeInfo['Id'])
        for inc in NodeInfo['IncludeList']:
            print "%s -> %s;" % (NodeInfo['Id'], inc)
    print "" # output candy

GraphHeader = '''digraph Files {
    label = "Listing files by includes";
    rankdir = LR;
'''
GraphFooter = '''
}
'''    
    
if __name__ == '__main__':
    print "// %s"%"Parsing xml files from %s"%BaseDir

    print GraphHeader

    for filename in glob.glob(os.path.join(BaseDir, '*.xml')):
        #Filename = "analog_8c.xml"
        #FullFilename = os.path.join( BaseDir, Filename )
        try:
            ReadFile(filename )
        except xml.etree.ElementTree.ParseError:
            print sys.stderr, "malformed xml in file %s - skipping"%filename
    
    print GraphFooter
