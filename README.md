# django batch size에 따른 db 적재 속도 테스트

### 테스트 설명
* django의 ORM을 이용하여 database에 데이터를 적재할 때, bulk size(n)에 따른 속도 차이 검증
* Default Database : sqlite3
* single datasize : 184Byte

### 테스트 환경
- PC : Macbook M1 Pro
- CPU : Apple M1 Pro
- OS Version : Sonoma 14.6.1
- RAM : 16GB

### 테스트 목록
* n = 한번에 db에 적재하는 데이터 사이즈
* 테스트 횟수 : 3회
* 소요 시간 : 3번의 테스트의 평균 소요 시간

1. n = 1
- 소요 시간 : 43.42초

2. n = 100
- 소요 시간 : 1.87초

3. n = 1,000
- 소요 시간 : 1.91초

4. n = 10,000
- 소요 시간 : 2.05초

5. n = 100,000
- 소요 시간 : 2.37초

### 성능 차이 이유
- 메모리 - Disk의 속도 차이 이슈
- 

### Feature Work
1. Default DB를 sqlite3가 아닌 다른 database(mysql, mongodb)로 변경했을 때의 속도 차이 테스트

