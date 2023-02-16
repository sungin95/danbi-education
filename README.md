## 개요 

#### 윙크 서비스 내에 Routine 기능을 추가하고자 합니다. 

> Routine 기능이란, 매 주마다 정해진 일정에 자신이 해야할 일을 등록하고, 해당 수행여부에 대한 내용을 기록하여 관리할 수 있도록 도와주는 기능입니다. 
>
> Routine 기능에서는 다음과 같은 기능을 제공하고자 합니다. 

- 유저의 로그인/로그아웃 기능 
- 매 주별 해야할 일의 등록 / 수정 / 삭제 / 조회 기능 
- 일정이 지난 후 진행한 할 일들에 대한 해결여부 기록 
  - 각 할일에 대한 결과는 독립된 결과로 기록되어야 함 
  - 예시)월/수/금 할일로 등록했을 때, 특정 날짜 데이터를 조회하면 조회한 날짜에 대한 수행결과만 모두 조회가 되도록 구성

## 기간

2월 9일 목 ~ 2월 16일 목



## 요구사항 

1. 유저의 로그인은 email로 진행합니다. 
2. 유저의 비밀번호는 8글자 이상이며 특수문자, 숫자를 포함해야 합니다. 
3. 유저 관련 동작은 django에서 제공하는 기본 기능을 이용해서 구현합니다. 
4. 테이블은 아래의 Schema를 따라야 합니다. 각 필드별 타입은 알아서 정의해주시면 됩니다. 
   1. 서버 구성은 자유롭게 하시면 됩니다.

## 제약사항 

1. Python, Django, DRF를 이용해 구현해 주세요 
2. 유저 검증은 Session 또는 jwt를 이용해 주세요. 
3. Database의 사용은 자유롭게 하시면 됩니다. 
4. Restful API 구현은 자유롭게 하시면 됩니다. 
5. 명시된 예시 외에 필요하다고 생각되는 API는 자유롭게 구현해 주세요. 
6. 테스트 코드를 꼭 작성해 주세요.

## 평가항목 

- 프로젝트의 구성을 적절히 하였는가? 
- 프로젝트 소스 코드의 구성이 가독성 있게 구성되어 있는가? 
- 테스트 코드는 적절하게 구현되어 있는가? 
- 요구사항에 대한 판단이 적절하게 이루어져 있는가?



## 참고 자료

DRF

- [처음에 따라한 영상](https://www.youtube.com/watch?v=ywJWbAF6txQ)
  - drf를 제대로 몰라서 처음에 영상을 보면서 따라 만듬.

JWT토큰을 활용한 로그인 구현

- 처음에는 라이브러리를 활용하여 만듬. 
  - https://han-py.tistory.com/214
  - https://minwoo.kim/posts/create-register-and-jwt-login-api-using-django-rest-framework/
- 라이브러리 사용 안하고 만들기 
  - https://axce.tistory.com/108
    - 덕분에 라이브러리 탈출 가능

소프트 딜리트

- is_deleted가 뭐지 하고 찾다가 알아냄. 
- 데이터를 실제로 삭제를 하지 않고 is_deleted를 True, False로 값을 줘서 False일때만 찾을 수 있도록 만들어줌.
- https://dev.to/bikramjeetsingh/soft-deletes-in-django-a9j

테스트 코드

- https://www.youtube.com/watch?v=4mm0mGMBQc8
  - 유일한 django testcase 설명해 주는 한국어 영상
  - [영상에서 나오는 사이트](https://docs.djangoproject.com/en/4.1/intro/tutorial05/)
- [JWT토큰을 headers에 넣기](https://vixxcode.tistory.com/126)

postman

- [포스트맨 따라하기 블로그](https://inpa.tistory.com/entry/POSTMAN-%F0%9F%92%BD-%ED%8F%AC%EC%8A%A4%ED%8A%B8%EB%A7%A8-%EC%82%AC%EC%9A%A9%EB%B2%95-API-%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%9E%90%EB%8F%99%ED%99%94-%EA%B3%A0%EA%B8%89-%ED%99%9C%EC%9A%A9%EA%B9%8C%EC%A7%80)

