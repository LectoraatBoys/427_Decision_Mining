import xml.etree.ElementTree as ET
import pandas as pd
import re

# xml
tree = ET.parse('df.xml')
root = tree.getroot()

breadcrums = ['.//wetgeving/wet-besluit/wettekst/hoofdstuk/paragraaf/artikel/lid/al']
elements = root.findall(breadcrums[0])
lst = []
for element in elements:
    # converteer hoofdletters naar kleine letters
    text = element.text.lower()
    lst.append(text)

# pandas en re
df = pd.DataFrame(lst, columns=['zinnen'])
stopsigns = r'[\n ,-.:\xa0«°»éë]+'
# wijs unieke id toe aan alle zinnen
df = df.reset_index()
# houdt bij welke ongewenste tekens gefilterd moeten worden.
df["woorden"] = df['zinnen'].apply(lambda x: re.findall(f'{stopsigns}|\w+', x))

df.to_csv("df.csv", index=False)
