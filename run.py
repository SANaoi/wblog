import pyttsx3

a = [1,2,3,4,5,6]
b = [5,6,1,2,9,8]
c = ['a',1,4,'b']

new = set(a).intersection(b,c)

all_list = [[1, 2, 3, 4, 5, 6], [5, 6, 1, 2, 9, 8], ['a', 1, 4, 'b', 2],[1,2]]
p = set.intersection(*map(set, all_list))
print(p)

engine = pyttsx3.init()
engine.say('hello world')
engine.runAndWait()
pyttsx3.speak("你好")