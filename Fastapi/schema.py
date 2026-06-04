from pydantic import BaseModel,Field

from typing import Optional,Annotated,Literal


class empl(BaseModel):
    name:str
    age:int
    salary:float
    city:Annotated[str,Field(...,description="jaipur,delhi")]
    ##name:Annotated[str,Field(...,description="")]
    gender:Annotated[str,Literal["male","female"],Field(...,description="gender male or female")]
    
    
    
    
class emplcreate(empl):
    pass
    
    
    
class emplupdate(BaseModel):
    name:Optional[str]=None
    age:Annotated[Optional[int],Field(default=None,description="30,40 etc")]
    salary:Annotated[Optional[int],Field(default=None,description="20000,15000 like this")]
    city:Annotated[Optional[str],Field(default=None,description='jaipur ,delhi')]
   ## name=(Annotated[Optional(str),Field(default=None,description="harsh,ajay")])
    gender:Annotated[Optional[str],Literal["male","female"],Field(default=None,description="gender male or female")]



class chatRequest(BaseModel):
    question:str
    