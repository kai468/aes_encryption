  
# Using readlines()
file1 = open('myInput.txt', 'r')
Lines = file1.readlines()
file1.close()

# prepare output
file1 = open('myOutput.txt', 'a')
  
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    #print("Line{}: {}".format(count, line.strip()))
    file1.write('print "')
    file1.write(line.strip())
    file1.write('"\n')

file1.close()

for i in range(65,73):
		print(chr(i))
for i in range(1,9):
    print(i)