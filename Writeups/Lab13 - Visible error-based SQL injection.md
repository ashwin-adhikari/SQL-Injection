**<h2>Background</h2>**
Misconfiguration of the database sometimes results in verbose error messages. These can provide information that may be useful to an attacker. For example following error message occurs after injecting a single quote into an id parameter.

``Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = '''. Expected char
``
This shows the full query that the application constructed using our input. We can see that in this case, we're injecting into a single-quoted string inside a WHERE statement. This makes it easier to construct a valid query containing a malicious payload. 

Occasionally, we may be able to induce the application to generate an **_error message that contains some of the data_** that is returned by the query.

We can use the ``CAST()`` function to achieve this. It enables you to convert one data type to another. For example, imagine a query containing the following statement:
``CAST((SELECT example_column FROM example_table) AS int)``

Attempting to convert one data (often string) to an incompatible data type, such as an int, may cause an error similar to the following:
``ERROR: invalid input syntax for type integer: "Example data"``

**<h2>Problem:</h2>**
The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned. 

The database contains a different table called users, with columns called username and password.

**<h2>Goal:</h2>**
Find a way to leak the password for the administrator user, then log in to their account.

**<h2>Solution:</h2>**
- Check if visible error message are shown incorrect syntax ``TrackingId = ....abc'`` 
![alt text](/images/lab13visibleerror.png)
- For correct syntax ie ``'--`` the errors are not shown.
- Use ``CAST()`` to obtain error messages for the syntax, using with logical AND,OR should work boolean value so, use logical operations such as =,!=,etc
- As we have the table name ie users and row in it ie username and password we can try to get visible errors ``TrackingId = ....abc' AND 1=cast(select username from users) as int``
We get the same initial error.
- Delete the tracking id to get space for query.
    - Visible error obtained : ``ERROR: more than one row returned by a subquery used as an expression``
- Limit the query to one row using ``limit  1``
    - Visible error obtained: ``ERROR: invalid input syntax for type integer: "administrator"``
- Repeat the same process for password row
    - Visible error obtained: ``ERROR: invalid input syntax for type integer: "xbadf489rlohfz6rqmge"``
- login using these credentials to solve lab
