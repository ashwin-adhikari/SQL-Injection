This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

**Goal:** display the database version string. <br>

**Solution:**<br>
Using burpsuite for this; 
- Check number of columns using query: ``order by num--``. This produced an error since commenting using ``-`` is invalid for MySQL so we use ``' order by num#`` Which gives response.
- Increase number until we get **__Internal Server Error__**, which we get for ``order by 3#``.
- Now we check whats in the columns using union query, 
``'union select NULL, 'a'#`` gives response 
``' union select @@version,NULL#`` it produces required output.
![alt text](/images/lab4databaseversion.png)