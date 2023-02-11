ConnectionRefusedError: [WinError 10061] 대상 컴퓨터에서 연결을 거부했으므로 연결하지 못했습니다



\# error해결

settings.py 에 다음을 추가 

`EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"`



postman 에서 자구 이렇게 떠서 찾아 봤더니

`"detail": "Unsupported media type \"text/plain\" in request."` 

입력 형식을 text에서 JSON으로 바꾸니까 해결
