# Problem 2: Blood Distribution
# To run, input through STDIN. Output will be given through STDOUT.

# Index Map:
# O-  O+  A-  A+  B-  B+  AB-  AB+
# 0   1   2   3   4   5   6    7

# General approach: we note that because there is no priority or weight placed
# on people, we are just maximizing the amount of blood that can be given and
# do not need to worry about who it is given to. That is, we can greedily
# select how to distribute the blood as long as the order of our assignment
# results in the greatest amount delivered.

# Firstly, we can begin by giving as much blood as possible to the person of
# the matching type. To see why this is true, consider how this could be false.
# Since we established that all people are weighted the same, the only
# situation in which it would be suboptimal to give blood to someone of the
# same type is if we need them to receive a different type so someone else can
# use that type. However, compatibility is transitive (if type X can receive
# type Y and type Y can receive type Z, then type X can receive type Z), the
# second person can just receive that backup blood.

# Input: take two rows of space-separated integers.
blood = list(map(int, input().split()))
patients = list(map(int, input().split()))

# Keep a running total of blood given.
total = 0

# Now, let's define a utility function that will assign blood type X to patient
# type Y and return the amount distributed, as well as updating the counts.

# Function: b = blood count, p = patient count, x = blood type, y = patient type
def transfer(b, p, x, y):
    units = min(b[x], p[y])
    b[x] -= units
    p[y] -= units
    return units

# Give as much blood as possible to the matching type.
for i in range(8):
    total += transfer(blood, patients, i, i)

# At this point, O- patients can be removed from the pool since they cannot
# receive anything other than O- and we've already distributed as much as
# possible. A-, B-, and O+ can only receive their own type and O-, so they
# should have the highest priority to receive the O- as the other patients are
# more likely to be able to receive other backup types.

# Keep in mind that the ordering here does not matter. If giving blood to an O+
# means we cannot give it to a B-, giving it to the B- instead of the O+ does
# not change our end result.
for i in [1, 2, 4]:
    total += transfer(blood, patients, 0, i)

# At this point, we've given as much O- and X blood as possible to type X
# patients where X is one of A-, B-, and O+, so there is no blood left for
# these patients. A+, B+, and AB- are next as they can receive 4 types of blood
# whereas AB+ can receive all 8 and should be left for the end.

# Also, we should prioritize distributing the O- and O+ blood before giving the
# A- and B- blood to the A+ and B+ patients because AB- can accept that but not
# O+. The only question is whether we should give to the A+ patients first or
# the B+ patients, and I've found through testing that neither order will
# always be correct, so we must try both and return the maximum result.

# Duplicate the totals and blood/patient counts
total1 = total2 = total
blood1 = blood[:]
blood2 = blood[:]
patients1 = patients[:]
patients2 = patients[:]

# First, try giving to the A+ patients first, prioritizing O+ blood as AB-
# cannot accept that.
for blood_type in [1, 0]:
    # A+ (3) before B+ (5)
    total1 += transfer(blood1, patients1, blood_type, 3)
    total1 += transfer(blood1, patients1, blood_type, 5)

    # B+ (5) before A+ (3)
    total2 += transfer(blood2, patients2, blood_type, 5)
    total2 += transfer(blood2, patients2, blood_type, 3)

# Now, we can also try giving A- blood to A+ patients and B- blood to B+
# patients.
total1 += transfer(blood1, patients1, 2, 3)
total1 += transfer(blood1, patients1, 4, 5)

total2 += transfer(blood2, patients2, 2, 3)
total2 += transfer(blood2, patients2, 4, 5)

# Finally, we just need to try transfering A-, B-, and O- blood to AB-, and
# then the remaining blood to AB+.

for i in [0, 2, 4]:
    total1 += transfer(blood1, patients1, i, 6)
    total2 += transfer(blood2, patients2, i, 6)

# (Exclude 7 => 7 since we already did that.)
for i in range(7):
    total1 += transfer(blood1, patients1, i, 7)
    total2 += transfer(blood2, patients2, i, 7)

# Finally, output the better of the two approaches.
print(max(total1, total2))