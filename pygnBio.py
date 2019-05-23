import pygn.pygn as pygn

client_id = '481727732-088F497C5E2FC432B7297FB9E4EBBB3A'

user_id = pygn.register(client_id)

data = pygn.search(client_id,user_id,'Kings Of Convenience','Riot On An Empty Street')
print(data)
print(data['artist_bio_url'])