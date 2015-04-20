import glob

funcs = []

okTypes = ["int","short","long","unsignedint","unsignedshort","unsignedlong","char","size_t","char*","int*","void"]

typedefs = []

for f in glob.glob("*.h"):
    print "SCANNING " + f
    for l in open(f):
        if "typedef" in l:
            typedefs.append(l)

changed = True
while changed:
    changed = False
    for l in typedefs:
        r = l.replace("unsigned int","unsignedint")
        r = r.replace("unsigned short","unsignedshort")
        r = r.replace("unsigned long","unsignedlong")
        ls = r.split();
        if (len(ls) == 3) and (ls[0] == "typedef") and (ls[1] in okTypes):
            if (ls[2][:-1]) not in okTypes:
                okTypes.append(ls[2][:-1])
                changed = True

print "OK TYPES:" + str(okTypes)                         

for f in glob.glob("*.c"):

    last = ""
    inFunc = False
    body = []
    for l in open(f):
        #print l[:-1]
        flushRight = (l.split() != []) and (l.split()[0][0] == l[0]) and (l[0] not in ['{','}'])
        if flushRight:
            if inFunc:
                inFunc = False
                funcs.append((fType, fName, fParams, body))
                body = []
            ps = l.split("(")
            if (len(ps) > 1) and (l[0] not in ['#','//']):
                inFunc = True
                fName = ps[0]
                fParams = (ps[1].split(")"))[0].split(",")
                
                if last.find("static") == 0:
                    fType = (last.split("static "))[1].split()[0]
                elif last.split() != []:
                    fType = last.split()[0]
                else:
                    continue
            last = l
        elif inFunc:
            body.append(l[:-1])

assertCount = 0
noAssertCount = 0

badTypes = []

for (fType,fName,fParams,body) in funcs:
    assertIn = False
    for b in body:
        if "ASSERT" in b:
            assertIn = True
    badType = False
    for p in fParams:
        ps = p.split()
        if len(ps) > 1:
            pt = ps[0]
            if (pt == "const") or (pt == "unsigned"):
                pt = ps[1]
            if (pt[-1] == '*'):
                pt = pt[:-1]
            if pt not in okTypes:
                if pt not in badTypes:
                    badTypes.append(pt)
                badType = True

    if assertIn and not badType:
        print fType + " " + fName + " " + str(fParams)
        for b in body:
            print b
        assertCount = assertCount + 1
        print "====================="
    else:
        noAssertCount = noAssertCount + 1


print str(assertCount) + " functions suitable"
print str(assertCount + noAssertCount) + " total functions"
print str(float(assertCount)/float(noAssertCount+assertCount)*100.0) + "% of functions might be suitable"

print "BAD TYPES:" + str(badTypes)
