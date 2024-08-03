import axios from 'axios';

const serverUrl = 'http://localhost:3003/';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const getAll = (endpoint : string) => {
    const endpointUrl = serverUrl + endpoint
    return axios.get(endpointUrl)
       .then(res => res.data)
       .catch(err => {
            console.error('Error fetching data:', err.response? err.response.data : err.message);
            throw err; 
        });
};

const postMessage = (userMessage : Message) => {
    const endpointUrl : string = serverUrl + 'query';
    return axios.post(endpointUrl, userMessage)
                .then(res => res.data)
                .catch(err => {
                    console.log('Error adding object: ', err.response? err.response.data : err.message);
                    throw err;
                });
}

export default {
    getAll, postMessage
}