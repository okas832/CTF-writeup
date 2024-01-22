# Bomberman
## Challenge Information
- Category : Pwnable
- Author : ptr-yudai

## Solution
We can remove the wall at (0, 5) by use-after-free bug.

1. Place the bomb and stay next to it.
2. Move player to bomb position at 0.5 seceond after the bomb explode.
3. Pickup the exploding bomb before the fire extinguish(1 second after the bomb explode).
4. Place the bomb
5. Pickup the bomb

Because of Safe Linking in tcache, the position of freed bomb always set to (0, 5)

However, this does not help to reach the flag on the map.
In upper side of the map, current player's position exist. So instead reaching flag on the map, we can create and go to the flag outside of the map.


