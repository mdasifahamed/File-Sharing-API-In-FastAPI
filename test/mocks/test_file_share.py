import os
""" API Seeks Only File Owner Can Share Files
"""

def test_file_share(user1_file_upload,user1_logged_in,test_user1,test_user2):
    file_info = user1_file_upload
    res = user1_logged_in.post('/sharefile',json={'file_name':file_info['file_name'],'shared_to':test_user2['email']})
    assert res.status_code == 201
    assert res.json().get('shared_to') == test_user2['email']
    assert res.json().get('shared_by') == test_user1['email']
    assert res.json().get('file_id') == file_info['id'] # Assures That Correct File Si Shared

def test_file_share_fail(user2_logged_in,test_user3):
    """ We Can Pretend That We Know A File is Uploaded to API Server
        We The File Name Also But The One Who Is Trying To Share Is Not Owner
        of The File. It Should Fail To Share 
    """
    res = user2_logged_in.post('/sharefile',json={'file_name':'test.txt','shared_to':test_user3['email']})
    assert res.status_code == 400
    assert res.json().get('detail') == 'Not A File Owner'




    


   


