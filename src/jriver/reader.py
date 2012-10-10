'''
Created on Jul 4, 2012

@author: tolga

'''

from xml.etree import ElementTree as ET
import logging

class TextReader():
   
    def read(self, stream):
        return stream.read()
    
    def parse(self, txt):
        return txt

class XmlReader():

    def read(self, stream):
        return ET.parse(stream)
    
    def parse(self, xmldata):
        return ET.tostring(xmldata)

class McwsSignatureReader(TextReader):
    
    def parse(self, packet):
        siglist = packet.split(';')
        out = {}
        out['len'] = int(siglist[1])
        out['index'] = int(siglist[2])
        out['keys'] = siglist[3:]
        
        return out
    
class McwsResponseReader (XmlReader):

    def parse(self, tree):
        out= {}
        
        response = tree.getroot()
        
        try:
            assert response.tag == 'Response'
            
        except Exception as e:
            logging.error('Cannot parse element tree. Root element "Response" expected, found: ' + response.tag)
            raise e
        
        # Is valid response?
        try:
            if response.attrib.get("Status")=="OK":
                out['status']= True
                out.update(self.parse_response(response))
                
            elif response.attrib.get("Status")=="Failure":
                out['status']= False
                out['data']= response.attrib.get("Information")
            else: 
                logging.error('Unexpected Response: ' + repr(response))
                raise 
        except Exception as e:
            logging.error("Cannot read response: " + repr(response))
            raise e

        return out
    

    def parse_response(self, response):
        '''
        should be overwritten by lowerlevel parsers
        '''
        return dict(xmlstr=ET.tostring(response))


   

    
class McwsItemValueReader(McwsResponseReader):

    def parse_response(self, tree):
        "<Item Name= {name}> {value} </Item>"
        d={}
        for e in tree.findall('Item'):
            d[e.attrib["Name"]] = e.text
        return d


class FieldsItemsReader(McwsResponseReader):

    def parse_response(self, tree):
        """
        <Item>
        <Field Name= {name}> {value} </Field>
        ...
        <Item>
        ...
        
        """
        itemlist = []
        for item in tree.findall('Item'):
            itemd = {}
            for field in item.findall('Field'):
                itemd[field.attrib["Name"]] = field.text
            itemlist.append(itemd)
        return itemlist


class McwsMplReader(XmlReader):
    def parse(self, tree):
        root = tree.getroot()
        
        items=[]

        if root.tag != 'MPL':
            logging.error('MPL excepted in XML but got: \n\n' + repr(ET.tostring(tree)))
            raise 
            

        for itemTree in root.findall('Item'):
            item={}
            for fieldTree in itemTree.findall('Field'):
                name= fieldTree.attrib.get('Name')
                value= fieldTree.text
                item[name]=value
            items.append(item)
        
        return items

