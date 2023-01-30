import sqlite3

conn = sqlite3.connect('Danışanlar2.db')

c = conn.cursor()

c.execute("""CREATE TABLE Danışanlar (
    ID integer,
    İsim text,
    Soyisim text,
    Hastalıklar text,
    Telefon Numarası text,
    Yaş integer,
    Ekstra Bilgi text

)""")

# for i in range (5):
#     id = i + 5
#     isim = input()
#     soyisim = input()
#     hastalık = input()
    
#     c.execute("INSERT INTO Danışanlar VALUES (?, ?, ?, ?)",(id,isim,soyisim,hastalık))

conn.commit()
conn.close()