from collections import Counter
import re

from bs4 import BeautifulSoup
import requests


myurl = "http://phocks.org/stumble/creepy/"  # input("@> ")


soup = BeautifulSoup(requests.get(myurl).text, 'html.parser')
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.body.get_text()

# break into lines and remove leading and trailing space on each
# lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
# text = '\n'.join(chunk for chunk in chunks if chunk)
text = re.sub(r"[\[\]\(\)]", "", text)

print(text)
print(Counter(text.split()))
