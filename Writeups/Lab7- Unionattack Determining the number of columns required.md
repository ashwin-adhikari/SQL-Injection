**<h2>Background to UNION attack:</h2>**

The **_UNION_** keyword enables you to execute one or more additional **_SELECT_** queries and append the results to the original query. For example:

``SELECT a, b FROM table1 UNION SELECT c, d FROM table2``

**<h4>For a UNION query to work, two key requirements must be met:</h4>**

- ``The individual queries must return the same number of columns.`` For example, if the first query returns three columns (like "name", "age", "city"), the second query must also return three columns.
- ``The data types in each column must be compatible between the individual queries.``  For instance, if the first column in one query is a list of names (text), the first column in the second query must also be text (or something similar). You can't mix a column of names (text) with a column of numbers because the database wouldn't know how to handle the differences.

**<h4>To carry out a SQL injection UNION attack, make sure that your attack meets these two requirements. This normally involves finding out:</h4>**

- How many columns are being returned from the original query.
- Which columns returned from the original query are of a suitable data type to hold the results from the injected query.

<h2>Determining the number of columns required</h2>

We are already familiar with ``' order by `` query, which is used to determine the number of columns.<br>
The second method involves submitting a series of UNION SELECT payloads specifying a different number of null values:
>' UNION SELECT NULL-- <br>
' UNION SELECT NULL,NULL--<br>
' UNION SELECT NULL,NULL,NULL--

<h2>Goal:</h2>
Determine the number of columns returned by the query by performing a SQL injection UNION attack that returns an additional row containing null values.

<h2>Solution:</h2>

- Check the number of columns by using ``' order by `` attack which results total 3 columns present.
- Now to add the additional row we must find the data type of the columns we got which can be done by using ``' union select NULL,NULL,NULL--``
- We replace the **NUll** with text or number to find the type of data type present. If the data type in the column matches that of our query additional row will be added.
![alt text](/images/lab7additionalrow.png)
