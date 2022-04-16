from igdb.wrapper import IGDBWrapper
wrapper = IGDBWrapper("YOUR_CLIENT_ID", "YOUR_APP_ACCESS_TOKEN")

# JSON API request
byte_array = wrapper.api_request(
            'games',
            'fields id, name, summary; offset 0; where platforms=*;'
          )
# parse into JSON however you like...

# Protobuf API request
from igdb.igdbapi_pb2 import GameResult
byte_array = wrapper.api_request(
            'games.pb', # Note the '.pb' suffix at the endpoint
            'fields id, name, summary; offset 0; where platforms=*;'
          )
games_message = GameResult()
games_message.ParseFromString(byte_array) # Fills the protobuf message object with the response
