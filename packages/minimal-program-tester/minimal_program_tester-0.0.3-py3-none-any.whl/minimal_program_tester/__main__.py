
from minimal_program_tester import search_for_testcases, check_file

from colorama import init as colorama_init
from colorama import Fore, Back
from colorama import Style
import argparse

DEFAULT_TIME_LIMIT = 2 # in seconds

time_limit = DEFAULT_TIME_LIMIT

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', "--exec",)
    parser.add_argument('-f', "--folder",)
    parser.add_argument('-t',"--timelimit")
    args = parser.parse_args()

    try:
        exe_path = args.exec
        tests_folder = args.folder
        time_limit_arg = args.timelimit
        if time_limit_arg is not None and time_limit_arg.isnumeric():
            time_limit = float(time_limit_arg)
        print(f"{Back.MAGENTA}{Fore.YELLOW}Files loaded{Style.RESET_ALL}")
    except Exception  as e:
        print("ERROR",e)
        print(f"{Back.RED}{Fore.YELLOW}ERROR:{Style.RESET_ALL} The executable, or test folder path is invalid" )





    testcases = search_for_testcases(tests_folder)

    print(f"{Back.MAGENTA}{Fore.YELLOW}Test cases parsed{Style.RESET_ALL}")

    show_diff = True

    counter = 0
    print(len(testcases))
    for number, testcase in testcases:
        print(f"TESTCASE[{number}]: ",end="")
        correct, differences, result, TE_FLAG  = check_file(exe_path,tests_folder + r'\\' + testcase.input_file,tests_folder + r'\\' + testcase.output_file, timeout_s = time_limit)

        if  TE_FLAG:
            print(f"{Fore.RED}TE{Style.RESET_ALL}")
            continue

        if result != 0:
            print(f"{Fore.RED}SG{Style.RESET_ALL}")
            continue

        if correct:
            print(f"{Fore.GREEN}OK{Style.RESET_ALL}")
            counter += 1
        else:
            print(f"{Fore.RED}WA{Style.RESET_ALL}")
            if show_diff and len(differences):

                print(f"{Fore.YELLOW}{"="*50}")
                for line in differences:

                    print(f"=in line[{line[0]}]:")
                    print(f'    we got : "{line[2]}"')
                    print(f'    you got: "{line[1]}"')

                print(f"{"="*50}{Style.RESET_ALL}")


    print(f"{Back.BLUE}{Fore.YELLOW}CORRECT: {counter}/{len(testcases)} = {Back.YELLOW}{Fore.BLACK}{(float(counter)/len(testcases)):.2f}%{Style.RESET_ALL}")


