import base64
enc = "MTE3LDk2LDk4LDEwNyw3LDQzLDIyMCwyMzMsMTI2LDEzMSwyMDEsMTUsMjQ0LDEwNSwyNTIsMTI1LDEwLDE2NiwyMTksMjMwLDI1MCw4MiwyMTEsMTAxLDE5NSwzOSwyNDAsMTU4LDE3NCw1OSwxMDMsMTUzLDEyMiwzNiw2NywxNzksMjI0LDEwOCw5LDg4LDE5MSw5MSwxNCwyMjQsMTkzLDUyLDE4MywyMTUsMTEsMjYsMzAsMTgzLDEzMywxNjEsMTY5LDkxLDQ4LDIyOSw5OSwxOTksMTY1LDEwMCwyMTgsMCwxNjUsNDEsNTUsMTE4LDIyNywyMzYsODAsMTE2LDEyMCwxMjUsMTAsMTIzLDEyNSwxMzEsMTA2LDEyOCwxNTQsMTMzLDU1LDUsNjMsMjM2LDY5LDI3LDIwMSwxMTgsMTgwLDc0LDIxMywxMzEsNDcsMjAwLDExNiw1Miw0OSwxMjAsODYsMTI0LDE3OCw5MiwyNDYsMTE5LDk4LDk1LDg2LDEwNCw2NCwzMCw1NCwyMCwxMDksMTMzLDE1NSwxMjIsMTEsODcsMTYsMjIzLDE2MiwxNjAsMjE1LDIwOSwxMzYsMjQ5LDIyMSwxMzYsMjMy"
enc = b'[' + base64.b64decode(enc) + b']'
enc = eval(enc)[::-1]

key = b'acscpass'

for i in range(len(enc)):
    enc[i] ^= key[i % len(key)]

s = enc[-3]
k = enc[-2]
j = enc[-1]
print(s, k, j)
g = [
      8026407584881212335717763155461175939053253449558928097356743317580304745257836900537741725487713354811898351514317778474405234115608371781687347872491703,
      9901479087075272465000928546760145175528311831313716995411286084780215684429457115750234954269995515521497208022159902709895803492831087888441410900661623,
      8903225968632645048112414558941014482368293389707967329431586917899894237468493767277617251082326067122876205027521423107103664566560453106513383698662841,
      7306065826954797942887008925345768422542194975212611412996809619206152967943872265885214129607801191067761271051786230521446267111488994860029935891658147,
      13002100837416249802976975336617228981498976557336038776019341954643478558536425323716753407024112736914972406623544975287903736193016505594778344376373179,
      11576051655637376487642664054274257390376244499880178084751392229273250591900336107156856829956635498116092894051582635232354596017926523129295080605554429,
      7902539523670688752549365452498382985299018894363342133531323012327857960923461934902488879455588857566708722435022350733082133933092267702307821906957977,
      6783142639439350199274781001550540761424373981915677251043304945175275590386243548101294984514936470982791698773776831533758049672189386462720647770985001,
      11319393487244650012717839752121654225994209596419701136831846093323997458647164935453184402661574913288632779725321036933530944725804415713594714876906847,
      9585387948560465713976215768016745842108284855244208916003456862520169267729486151203630145345165962235437344782253615764252330421571444685028102486610567,
    ]
h = [
      11138133675080925873149032570509408923592577663944493077262179603892338339426376013580530251498364611817562627156767932116957250284539752419366057012361649,
      10574147867451418851637041344231275651423577891311215749455683353579335478795148329490570900445186263552549726662037946613806250295825461252937365691144757,
      10674081755614194430694316863648731761829693259627261111906003227581182291436573479641202865404241412518768803795734995501804298710271483715401954860647953,
      12968732443832149370169937542849870171809900018949150636308457250052280094029579199566526477098080152448048695730264594884959310262897810775613424383036007,
      8972395174076295368444847039674947715229479296809544092248089326976428235345226886712046918654462399484955991711195283733874190395639967899628857836740743,
      9527362749634281224487906953140787001780863710164703682625342548102961426576294773243660413567139103445338886795721973525199297094569903788493496539197863,
      10229709325149619765696926612743287965524038512950567412494449028112447211284065074607122123674007398601575622550266734924682588447213742414387099108109461,
      6775733025973714289289099342079544491278357801546402292504820748645442063442072618107305909729834896739059944218135896652802888272263806165032921710097769,
      11844424614832993323731152366810540116450336338053864348795634499070072404906281126852701590624769842713079092273019871232731892965721940265502359688474441,
      6939919557269991460418095931967704251043296456961607911365019726251568836845834148571433683707268031711944237071545445764147715416436144904514445039547287,
    ]

l = g[j]  # p
o = h[k]  # q
t = 2 ** (2**s) + 1  # e

x = 0
for i in range(len(enc[:-3])):
    x |= enc[i] << (8 * i)
phi = (l - 1) * (o - 1)
d = pow(t, -1, phi)

mm = pow(x, d, l * o)
print(bytes.fromhex(hex(mm)[2:]))


