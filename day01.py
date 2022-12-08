# Advent of Code 2022
# Day 1

# Read the file

file = open('day01-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

# Sum the weights for each elf

weights = []
sum = 0
i = 0
for line in lines:
    line = line.strip()
    if line:
        sum += int(line)
    else:
        weights.append(sum)
        print('Elf #{i} is carrying {sum}'.format(i=i, sum=sum))
        sum = 0
        i = i + 1

# Find the top three

max1 = 0
max2 = 0
max3 = 0

for weight in weights:
    if weight > max1:
        max3 = max2
        max2 = max1
        max1 = weight
    elif weight > max2:
        max3 = max2
        max2 = weight
    elif weight > max3:
        max3 = weight

# Print part 1 results

print('Max is {max1}'.format(max1=max1))

# Print part 2 results

sum_of_top_3 = max1 + max2 + max3
print('Sum of top 3 is {sum_of_top_3}'.format(sum_of_top_3=sum_of_top_3))
