import axios from 'axios';
import https from 'https';



let endpoint = localStorage.getItem('Endpoint');
let key = localStorage.getItem('EndpointKey');
let assistantInstructions = localStorage.getItem('assistantInstructions');
  
const instance = axios.create();


export default {  

  
  async getThread() {
    
    try {
        const response = await instance.post(endpoint+"/thread", {},
        {
          headers: {
            access_token: key,
            'Content-Type': 'application/json',
          }
        });
        const data = response.data.thread_id;
        console.log(data);
        return data.replace(/"/g, ''); 
    
    } 
    catch (error) {
        console.error('Failed to fetch thread:', error);
    }
  },

  async postMessage(message, thread_id) {
    console.log("key: " + key);
    console.log("endpoint: " + endpoint);
    console.log("thread: " + message);
    console.log("message: " + endpoint);
    
    try {
      const response = await instance.post(endpoint+"/message",
      {
          message:message,
          thread_id: thread_id,
        },
        {
          headers: {
            access_token: key,
            'Content-Type': 'application/json',
          },
        }
      );
        const messageText = response.data.message;
        return messageText;
    } catch (error) {
        console.error('Failed to post message:', error);
    }
  },

  
  
  

  async uploadFile(file) {
    const response = await instance.post(endpoint+"/upload",
    {
      file: file
    },
    {
      headers: {
        access_token: key,
        'Content-Type': 'application/json',
      }
    });
    return response;
  },
};
