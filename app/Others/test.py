def biggest(r, l, u, d):
	big = r
	if big<l:
		big = l
	if big<u:
		big = u
	if big<d:
		big = d
	
	if big==r:
		return "right"
	if big==l:
		return "left"
	if big==u:
		return "up"
	
	return "down"

print (biggest(1, 2, 2, 0))
print (biggest(18, 2, 2, 0))

i = 1
j = 1
print(i==j)