from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def healthcheck():
    
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"pong": True}