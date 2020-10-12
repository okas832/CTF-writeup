from Crypto.Util.number import long_to_bytes

c=0x6f86e49629be8a5e21e2c0da25b795e05f0a6ce944db124c3a6c1487c6366b6d95061c2d119ef872cc9b748773a752720c5b928d7ca935ebc5d61e1c9e7ed36e433593d06c26b495e59928635eebad40ce2667f732b2030d302493843a19ac6f11bb0b5b418d9d491ab121d97943bc831c3698b95a53d9f4a3993467a28bce06
n=122473281967438489245200697284209085987870862283159865766870179887073743162940196687790020000214348808748860823908604767044897851166168164492210236033531220345674450723507633030168013139661432069654897358471472862044385693485920354874587842549791152511954498099227284018784968830037098759971168868584379278973
e=65537

print(long_to_bytes(pow(c, e, n)).split(b'\x00')[1])