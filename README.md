## API 문서

### 인증

#### basic Auth

- HTTP의 basic authentication 을 이용한다.
-  header의 `Authorization` 키에 `Basic <value>` 값을 넣어 준다

> value : **`username:password`** 문자열을 Base64로 인코딩한 값



#### Token Auth

Token을 이용한 authentication 

[공식문서](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication) 참조

- header의 `Authorization` 키에 `Token <value>` 값을 넣어 준다

> value : 발급받은 Token의 키 값
>
> 토큰 발급 방법 : AuthTokenAPI



### posts

#### post list

- URL : 