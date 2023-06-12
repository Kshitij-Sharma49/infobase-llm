from flask import Flask, jsonify, request
from flask_cors import CORS
import re
import io
import json
import PyPDF2
import requests
from pdfminer.high_level import extract_text

app = Flask(__name__)
CORS(app)
# api = Api(app)


@app.route('/match_content/file1=<file1>&file2=<file2>', methods=['GET'])
def return_predictions(file1, file2):
    substring1 = "conclusion"
    
    link1 = f'https://gateway.lighthouse.storage/ipfs/{file1}'
    link2 = f'https://gateway.lighthouse.storage/ipfs/{file1}'
    
    textstr=''
    response = requests.get(link1)
    memory_file = io.BytesIO(response.content)
    # Extract text from the PDF
    textstr += (''.join(extract_text(memory_file)))  
    print(f'{file1}.pdf loaded successfully.')   
    
    # if os.path.isfile(f'{file1}.pdf'):
    #     # file exists, load it
    #      
    #     with open(f'{file1}.pdf', 'rb') as f:
    #         reader = PyPDF2.PdfReader(f)
    #         pages = [reader.pages[j].extract_text() for j in range(len(reader.pages))]
    #         textstr+=(' '.join(pages))
            
    # else:
    #     return jsonify({'error': f'{file1}.pdf does not exist'}), 404

    textstr = textstr.lower()

    index = textstr.find(substring1)
    result1 = textstr[index:index+600]
    ind = index+500

    while result1[-1] != '.':
        result1 += textstr[ind]
        ind=ind+1

    result1 = re.sub(r'\s+', ' ', result1)

    textstr=''
    response = requests.get(link2)
    memory_file = io.BytesIO(response.content)
    # Extract text from the PDF
    textstr += (''.join(extract_text(memory_file)))  
    print(f'{file2}.pdf loaded successfully.')   
    
    # if os.path.isfile(f'{file2}.pdf'):
    #     # file exists, load it
    #     print(f'{file2}.pdf loaded successfully.')    
    #     with open(f'{file2}.pdf', 'rb') as f:
    #         reader = PyPDF2.PdfReader(f)
    #         pages = [reader.pages[j].extract_text() for j in range(len(reader.pages))]
    #         textstr+=(' '.join(pages))
            
    # else:
    #     return jsonify({'error': f'{file2}.pdf does not exist'}), 404

    textstr = textstr.lower()

    index = textstr.find(substring1)
    result2 = textstr[index:index+600]
    ind = index+500

    while result2[-1] != '.':
        result2 += textstr[ind]
        ind=ind+1

    result2 = re.sub(r'\s+', ' ', result2)
    
    prompt = f'Please compare the meaning and similarity between the following two texts: Text 1 = ({result1}) and Text 2 = ({result2}). Determine if the texts exhibit significant similarities in their meaning, indicating potential plagiarism. Provide a similarity score or percentage to quantify the degree of similarity between the texts'
            
    url = "https://chatgpt-api8.p.rapidapi.com/"

    payload = [
        {
            "content": prompt,
            "role": "user"
        }
    ]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "52fb48fd7dmsh0b71e6ec5aa9659p195552jsn129611c1574a",
        "X-RapidAPI-Host": "chatgpt-api8.p.rapidapi.com"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        print(response_data)
        text_data = response_data['text']
        # return jsonify(response_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'message': text_data})


@app.route('/quick_assistant_with_context/file1=<file1>', methods=['GET'])
def llm_request_with_context(file1):
    substring1 = "abstract"
    
    link1 = f'https://gateway.lighthouse.storage/ipfs/{file1}'
    
    textstr=''
    response = requests.get(link1)
    memory_file = io.BytesIO(response.content)
    # Extract text from the PDF
    textstr += (''.join(extract_text(memory_file)))  
    print(f'{file1}.pdf loaded successfully.')   
    
    textstr = textstr.lower()

    index = textstr.find(substring1)
    result1 = textstr[index:index+600]
    ind = index+500

    while result1[-1] != '.':
        result1 += textstr[ind]
        ind=ind+1

    result1 = re.sub(r'\s+', ' ', result1)

    if request.json.get('rapidapi-key') is not None:
        rapidapi_key = request.json.get('rapidapi-key')

    else:
        rapidapi_key = "49fba4d0demshb6a2281b6adae66p13613ajsnedf2f167f7ac"    

    user_message = request.json.get('message')
    
    prompt = f'There is a research paper document with the given research abstract: ({result1}). With the context learned from the given abstract, can you please answer the following question: ({user_message})'
            
    url = "https://chatgpt-api8.p.rapidapi.com/"

    payload = [
        {
            "content": prompt,
            "role": "user"
        }
    ]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "chatgpt-api8.p.rapidapi.com"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        print(response_data)
        text_data = response_data['text']
        # return jsonify(response_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'message': text_data})


@app.route('/quick_assistant', methods=['POST'])
def llm_request():
    default_message = "" 
    user_message = request.json.get('message')
    
    prompt = default_message + user_message

    if request.json.get('rapidapi-key') is not None:
        rapidapi_key = request.json.get('rapidapi-key')

    else:
        rapidapi_key = "49fba4d0demshb6a2281b6adae66p13613ajsnedf2f167f7ac"    

            
    url = "https://chatgpt-api8.p.rapidapi.com/"

    payload = [
        {
            "content": prompt,
            "role": "user"
        }
    ]
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "chatgpt-api8.p.rapidapi.com"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        print(response_data)
        text_data = response_data['text']
        # return jsonify(response_data)
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'message': text_data})

# api.add_resource(TestClass, "/next")    

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')