from xml.dom.minidom import parseString,Document
import uuid
import urllib2
class TTNCApi:
  def __init__(self,username=False,password=False,vkey=False):
    self._username=username
    self._password=password
    self._vkey = vkey
    self.response = False
    self.requests={}
    self.requests_priority={}
    self.doc = Document()
    self.root = self.doc.createElement('NoveroRequest')
    self.doc.appendChild(self.root)
    if username!=False and password!=False : 
        self.sessionrequest()
         
  def sessionrequest(self):
      request = self.newrequest('Auth', 'SessionLogin', 'SessionRequest')
      request.setdata('Username',self._username)
      request.setdata('Password',self._password)
      if self._vkey:
          request.setdata('VKey',self._vkey)
  def usesession(self,session):
        child = self.doc.createElement("SessionId")
        text=self.doc.createTextNode(session)
        child.appendChild(text)
        self.root.appendChild(child)
  def newrequest(self,target,name,id=False):
      request = TTNCRequest(self,target,name,id)
      if target=="Auth":
          self.requests_priority[request.getid()]=request
          return self.requests_priority[request.getid()]
      else:
          self.requests[request.getid()]=request
          return self.requests[request.getid()]
      
  def makerequests(self):
      for item in self.requests_priority.values():
          self.root.appendChild(item.get())
      for item in self.requests.values():
          self.root.appendChild(item.get())
      xml_request= str(self.doc.toxml())
      #print self.root.toprettyxml()
      url="https://xml.ttnc.co.uk/api/"
      req = urllib2.Request(url,data="none",headers={'Content-type': 'text/xml'})
      req.add_data(xml_request)
      resp = urllib2.urlopen(req)
      dom = parseString(resp.read())
      #print dom.toxml()
      self.response=TTNCResponse(dom)
  def getresponsefromid(self,id):
     xml = self.response.get()
     Response=xml.getElementsByTagName('Response')
     for item in Response:
        if item.getAttribute("RequestId")==id:
            return self.requesttoarray(item)
  def requesttoarray(self,xml):
      all_infos={}
      if xml.attributes is not None and xml.attributes.length>0:
          all_infos['@attributes']={}
          for keys in xml.attributes.keys():
            all_infos['@attributes'][keys]=xml.getAttribute(keys)
      for item in xml.childNodes:
          if item.localName is not None :
              if item.childNodes.length > 1:
                  all_infos[item.localName]=self.requesttoarray(item)
              else:
                 for items in item.childNodes:
                     all_infos[item.localName]=items.toxml()
      return all_infos       
      
      
class  TTNCRequest:
    def __init__(self,api,target,name,id):
        self.response=False
        self.api=api
        self.target=target
        self.name=name
        if id!=False :
            self.requestid=id
        else:
            self.requestid=self.generaterequestid()
        
        self.doc = Document()
        self.root = self.doc.createElement("Request")
        self.doc.appendChild(self.root)
        self.root.setAttribute("target",target)
        self.root.setAttribute("name",name)
        self.root.setAttribute("id",self.requestid)
        
        
    def generaterequestid(self):
        return str(uuid.uuid1())
    def getid(self):
        return self.requestid
    def setdata(self,key,value):
        child = self.doc.createElement(key)
        text=self.doc.createTextNode(value)
        child.appendChild(text)
        self.root.appendChild(child)
    def get(self):
        return self.root
    def getresponse(self):
        if self.api.response==False:
            return False
        return self.api.getresponsefromid(self.requestid)
    
class TTNCResponse:
    def __init__(self,response):
       if isinstance(response, str):
          self.xml=parseString(response)
       elif isinstance(response, Document):
           self.xml=response
    def get(self):
        return self.xml
