## adder-web

### 必要な環境設定  
#### KeyCloakの接続に必要な設定  
- `KEYCLOAK_BASE_URL`  
- `KEYCLOAK_REALM_NAME`  
- `KEYCLOAK_CLIENT_ID`  
- `KEYCLOAK_CLIENT_SECRET`

### 他の環境設定  
#### ウェブサービス起動のUrl 
 - `APP_BASE_URL`

### Dockerを使ってプロジェクト実行
- 1.windows hosts設定追加
    path:`C:\Windows\System32\drivers\etc\hosts`

  ```
  172.19.245.xx        keycloak.zgc.com
  172.19.245.xx        adder.zgc.com 
  ```
  （上記のIPアドレスは、WSLでCMDコマンド「ifconfig」を実行し、その後、eth0の下に表示されるinetのIPアドレスを参照して取得します。）

### keyclock設定
- 【keyclock設定.xlsx】を参照してください。


### Dockerイメージ作成
```bash
APP_VER=v1.0.x && APP_NAME=adder-web && echo ${APP_NAME}:${APP_VER}
docker build --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy -f ./WebApp.with.proxy.Dockerfile -t ${REGISTRY}/${APP_NAME}:${APP_VER} ./
```

### docker-compose.ymlファイルの例
```yaml
services:
  adder-web-service:
      image: adder-web:v1.0.x
      container_name: adder-web-service
      environment:
        TZ: "Asia/Tokyo"
        KEYCLOAK_BASE_URL: http://keycloak.com:xxxx
        SERVER_BASE_URL: http://adder.com:xxxx
        KEYCLOAK_REALM_NAME: xxx
        KEYCLOAK_CLIENT_ID: xxx
        KEYCLOAK_CLIENT_SECRET: xxx
      ports:
        - xxx:8000
      extra_hosts:
      - keycloak.zgc.com: 172.19.245.xx
      - adder.zgc.com: 172.19.245.xx
```


### ローカル実行 
- 1.環境変数設定 
- 2.依頼をインストール　＆　実行  
    `start.cmd`