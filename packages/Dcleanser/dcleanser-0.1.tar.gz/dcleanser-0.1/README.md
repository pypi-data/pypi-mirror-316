Data Cleansing Tool
This project provides a Python script for cleansing data in various file formats (CSV, Excel, JSON, XML). It offers a variety of operations to clean and process your data, including removing null values, handling duplicates, formatting column names, and transforming date columns. Users can choose cleansing operations interactively through a command-line interface.

Features
File Format Support: CSV, Excel (.xls, .xlsx), JSON, XML,
if you chose any operation,then want to getback to origianl data option also included.
Operations:
Remove rows/columns with null values.
Replace null values with a custom value.
Remove duplicate rows and columns.
Convert column names to lowercase and remove whitespaces.
Split date columns into day, month, and year.
Convert categorical columns to One-Hot Encoding.
And many more customizable data cleansing options....
Installation
Clone the repository or download the files to your local machine.

Dependencies: Ensure that you have Python 3.x. You can install the necessary dependencies using pip:

bash
Copy code
pip install pandas
Usage
Prepare your data: Make sure you have a data file in one of the supported formats (CSV, Excel, JSON, or XML).

Run the script: In the terminal or command prompt, navigate to the directory where the script is located and run it:

bash
Copy code
python autocleaner.py or python3 autocleaner.py
Enter file path: You will be prompted to enter the file path of the dataset you want to clean.

Choose cleansing operations: The script will display a menu of available operations. Enter the numbers of the operations you want to apply (separate multiple choices with commas). Some of the available operations include:

Remove rows/columns with null values.
Replace null values with a custom value.
Remove duplicate rows and columns.
Convert column names to lowercase and remove whitespaces.
Split date columns into day, month, and year.
Convert categorical columns to One-Hot Encoding.
Remove rows with null values.
Replace null values with a specified value.
Convert column names to lowercase.
Convert a date column to 'day', 'month', and 'year'.
Exit or revert to original: Type 'backtodata' to revert to the original data or 'exit' to stop the program.

Output: After performing the selected operations, the final cleaned DataFrame will be displayed.

Example
Here’s a simple usage example:

bash
Copy code
Enter your file path: data.csv
Choose cleansing operations (multiple choices allowed):
 Remove rows with null values
 Remove columns with null values
 Replace null values with a specified value
 Remove duplicate rows
 Convert column names to lowercase
...
Enter the numbers of the operations you'd like to perform, separated by commas: 1,4,5
Final DataFrame:
  Column1  Column2
0       1       10
1       2       20
Notes
Ensure the file path you provide is correct and accessible.
The script will display statistics before and after cleansing to help you track the changes made to your dataset.
You can perform multiple cleansing operations on the same dataset in a single run.
License
This project is licensed under the MIT License - see the LICENSE file for details.

