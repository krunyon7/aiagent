from functions.get_files_info import get_files_info


def test_results(working_directory, directory):
    if directory == ".":
        return (
            "Result for current directory:\n" + 
            get_files_info(working_directory, directory)
            )
    else:
        return (
            f"Results for '{directory}' directory:\n" + 
        get_files_info(working_directory, directory)
        )

print(test_results("calculator", "."))
print(test_results("calculator", "pkg"))
print(test_results("calculator", "/bin"))
print(test_results("calculator", "../"))
        