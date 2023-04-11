from fastapi import FastAPI, HTTPException
from datetime import *
from pydantic import BaseModel
import random
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()

class InvoiceItem(BaseModel):
    nit: str 
    direction: str 
    date: date
    currency: str
    type: str
    products: dict = {}

class InvoiceDocs(BaseModel):
    DTE: str
    Autorization: str
    datetime: datetime
    itms: int

def _randN(N):
	min = pow(10, N-1)
	max = pow(10, N) - 1
	return str(random.randint(min, max))

# fastapi automatically transform the dictionary to a json
@app.post("/")
async def root(item: InvoiceItem):
    
    if item.nit and item.direction and item.date and item.currency and item.type and item.products:
        if len(item.nit) == 8:
            t1 = _randN(20)
            t2 = _randN(16)
            t3 = datetime.today()
            t4 = len(item.products)
            print(str(t3))
            return_data = InvoiceDocs(DTE=t1, Autorization=t2, datetime=t3, itms=t4)
            json_compatible_item_data = jsonable_encoder(return_data)
            return JSONResponse(content=json_compatible_item_data)
        else:
             raise HTTPException(status_code=404, detail="Invalid NIT")
    else:
        raise HTTPException(status_code=404, detail="Mising Data")
    
if __name__ == "__main__":
     uvicorn.run(app,host="0.0.0.0", port=8000)