# KairanBotPython
# Disclamer: This project is meant for personal use, and is hard to set up. The instructions below are incomplete. At some point later this year, I hope to make it more user-friendly. - Kairan 2020
<pre><code>1. pip install -r requirements.txt
2. git clone <a href="https://www.github.com/kairanaquazi/KairanbotPython.git">https://www.github.com/kairanaquazi/KairanbotPython.git</a> master
3. cd KairanBotPython
</pre></code>
<strong>Add your bot token into .env (TOKEN=[your token])</strong><br>
<strong>Edit the praw.ini file.
Add your Reddit's bot id, secret and name. If you don't want to do Reddit
tools, delete the Reddit command in socialandstuff.py</strong>
<strong>You must also install Redis and start the server. Add your password to options.json</strong><br>
<pre><code>
5. python bot.py
</pre></code>
You may also have to remove some of my guild specific code to make sure you don't get
errors.
<br>
Feel free to file issues (please don't email me unless it is an urgent issue, eg. Data leak or Redis or something)