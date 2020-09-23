###### PROBLEM TWO: SALES TAXES

Basic sales tax is applicable at a rate of 10% on all goods, except books, food, and medical products that are exempt. Import duty is an additional sales tax applicable on all imported goods at a rate of 5%, with no exemptions.

When I purchase items I receive a receipt which lists the name of all the items and their price (including tax), finishing with the total cost of the items, and the total amounts of sales taxes paid.  The rounding rules for sales tax are that for a tax rate of n%, a shelf price of p contains (np/100 rounded up to the nearest 0.05) amount of sales tax.

Write an application that prints out the receipt details for these shopping baskets.

==========

###### Explanation of design:

The program is split into 3 classes: Receipt, Item, Util.

Util is a class to store helper method targeted to be generic aside from the printing of the receipt.
Receipt is a class to drive the printing functionality.
Item is a class to make the computation of tax required for each item.

The flow of the program starts with reading the input file and putting them in a list. This list is then pass to the Receipt class which further parses individual line as item. For each item, an evaluation of the tax rate and whether or not it is exempted from a certain tax rate would be done in order to calculate the tax amount. 
All the subtotal and tax amount would be pass back to Receipt for printing of the receipt under a specific format.

Method is_exempted under Item is extracted to provide the ability to extend and upscale the program in accepting a wider range of inputs and to provide accurate calculation of the tax based on the categorization of the item name. Currently only a fixed set of keywords is used to determine whether or not basic tax is exempted. An option to extend the categorization of item name could be to leverage on external APIs in categorizing name of the item and check if any of the categories matches with book, food and medical products.

==========

###### Assumption:

To yield correct result, items under the category of book, food, medical products would require keyword added to the exemption list. Current supported items are listed in the EXEMPTION constant ({"book", "food", "chocolate", "medical", "pills"}).
For instance, "apple" would not be considered as food unless specified in EXEMPTION.

