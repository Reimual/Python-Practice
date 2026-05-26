import argparse

def counts(filename: str) -> int:
    nums: int = 0
    
    if filename == "" or filename == None:
        return -1
    
    with open(filename, "r", encoding='utf-8' , errors='replace') as file:
        text: str = file.readline()
        while text != '':
            if text[-1] == '\n' and len(text) != 1:
                if '#' in text:
                    index: int = text.find('#')
                    for i in range(0, index):
                        if text[i] == "" or text[i] == " ":
                            continue
                        else:
                            nums += 1
                            break
                elif not text[-2] == ' ':
                    nums += 1
            elif text[-1] != '\n' and len(text) == 1:
                nums += 1
                
            text = file.readline()
    
    return nums

def args_func() -> str:
    parser = argparse.ArgumentParser(
        prog="*.py",
        description="Count lines of code"
    )

    parser.add_argument('src', help="source code file")
    
    try:
        arg = parser.parse_args()
             
        return arg.src
    except FileNotFoundError:
        print("No such file or directory: arg")
    except SystemExit:
        ...
        
    return ""

def main():
    filename: str = args_func()
    nums: int = counts(filename)
    
    print(f"This file's code lines is {nums}")

if __name__ == '__main__':
    main()