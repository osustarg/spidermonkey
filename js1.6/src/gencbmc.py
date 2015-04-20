import glob

def remCom(s):
    s2 = s.split(r"/*");
    s3 = s
    if len(s2) > 1 and r"*/" in s:
        s3 = s2[0] + s.split(r"*/")[1]
    return s3
        
baseTypes = ["int","short","long","char","size_t","void"]

rawTypedefs = []

for f in glob.glob("*.h"):
    typedef = ""
    ender = ";"
    inTypedef = False
    for l in open(f):
        l = remCom(l)
        ls = l.split()
        if not inTypedef:
            if len(ls) > 0 and ls[0] == "typedef":
                if len(ls) > 1 and ls[1] == "struct" and "{" in l:
                    ender = "}"
                else:
                    ender = ";"
                if ender in l:
                    rawTypedefs.append(l)
                    typedef = ""
                else:
                    inTypedef = True
        if inTypedef:
            typedef = typedef + l
            if ender in l:
                rawTypedefs.append(typedef)
                typedef = ""
                inTypedef = False

depend = dict()
typedef = dict()

for t in rawTypedefs:
    print "============================="
    s = t.split()
    defined = s[-1].split(";")[0]
    typedef[defined] = t
            
    if s[1] not in ["struct","union","enum"]:
        depend[defined] = s[1]
    elif s[1] in ["struct","union"]:
        ls = t.split("\n")
        depend[defined] = []
        for l in ls:
            if ("{" not in l) and ("}" not in l) and ("typedef" not in l):
                ts = l.split()
                if len(ts) > 1:
                    type = l.split()[0]
                    depend[defined].append(type)
    else:
        depend[defined] = []
    print "DEFINED: " + defined
    print "DEPEND: " + str(depend[defined])
    print t
            
            
