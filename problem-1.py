# Problem 1: Finding Favorite Times
# To run, input through STDIN. Output will be given through STDOUT.

# Times will be stored as two variables, the hour and the minute.
# This is the easiest to manipulate when incrementing the time.

# Function: determine if a time (hour, minute) has an arithmetic sequence
def has_seq(hour, minute):
    # If the minute is less than 10, then there is a leading zero. Since at
    # least one digit of the hour is positive (12-hour time, so no 0-hour),
    # and the second last digit of the time is zero, the last digit must be
    # negative for the digits to form an arithmetic sequence, which is
    # impossible.
    if minute < 10:
        return False
    
    # Otherwise, we separate the time into its full digits, which we can do
    # using modular arithmetic.
    digits = []

    # If the hour is only one digit, then we do not add a leading zero as
    # described in the assignment.
    if hour < 10:
        digits.append(hour)
    
    # Otherwise, we add both the first digit (always 1) and the second digit.
    else:
        digits.append(1)
        digits.append(hour % 10)
    
    # The first digit of the minute is always included even if it is zero
    # (though we have already filtered out that possibility).
    digits.append(minute // 10)
    digits.append(minute % 10)

    # Then, we take the difference between the first two digits.
    diff = digits[0] - digits[1]

    # Finally, we make sure the difference between each other consecutive pair
    # of digits is the same
    for i in range(1, len(digits) - 1):
        if digits[i] - digits[i + 1] != diff:
            return False
    
    # If we found no mismatches, this is an arithmetic sequence.
    return True

# Input processing: input the number of steps to take.

try:
    D = int(input())
except:
    raise SystemExit("Please enter an integer.")

if D < 0:
    raise SystemExit("Please enter a positive integer.")

# Optimization: Since D can be up to 1 billion, and just a simple loop would
# take ridiculously wrong for that, we observe that every 12 hours, the cycle
# starts over exactly the same.

# In every 720 minutes, there are 31 arithmetic sequences (pre-computed using
# the unoptimized method). Therefore, if D is larger than 720, we can subtract
# 720 from D and add 31 to the count, and repeat as many times as needed.

# Floor-divide D by 720 to get the number of repetitions, then take the
# remainder and compute manually.
count = 31 * (D // 720)
D %= 720

# Initial value: time starts at 12:00.
hour = 12
minute = 0

# We need to loop D + 1 times to include the end time as well.
for _ in range(D + 1):
    # Check first so we start at 12:00 and not 12:01, and end at the right
    # time.
    if has_seq(hour, minute):
        count += 1

    # Then, increment.
    # If we've reached X:59, then we need to go to the next hour.
    if minute == 59:
        # If we've reached 12:59, we need to go to 1:00 instead of 13:00.
        if hour == 12:
            hour = 1
        
        # Otherwise, just increment the hour.
        else:
            hour += 1

        # Finally, reset the minute to 0.
        minute = 0
    
    # Otherwise, just increment the minute.
    else:
        minute += 1
    

# Finally, output the total count.
print(count)