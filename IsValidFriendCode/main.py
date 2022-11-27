# See: https://www.3dbrew.org/wiki/FRDU:IsValidFriendCode

import hashlib


def is_valid_friend_code(friend_code: int) -> bool:
	return ((friend_code >> 32) == (hashlib.sha1((friend_code & 0xFFFFFFFF).to_bytes(4, byteorder="little")).digest()[0] >> 1))


# 0000-0000-0135 => True
print(is_valid_friend_code(135))
