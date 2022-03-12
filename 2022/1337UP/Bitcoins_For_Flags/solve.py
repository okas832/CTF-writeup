a = [3481208486, 3103842858, 344481046, 529018163, 575205860, 353026313, 1190179403, 2348606633, 579662040, 2545240700, 2797676555, 636588589, 384605791, 4071049476, 731109131]

v = 0x811C9DC5

table = {}

word = open("words_alpha.txt", "rb").readlines()

for w in word:
    w = w.strip()
    nv = v
    for l in w:
        nv = ((nv * 0x1000193) ^ l) & 0xFFFFFFFF
    if nv in a:
        table[nv] = w

if len(table) == len(a):
    ans = []
    for k in a:
        ans.append(table[k])

    ans = b" ".join(ans)
    print(ans)