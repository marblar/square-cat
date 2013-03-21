import libxml2
log = ""
class callback:
    def startDocument(self):
        global log
        log = log + "startDocument:"

    def endDocument(self):
        global log
        log = log + "endDocument:"

    def startElement(self, tag, attrs):
        global log
        log = log + "startElement %s %s:" % (tag, attrs)

    def endElement(self, tag):
        global log
        log = log + "endElement %s:" % (tag)

    def characters(self, data):
        global log
        log = log + "characters: %s:" % (data)

    def warning(self, msg):
        global log
        log = log + "warning: %s:" % (msg)

    def error(self, msg):
        global log
        log = log + "error: %s:" % (msg)

    def fatalError(self, msg):
        global log
        log = log + "fatalError: %s:" % (msg)

handler = callback()
ctxt = libxml2.parseFile("contents/index.apxl")
xp = ctxt.xpathNewContext()
xp.xpathRegisterNs("sf","http://developer.apple.com/namespaces/sf")

substitutions = xp.xpathEval("//sf:text[contains(./sf:text-storage/sf:text-body/sf:p,'kc:')]")

template = """
<sf:movie-media sfa:ID="SFDMovieMedia-1" sf:muted="false" sf:volume="1" sf:poster="0" sf:looping="no">
 <sf:self-contained-movie>
  <sf:main-movie sfa:ID="SFEData-42" sf:path="%s" sf:displayname="%s" sf:hfs-type="1299148630" sf:size="3316352"/>
  <sfa:main-movie-data-description sfa:ID="SFDMovieMediaDataDescription-0" sfa:length="3215" sfa:hash="599C8C690EF730D14C7C3DBBA2E016BD885BCAF80E89608776A3F7C4E6CDFF18"/>
 </sf:self-contained-move>
</sf:movie-media>
"""

if not substitutions:
    print "Error: no substitutions found."
    exit(1)

print "Matches: %s" % substitutions

for substitution in substitutions:
    contentNode = substitution.parent.parent.parent.parent.parent.parent
    print contentNode.name
    kcPlaceholder = substitution.children.children.next.children.children
    print kcPlaceholder
    kc,filename = str(kcPlaceholder).split(":",1)
    print "Replacing %s" % filename
    substitution.unlinkNode()
    contentNode.addChild(libxml2.newNode(template % (filename,filename)))

ctxt.saveFile("contents/index.apxl")

