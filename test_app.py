

from sample_app import app



def test_ejemplo_app():
   client = app.test_client()
   response = client.get("/")
   if response.status_code != 200:
    raise AssertionError(f"Error: Se esperaba 200, pero se recibió {response.status_code}")
   
    

    
    