import json
# from typing import Optional
from pydantic import BaseModel

class Voters(BaseModel):
    # id:Optional[int]=None
    username:str
    password:str

# with open('test.json','r')as f:
#     voters=json.load(f)['Voters']
# print(voters)    