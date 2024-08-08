import uvicorn

if __name__ == '__main__':
    uvicorn.run("rest_api:app",
                host="0.0.0.0",
                port=8432,
                reload=True#,
                #ssl_keyfile="./key.pem", 
                #ssl_certfile="./cert.pem"
                )