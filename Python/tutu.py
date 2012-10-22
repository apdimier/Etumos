from xml.dom.minidom import Document
doc = Document()

wml = doc.createElement("wml")
doc.appendChild(wml)
print doc.toprettyxml(indent="")
