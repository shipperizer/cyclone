As promised, please find attached the code challenge.
I would like the code delivered to me as a Github repo that I can access, with a clear README file with install instructions.
I will also need the code up and running on a cloud platform.
You can complete it any time before tomorrow evening, just send me an email letting me know how many hours you took.

Octopus is keen to develop it’s technology as a series of cloud based, RESTful micro-services, with good security measures in
place to protect customer data.
The code-challenge thus includes the requirement to build some application-level encryption.

1) Create a Python web application using Tornado web server and host it as an App Engine project on Google.
2) The project should have a single page with a form where I can enter a URL to any website (e.g. Wikipedia or BBCNews)
3) The application should fetch that url and build a dictionary that contains the frequency of use of each word on that page.
4) Use this dictionary to display, on the client’s browser, a “word cloud” of the top 100 words, where the font size is largest
   for the words used most frequently, and gets progressively smaller for words used less often.
5) Each time a URL is fetched, it should save the top 100 words to a MySQL DB (Google Cloud SQL), with the following three columns:
    a) The primary key for the word is a salted hash of the word.
    b) The word itself is saved in a column that has asymmetrical encryption, and you are saving the encrypted version of the word.
    c) The total frequency count of the word.
Each time a new URL is fetched, you should INSERT or UPDATE the word rows.
6) An “admin” page, that will list all words entered into the DB, ordered by frequency of usage, visible in decrypted form.

Extra points for:
- Displaying just nouns and verbs (no prepositions or articles)
- In README, describe the best way to safely store and manage the keys.
- Elegant front end layout.
- Clean, well documented code.
