'''
Created on 3 Apr 2013

@author: moz



'''
import os.path
import xml.etree.ElementTree as etree

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
        if i.attrib['local'] == 'yes':
            IncList.append(i.attrib['refid'])
#        else:
#            print "-- skipping non-local %s" % i.text
    
#    print "-- %s" % IncList
    RetDict['IncludeList'] = IncList
    return RetDict

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

    Filename = "analog_8c.xml"

    FullFilename = os.path.join( BaseDir, Filename )
  
    print "// %s"%"Reading compounds in file %s"%FullFilename    
    tree = etree.parse(FullFilename)
    root = tree.getroot()

    for c in root.findall( "compounddef" ):
        NodeInfo = ReadCompound(c) 
        print "// %s"%NodeInfo
        
        print "node [shape = circle,width=%d,fixedsize=true]; %s;"%(NodeInfo['IncludedCount']+1, NodeInfo['Id'])
        for inc in NodeInfo['IncludeList']:
            print "%s -> %s;"%(NodeInfo['Id'], inc)

    
    print GraphFooter
