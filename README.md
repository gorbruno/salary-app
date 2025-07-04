curl -X POST http://localhost:8000/auth/token  -d "username=aagorbunov&password=IFkWD13e88VNB"  -H "Content-Type: application/x-www-form-urlencoded"

curl http://localhost:8000/salary \
  -H "Authorization: Bearer <token>"