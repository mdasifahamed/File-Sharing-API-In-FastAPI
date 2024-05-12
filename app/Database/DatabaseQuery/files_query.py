from sqlalchemy.orm import Session # Session Class that will handle db sessions
from ...pydantic_model import Files,ShareFiles,ReturnUser # custom for handling data from request  
from ...Oauth2 import get_current_user # a function that returns current_user based On JWT token decoding.More Details Can Be Found On Oauth2 module
from .. import db_model # Database models(Table) we have created to interact using SQLAlchemy (ORM Implementation)





def uploadfile(file_name:str,file_path,db:Session, current_user:ReturnUser):
    """Summary or Description of the Function

    Parameters:
    file_name (str): Name of the file  
    file_path (str): Path of the file where it is has been stored on the server.
    db(Session)    : It is an instance of the database session which has will be ijected from the API path.
    current_user   : It is an instance of the ReturnUser class.
    Returns:
    dict_object: It return a dict typ object after successfully Store it to the db

    """
   
    file = Files(file_name=file_name,file_path=file_path,owner_id=current_user.id) # Creating insatnce of The File Class
    file_to_store =  db_model.Files(**file.model_dump()) # file_info that is going to stored on the db 
    # above line `'**file.model_dump()` is defines that file object object i converting dictinary 
    # and '**' is for unpacking The dictionary beacause Files() From db_model it expects That.
    db.add(file_to_store) # Adding the Object to teh db
    db.commit() # Commiting Update
    db.refresh(file_to_store)
    return file_to_store


def sharefile(shareFile:ShareFiles,db:Session, current_user:ReturnUser):
    """Summary or Description of the Function

    Parameters:
    shareFile (ShareFiles): Inatance Of ShareFiles pyndanctic Model Which will Come from the request data
    db(Session)    : It is an instance of the database session which has will be ijected from the API path.
    current_user   : It is an instance of the ReturnUser class.
    Returns:
    dict_object: It return a dict typ object after successfully Store it to the db Or retrun message on any Failure

    """
    #get the file from the database
    file_on_db =  db.query(db_model.Files).filter(db_model.Files.file_name == shareFile.file_name).first()
    
    if not file_on_db:

        return {'message':"No file"}
    
    # check if the file has been already shred with person or not
    if not isAlreadyShared(file_on_db.id,db):

        file_info = {} # Empty Dictionary for filling ot with the file info
        file_info.update({"file_id":file_on_db.id,"shared_to":shareFile.shared_to,"shared_by":current_user.email})
        file_to_Upload = db_model.SharedFiles(**file_info)
        db.add(file_to_Upload)
        db.commit()
        db.refresh(file_to_Upload)
        return file_to_Upload
    
    return {'message':"File Already Shared"}



def get_all_files_of_owner(user_id:int,db:Session):

    """Summary or Description of the Function

    Parameters:
    user_id (int)  : id of the user 
    db(Session)    : It is an instance of the database session which has will be ijected from the API path.
    Returns:
    List of dict_object: It return  list of dict type objects of files info 
    from the database for the associated user id
    """
    
    files =  db.query(db_model.Files.file_name,db_model.Files.id).filter(db_model.Files.owner_id == user_id).all()
    return files

def get_shared_files(db:Session, current_user:ReturnUser):
    
    """Summary or Description of the Function

    Parameters:
    user_id (int)  : id of the user 
    db(Session)    : It is an instance of the database session which  will be ijected from the API path.
    Returns:
    List of dict_object: It return  list of dict type object which contain the filles info
    that has been shared with the current logged in user.
    """
    
    files =  db.query(db_model.Files.file_name,db_model.Files.id).join(db_model.SharedFiles,
    db_model.Files.id == db_model.SharedFiles.file_id).filter(db_model.SharedFiles.shared_to==current_user.email).all()
    return files

def getFileInfo(file_id:int,db:Session):

        
    """Summary or Description of the Function

    Parameters:
    file_id (int)  : id of File
    db(Session)    : It is an instance of the database session which  will be ijected from the API path.
    
    Returns:
    dict_object    : It will return dict type object which contain information about a file  
    """
    
    file = db.query(db_model.Files).filter(db_model.Files.id == file_id).first()
    return file

def get_file_path(file_id:int,db:Session):

    """Summary or Description of the Function

    Parameters:
    file_id (int)  : id of File
    db(Session)    : It is an instance of the database session which  will be ijected from the API path.
    Returns:
    file_path(str) : storage path of the file

    """

    file_path =  db.query(db_model.Files.file_path).filter(db_model.Files.id == file_id).first()
    print(file_path[0])
    return file_path[0]

def isFileOwner(file_name:str, db:Session, current_user: ReturnUser):

    """Summary or Description of the Function

    Parameters:
    file_name (str)  : name of File
    db(Session)    : It is an instance of the database session which  will be ijected from the API path.
    current_user   : It is an instance of the ReturnUser class.
    Returns:
    bool : if the file is ownerd by the current user then return tru or return false

    """

    file = db.query(db_model.Files).filter(db_model.Files.file_name == file_name, db_model.Files.owner_id == current_user.id).first()

    if file:

        return True
    
    return False

def isAlreadyShared(file_id:str,db:Session):
    file = db.query(db_model.SharedFiles).filter(db_model.SharedFiles.file_id == file_id).first()

    if file:

        return True
    
    return False

def hasFile(file_id:int, db:Session):

    """Summary or Description of the Function

    Parameters:
    file_id (int)  : Id of the File
    db(Session)    : It is an instance of the database session which  will be ijected from the API path.
    Returns:
    bool : if the file is in the db then return true else rteurn false

    """

    file = db.query(db_model.Files).filter(db_model.Files.id == file_id).first()
    if file:
        return True
    return False

def hasShared(file_id:int, db:Session, current_user:ReturnUser):


    """Summary or Description of the Function

    Parameters:
    file_id (int)  : Id of the File
    db(Session)    : It is an instance of the database session which  will be ijected from the API path.
    current_user   : It is an instance of the ReturnUser class.
    Returns:
    bool : Chendks if the fiel has been shared with the current user or not .

    """
    
    file = db.query(db_model.SharedFiles).filter(db_model.SharedFiles.file_id == file_id,
        db_model.SharedFiles.shared_to == current_user.email).first()
    print(file)
    if file:
        return True
    
    return False
