# Google Assistant를 이용한 스마트홈 시스템

## 맡은 역할
### Raspberry pi & Google Assistant API
1. **Raspberry pi에 Google Assistant API를 설치하여 AI스피커로 사용**
2. **아두이노와 블루투스 연결**
3. **아두이노로부터 신호를 받으면 trigger하여 각 신호에 맞는 기능 수행**
   - "pan off" 신호를 받게되면, pan을 정지시키고, 스피커를 통해 pan이 꺼졌음을 전달한다.
   - "pan on" 신호를 받게되면, pan을 작동시킨다. 스피커를 통해 pan이 켜졌음을 전달한다.
   - "GAS" 신호를 받게되면, 스피커를 통해 GAS가 감지되었음을 전달한다.
   - "PASSWORD" 신호를 받게되면, 스피커를 통해 password를 말하라고 전달하고, PASSWORD가 맞는지 확인한다.   
4. **스피커를 통해 명령이 들어온 경우, trigger하여 각 명령에 맞는 기능 수행**
   - "pan off" 명령을 들으면, pan을 정지시키고, 스피커를 통해 pan이 꺼졌음을 전달한다.
   - "humidity" 명령을 들으면, 아두이노로부터 받은 습도정보를 스피커를 통해 전달한다.
