def test_list_ownedfiles(user1_file_upload,user1_logged_in):
    """User1 Uploads A Files . User1 Should Be Able To Retrive His File Info
        '/getfiles' endpoint returns the a list of files owned by the currently loged in user
        'user1_file_upload' is a fixture it run when this test runs and adds a files
        to the server for the user 1
    """

    res = user1_logged_in.get('/getfiles')
    # '/getfiles' returns a list of dictinary each dictinary contains information about the file
    # as user1 uploaded 1 file the length of th list should be 1
    assert len(res.json()) == 1

def test_list_sharedFiles(user1_file_upload,user1_logged_in):
    """Another Endpoint For The Listing Files Is 
        '/getSharedFiles' which also returned a list of files that 
        been shared to a user.
        
        In Here No File Has Been Shared With The User1
    """

    res = user1_logged_in.get('/getSharedFiles')
    # '/getSharedFiles' returns a list of dictinary each dictinary contains information about the file
    # as no files has not been shared with the  user1  the list shloud be empty
    assert len(res.json()) == 0

# Share a file with the User3 and Test 

def test_share_a_file(user1_file_upload,user1_logged_in,test_user3):
    file_info = user1_file_upload
    res = user1_logged_in.post(f'/sharefile',json={'file_name':file_info['file_name'],
                                                   'shared_to':test_user3['email']})
    assert res.status_code == 201
   

def test_user3_has_sharedFile_but_dont_own_any(user3_logged_in):

    """ '/getfiles' returns list of the files of that is owned is by the current owner
        '/getSharedFiles' returns list of the files that has been shared to the current user
    """
    res_file_owns = user3_logged_in.get('/getfiles')
    res_file_shared = user3_logged_in.get('/getSharedFiles')

    assert len(res_file_owns.json()) == 0 # User3 Don;t Own Any Files
    assert len(res_file_shared.json()) == 1 # User3 Has One Shared File Which is Shared By the User 1
    
