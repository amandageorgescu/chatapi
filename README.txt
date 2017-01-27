Welcome to my simple chat API.

In order to chat, follow the steps below:

1. You must first register yourself as a user. You can do that with the following command, inserting your own name and email address:

curl -H "Content-type: application/json" -X POST https://protected-beyond-84593.herokuapp.com/users -d '{"name":"Amanda Georgescu","email":"georgescu.amanda@gmail.com"}'


2. Now, use the following command to see who else you can chat with:

curl -H "Content-type: application/json" -X GET https://protected-beyond-84593.herokuapp.com/users

This will list the names and email addresses of everyone who has registered to use the chat API, such as below:

Here are some people you can chat with:
Amanda Georgescu (georgescu.amanda@gmail.com)
Bob Smith (bobsmith@gmail.com)


3. Now, in order to chat with someone, use the below command, inserting your email address as "from", the email address of the person you want to chat with as "to", and the message you want to send as "message":

curl -H "Content-type: application/json" -X POST https://protected-beyond-84593.herokuapp.com/messages -d '{"from":"georgescu.amanda@gmail.com","to":"bobsmith@gmail.com","message":"Hey Bob"}'

You will see your own message printed out in the console such as below:

Amanda Georgescu: Hey Bob


4. Now, wait a few moments and use the below command to query for a reply, inserting the email address of the person you are chatting with as "from", and your email address as "to":

curl -H "Content-type: application/json" -X GET https://protected-beyond-84593.herokuapp.com/messages -d '{"from":"bobsmith@gmail.com","to":"georgescu.amanda@gmail.com"}'

If the person you are chatting with has replied already, you will see their message printed out as below:

Bob Smith: Hey Amanda

If they haven't replied yet, nothing will be printed.  You can always try the above command again after waiting a few more moments.  

5.  In order to keep chatting, just continue using the commands described in Steps 3 and 5.  Remember you can use the UP arrow to go back to recent commands, so you'll just need to update the message field if you want to send a new message, and the command for querying replies can be resused without changing.  

Enjoy!





 
