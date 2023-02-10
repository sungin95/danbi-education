# 단비교육 백엔드 개발 과제 v1.5 

## 개요 

### 윙크 서비스 내에 Routine 기능을 추가하고자 합니다. 

>  Routine 기능이란, 매 주마다 정해진 일정에 자신이 해야할 일을 등록하고, 해당 수행여부에 대한 내용을 기록하여 관리할 수 있도록 도와주는 기 능입니다.

Routine 기능에서는 다음과 같은 기능을 제공하고자 합니다. 

- 유저의 로그인/로그아웃 기능 
- 매 주별 해야할 일의 등록 / 수정 / 삭제 / 조회 기능 
- 일정이 지난 후 진행한 할 일들에 대한 해결여부 기록 
  - 각 할일에 대한 결과는 독립된 결과로 기록되어야 함 
  - 예시)월/수/금 할일로 등록했을 때, 특정 날짜 데이터를 조회하면 조회한 날짜에 대한 수행결과만 모두 조회가 되도록 구성 



## 요구사항

1. 유저의 로그인은 email로 진행합니다. 
2. 유저의 비밀번호는 8글자 이상이며 특수문자, 숫자를 포함해야 합니다. 
3. 유저 관련 동작은 django에서 제공하는 기본 기능을 이용해서 구현합니다. 
4. 테이블은 아래의 Schema를 따라야 합니다. 
         a. 각 필드별 타입은 알아서 정의해주시면 됩니다. 
5. 서버 구성은 자유롭게 하시면 됩니다.



## 목차

- routine 
  - routine_id (Primary Key) 
  - account_id 
  - title 
  - category [MIRACLE(기상 관련), HOMEWORK(숙제 관련)] 
  - goal 
  - is_alarm 
  - is_deleted 
  - created_at 
  - modified_at 
- routine_result 
  - routine_result_id (Primary Key) 
  - routine_id 
  - result [NOT(안함), TRY(시도), DONE(완료)] 
  - is_deleted 
  - created_at 
  - modified_at 
- routine_day 
  - day 
  - routine_id 
  - created_at 
  - modified_at



요청과 응답은 아래 예시를 따라야 합니다. 

- Routine 생성 
  - Request





