import requests 
import json
import numpy as np
import cv2

# server running locally at port 8888
url = 'http://127.0.0.1:8888/event'

# text data to be sent
data = {
    'input-text-0': 'hello',
    'input-text-1': 'world',
    'input-text-2': 'Is this a sample question?',
    'input-text-4': 'This will not be read'
}
# list of images to be sent
image_list = [
    'example1.png',
    'example2.png'
]

def test_getTextInput():
    data_copy = data.copy()
    data_copy['test_number'] = 0
    r = requests.post(url=url, data=data_copy)
    assert(r.status_code == 200)
    assert(json.loads(r.content)['data'] == ['hello', 'world', 'Is this a sample question?'])

def test_getWrongTextInput():
    data_copy = data.copy()
    data_copy['test_number'] = 0
    data_copy['input-text-0'] = 'goodbye'
    r = requests.post(url=url, data=data_copy)
    assert(r.status_code == 500)

def test_getExtraTextInput():
    data_copy = data.copy()
    data_copy['test_number'] = 0
    data_copy['input-text-3'] = 'goodbye'
    r = requests.post(url=url, data=data_copy)
    assert(r.status_code == 500)

def test_getImageInput_filepath():
    # compile image data as byte strings
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data={'test_number': 1})    
    assert(r.status_code == 200)
    filepaths = json.loads(r.content)['data']
    assert(len(filepaths) == len(image_list))
    for i in range(len(filepaths)):
        assert(np.array_equal(cv2.imread(filepaths[i]), cv2.imread(image_list[i])))

def test_getImageInput_nparray():
    # compile image data as byte strings
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data={'test_number': 2})
    assert(r.status_code == 200)
    images = json.loads(r.content)['data']
    assert(len(images) == len(image_list))
    for i in range(len(images)):
        assert(np.array_equal(np.array(images[i], dtype=np.int16), cv2.imread(image_list[i])))

def test_getWrongImageInput():
    # compile image data as byte strings
    files = {}
    for i in range(len(image_list)):
        with open(image_list[len(image_list) - 1 - i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data={'test_number': 2})
    assert(r.status_code == 500)

def test_all():
    data_copy = data.copy()
    data_copy['test_number'] = 3
    files = {}
    for i in range(len(image_list)):
        with open(image_list[i], 'rb') as f:
            files['input-image-%d'%(i)] = f.read()
    r = requests.post(url=url, files=files, data=data_copy)
    assert(r.status_code == 200)
