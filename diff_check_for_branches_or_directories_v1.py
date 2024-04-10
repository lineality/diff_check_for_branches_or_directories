# python, diff_check_for_branches_or_directories
import os
import subprocess
from datetime import datetime
import filecmp

# Set the paths of the two directories

"""
# e.g.
dir1 = "/path/to/directory1"
dir2 = "/path/to/directory2"
"""

dir1 = "/path/to/directory1"
dir2 = "/path/to/directory2"

# Get the current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")


# Specify the directory path you want to check
report_groot_directory = "branch_diff_reports"

# Check if the directory exists
if not os.path.exists(report_groot_directory):
    # If the directory doesn't exist, create it
    os.makedirs(report_groot_directory)

# Open a file for writing the report
report_file = open(f"{report_groot_directory}/diff_report_{timestamp}.txt", "w")

################
# Branch checks
################
# Change to the directory of the first ltn repository
os.chdir(dir1)
# Run git status and capture the output
git_status_output = subprocess.run(["git", "status"], capture_output=True, text=True)
# Write the git status output to the report file
report_file.write("Git Status:\n")
report_file.write(git_status_output.stdout)
report_file.write("\n")

# Change to the directory of the 2nd ltn repository
os.chdir(dir2)
# Run git status and capture the output
git_status_output = subprocess.run(["git", "status"], capture_output=True, text=True)
# Write the git status output to the report file
report_file.write("Git Status:\n")
report_file.write(git_status_output.stdout)
report_file.write("\n")

#############
# diff check
#############
# Check if the directories have the same files and contents
dircmp = filecmp.dircmp(dir1, dir2)

# Check if the directories have the same files
if dircmp.left_only or dircmp.right_only:
    report_file.write("The directories have different sets of files.\n")
    if dircmp.left_only:
        report_file.write("Files present only in the first directory:\n")
        report_file.write("\n".join(dircmp.left_only))
        report_file.write("\n")
    if dircmp.right_only:
        report_file.write("Files present only in the second directory:\n")
        report_file.write("\n".join(dircmp.right_only))
        report_file.write("\n")

# Check if the files have different contents
diff_files = dircmp.diff_files
if diff_files:
    report_file.write("Files with different contents:\n")
    for file in diff_files:
        file_path1 = os.path.join(dir1, file)
        file_path2 = os.path.join(dir2, file)
        diff_output = subprocess.run(
            ["diff", file_path1, file_path2], capture_output=True, text=True
        )
        report_file.write(f"Differences for file: {file}\n")
        report_file.write(diff_output.stdout)
        report_file.write("\n")

# Close the report file
report_file.close()
