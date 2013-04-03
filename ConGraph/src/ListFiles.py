'''
Created on 3 Apr 2013

@author: moz
'''
import os.path
import xml.etree.ElementTree as etree

BaseDir = "/nobackup/moz/Downloads/sdcard_fix/doc/doxygen/xml"

if __name__ == '__main__':
    print "Parsing xml files from %s"%BaseDir

    Filename = "analog_8c.xml"

    FullFilename = os.path.join( BaseDir, Filename )

  
    tree = etree.parse(FullFilename)
    root = tree.getroot()

    print "Reading compunds in file %s"%FullFilename    
    for c in root.findall( "compounddef" ):
        print "- Readable name: %s"%c[0].text
        print "- Kind: %s"%c.attrib['kind']
        print "- Id: %s"%c.attrib['id']

        print "- Included count: %d"%len(c.findall('includedby'))

        print "- Includes"
        IncList = []
        for i in c.findall( 'includes' ):
            if i.attrib['local'] == 'yes':
                IncList.append( i.attrib['refid'] )
            else:
                print "-- skipping non-local %s"%i.text
        print "-- %s"%IncList

    pass
