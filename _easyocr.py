import easyocr
reader = easyocr.Reader(['en', 'hi']) # this needs to run only once to load the model into memory
result = reader.readtext('./dump/dummy_page_01.jpg')
for line in result:
    print(result)