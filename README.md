## Group 7 - Apriori

This code is set up to take in a .csv file with the specified format:

Member_number,Date,itemDescription

You can change the csv file name you are inputting by editing line 3.

To run code on VS Code, select the play button at the top and select run python file.

To run code on a terminal, type "python main.py" after navigating to the project directory.

Using pandas library, latest version.

# To edit the parameters:

- Specify itemset length by adjusting the min and max values in line 129 and 131

- Specify minimum support and confidence, edit lines 127 and 131

I found a good number of narrowed down itemsets by using the values of 0.0008 confidence and support for itemsets of length 3 and 0.003 for itemsets of length 2.

https://youtu.be/JykRRu4aa5M

