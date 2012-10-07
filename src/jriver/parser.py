'''
Created on Jul 4, 2012

@author: tolga

'''


from xml.etree import ElementTree
XML=ElementTree

class McwsParser(object):
    
    def parse(self, packet):
        return packet


class McwsSignatureParser(McwsParser):

    def parse(self, packet):
        siglist = packet.split(';')
        out = {}
        out['len'] = int(siglist[1])
        out['index'] = int(siglist[2])
        out['keys'] = siglist[3:]
        
        return out
    
class McwsXmlParser(object):
    def parse(self, packet):
        try:
            xml = ElementTree.fromstring(packet)
        except:
            errortxt = 'Cannot parse XML packet: \n\n' + repr(packet) +'\n\n'
            logging.error(errortxt)
            raise
            
        
        return self.parse_xml(xml)

    def parse_xml(self, tree):
        return XML.dump(tree)

class McwsMplParser(McwsXmlParser):
    def parse_xml(self, tree):
        items=[]

        if tree.tag != 'MPL':
            logging.error('MPL excepted in XML but got: \n\n' + repr(XML.dump(tree)))
            raise 
            

        for itemTree in tree.findall('Item'):
            item={}
            for fieldTree in itemTree.findall('Field'):
                name= fieldTree.attrib.get('Name')
                value= fieldTree.text
                item[name]=value
            items.append(item)
        
        return items

    
class McwsResponseParser (McwsXmlParser):

    def parse_xml(self, response):
        out= {}
        assert response.tag=='Response'
        
        # Is valid response?
        try:
            if response.attrib.get("Status")=="OK":
                out['status']= True
                out.update(self.parse_data(response))
                
            elif response.attrib.get("Status")=="Failure":
                out['status']= False
                out['data']= response.attrib.get("Information")
            else: 
                logging.error('Unexpected Response: ' + repr(response))
                raise 
        except:
            logging.error("Cannot read response: " + repr(response))
            raise 

        return out

    def parse_data(self, tree):
        "<Item Name= {name}> {value} </Item>"
        d={}
        for e in tree.findall('Item'):
            d[e.attrib["Name"]] = e.text
        return d

class FieldsItemsParser(object):
    def parse_data(self, tree):
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

