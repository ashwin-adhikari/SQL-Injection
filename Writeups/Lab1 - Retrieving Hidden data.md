
This lab contains a SQL injection vulnerability in the product category filter.
When the user selects a category, the application carries out a SQL query like the following:
```SELECT * FROM products WHERE category = 'Gifts' AND released = 1 ```
<br>

**Exploit:**<br>
- After clicking on any category put ```'--``` to check for vulnerability.
Which results in ```SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1```
> ```--``` is a comment indicator in SQL. This means that the rest of the query is interpreted as a comment, effectively removing it. In this example, this means the query no longer includes AND released = 1
- With boolean condition ``` ' or 1=1--``` check for application response.
Which results in: ```SELECT * FROM products WHERE category = 'Gifts' OR 1=1--' AND released = 1```
![alt text](/images/lab1truecondition.png)
> The modified query returns all items where either the category is Gifts, or 1 is equal to 1. As 1=1 is always true, the query returns all items.

- Similarly checking for ```' or 1=2--``` which is a false condition gives us only released products.
![alt text](/images/lab1falsecondition.png)

