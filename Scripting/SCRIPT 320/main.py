def create():
    """Takes the bee movie script and makes it all one line"""
    # Make all the lines one line
    with open('<YOUR DIR HERE>beeMovieScript.txt', 'r') as f:
        lines = f.readlines()
    beeString = ''
    for line in lines:
        beeString += ' ' + line.strip('\n')
    # Write to the file
    with open('<YOUR DIR HERE>beeMovieLine.txt', 'w') as f:
        f.write(beeString[1:])

def solve():
    """Users have to find the words from the 3rd - 16th numbers of the fibonacci sequence"""
    # Open the file and read the line into variable.
    with open('<YOUR DIR HERE>beeMovieLine.txt', 'r') as f:
        line = f.readline()
    # Turn string into list of words.
    words = line.split()
    # Create blank string.
    output = ""
    for n in range(0, 20+1):  # First num is start; Second num is stop (+1 to account for it being inclusive).
        # Pass number into Fibonacci function & get back its value.
        FibNum = Fibonacci(n)
        # Use Fibonacci number to get list indexed word. Add one to account for list index starting at 0.
        output += words[FibNum]
    return output

# Function for nth Fibonacci number
def Fibonacci(n):
    """This is code ripped from stack exchange. It uses recursion to give you the desired fibonacci number"""
    # Check if input is 0 then it will
    # print incorrect input
    if n < 0:
        print("Incorrect input")

    # Check if n is 0
    # then it will return 0
    elif n == 0:
        return 0

    # Check if n is 1,2
    # it will return 1
    elif n == 1 or n == 2:
        return 1

    else:
        return Fibonacci(n - 1) + Fibonacci(n - 2)

if __name__ == '__main__':
    create()
    print(solve())
