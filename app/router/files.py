import os,shutil
from fastapi import APIRouter,HTTPException,Depends,status,UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from ..Database import database_engine
from ..Oauth2 import get_current_user
from ..Database import db_model
from ..Database.DatabaseQuery import files_query
from ..pydantic_model import Files,ResponseFiles,ShareFiles,ResponseShareFiles


upload_path = os.getcwd() + '/app/uploads'


router = APIRouter(
    tags=['Files']
)




@router.post('/file_upload')
async def uploadFile(file:UploadFile,db: Session = Depends(database_engine.get_db),
current_user = Depends(get_current_user)):
    # Copy The Upload File In Bnary Mode Teh Server TO Store The Close The File
    try:

        with open(os.path.join(upload_path,file.filename),'wb') as newFile:
            shutil.copyfileobj(file.file,newFile,length=1024*1024)

    except Exception:
        return {'message:' 'Failed To Upload File'}
    
    finally:
    
        await file.close()
    # Then  Only Store The File Info to The DB
    return files_query.uploadfile(file_name=file.filename,
    file_path=os.path.join(upload_path,file.filename),db=db,current_user=current_user)



@router.post('/sharefile',status_code=status.HTTP_201_CREATED)
async def shareFiles(file_info:ShareFiles, db: Session = Depends(database_engine.get_db),
                     current_user = Depends(get_current_user)):
    # checks is the owner is shareing the file or someone else
    if not files_query.isFileOwner(file_name=file_info.file_name,current_user=current_user,db=db):

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Not A File Owner")
    
    # store info about the shared File
    shared_file = files_query.sharefile(file_info,db,current_user)

    return shared_file



@router.get('/getfiles',status_code=status.HTTP_202_ACCEPTED,response_model=List[ResponseFiles])
async def get_owner_files(db: Session =Depends(database_engine.get_db),
    current_user=Depends(get_current_user)):
    # get All the Files Of The Logged In user Not The Shared The One The User Own
    try:
        files = files_query.get_all_files_of_owner(user_id=current_user.id,db=db)
    
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail='Database Error')
    
    return files


@router.get('/getSharedFiles', status_code=status.HTTP_200_OK ,response_model=List[ResponseFiles])

async def getsharedFiles(db: Session = Depends(database_engine.get_db),
    current_user = Depends(get_current_user)):

    # get All the Shared Files Of The Loged In User Which Has Been Shared To Him
    files = files_query.get_shared_files(db, current_user)
   
    return files    

@router.get('/download/{file_id}',status_code=status.HTTP_200_OK, response_class=FileResponse)

async def downloadFile(file_id:int, db: Session = Depends(database_engine.get_db),
        current_user = Depends(get_current_user)):
    
    # checks if The File Exist or Not
    if not files_query.hasFile(file_id=file_id,db=db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='File Not Found')
    
    file = files_query.getFileInfo(file_id=file_id, db=db)

    # user has acces too downlaod the file or not
    if  files_query.isFileOwner(file.file_name,db=db,current_user=current_user) or files_query.hasShared(file_id=file_id,db=db,current_user=current_user):
        print("owner :", files_query.isFileOwner(file.file_name,db=db,current_user=current_user))
        print("share :", files_query.hasShared(file_id=file_id,db=db,current_user=current_user))
        filepath = files_query.get_file_path(file_id=file_id, db=db)
        return filepath # As in Path Parameter response_class is passed as Fileresponse 
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Access Denied")


        

