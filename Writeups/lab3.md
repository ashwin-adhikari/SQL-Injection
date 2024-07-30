This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

<br>
To exploit SQL injection vulnerabilities, it's often necessary to find information about the database. This includes:

- The type and version of the database software.
- The tables and columns that the database contains.
<table>
    <tr>
        <th>Database Type</th>
        <th>Query</th>
    </tr>
    <tr>
        <td>Microsoft, MySQL</td>
        <td>SELECT @@version</td>
    </tr>
    <tr>
        <td>Oracle</td>
        <td>SELECT * FROM v$version</td>
    </tr>
    <tr>
        <td>PostgreSQL</td>
        <td>SELECT version()</td>
    </tr>
</table>

For a ```UNION``` query to work, two key requirements must be met:

- The individual queries must return the same number of columns.
- The data types in each column must be compatible between the individual queries.

To carry out a SQL injection UNION attack, make sure that your attack meets these two requirements. This normally involves finding out:

- How many columns are being returned from the original query.
- Which columns returned from the original query are of a suitable data type to hold the results from the injected query.

In order to find number of columns we can use ```order by``` query.
- ```' ORDER BY 1--```
- ```' ORDER BY 2--```
- ```' ORDER BY 3--```, etc
<br>

Here we get error when we pass querry  ```' ORDER BY 3--``` so columns are only 2.
![alt text](/images/lab3columnserror.png)

Now we found columns. We need to find which column has data. <br>
On Oracle, every ```SELECT``` query must use the FROM keyword and specify a valid table. There is a built-in table on Oracle called ```dual``` which can be used for this purpose. So the injected queries on Oracle would need to look like:

```' UNION SELECT NULL FROM DUAL--```
We get data from both the columns.
![alt text](/images/lab3tabledataquery.png)

Now we send a query get version from table ```v$version```

- ```union select banner, null from v$version--```

![alt text](/images/lab3payload.png)

![alt text](/images/lab3output.png)
