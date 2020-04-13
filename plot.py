from matplotlib import pyplot as plot

f = open('score_log', 'r')
scores = f.readlines()
scores = [int(i) for i in scores]
f.close()

print(scores[-10:])

f = open('time_log', 'r')
time = f.readlines()
time = [int(i) for i in time]
f.close()

pl1 = plot.plot(scores)
pl2 = plot.plot(time)


plot.xlabel("Generation")
plot.ylabel("Score")

plot.show()
