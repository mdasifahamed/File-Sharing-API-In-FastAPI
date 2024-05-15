
import pytest
def test_download(user1_file_upload, user1_logged_in):
    file_info = user1_file_upload
    file_id = file_info['id']

    res = user1_logged_in.get(f'/download/{file_id}')
    assert res.status_code == 200


def test_share_a_file(user1_file_upload,user1_logged_in,test_user2):
    file_info = user1_file_upload
    res = user1_logged_in.post(f'/sharefile',json={'file_name':file_info['file_name'],'shared_to':test_user2['email']})
    assert res.status_code == 201
    return res.json()
def test_shared_file_download(user2_logged_in):
    res = user2_logged_in.get('/getSharedFiles')
    files = res.json()
    file_id = files[0]['id']
    downlaod_res =user2_logged_in.get(f'/download/{file_id}')

    assert downlaod_res.status_code == 200


def test_downlaod_fail(user3_logged_in):
    """User3 Has No Shared File User3 Sholu Not Be Able To 
        Download A File Even If He Knows The File Info 
    """
    res = user3_logged_in.get('/download/1')
    assert res.status_code == 401
    assert res.json().get('detail') == "Access Denied"

