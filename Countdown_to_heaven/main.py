import math

# 高さから落下時間を求める関数
def getTime(height):
	return math.sqrt(2*height/9.80665)

# 落下時間から落下速度を求める関数
def getSpeed(time):
	return time*9.80665*3.6

# 落下速度から高さを求める関数
def getHeight(speed):
	return (speed/3.6)**2/2/9.80665 
