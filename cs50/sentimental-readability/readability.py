import string

def main():
    u_input = input("Text: ")
    l = Letters(u_input)
    w = Words(u_input)
    s = Sentences(u_input)
    i = round(Index(l, s, w))
    if i < 1:
        print("Before Grade 1")
    elif i >16:
        print("Grade 16+")
    else:
        print("Grade", i)

def Letters(u_input):
    alphabetic_count = sum(char in string.ascii_letters for char in u_input)
    return alphabetic_count


def Words(u_input):
    spaces = u_input.count(" ")
    return spaces + 1


def Sentences(u_input):
    symbals = [".", "?", "!"]
    count = 0
    for symbal in symbals:
        count += u_input.count(symbal)
    return count


def Index(l, s, w):
    index = (0.0588 * l / w * 100) - (0.296 * s / w * 100) - 15.8
    return index

main()
