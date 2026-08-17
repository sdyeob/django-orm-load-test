# django batch size에 따른 db 적재 속도 테스트

### 테스트 설명
* django의 ORM을 이용하여 database에 데이터를 적재할 때, batch size(n)에 따른 속도 차이 검증
* Default Database : sqlite3
* single datasize : 184B
* bulk datasize : 약 17MB

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

3. n = 250
- 소요 시간 : 1.56초

4. n = 300
- 소요 시간 : 1.65초

5. n = 400
- 소요 시간 : 1.56초

6. n = 700
- 소요 시간 : 1.80초

7. n = 1,000
- 소요 시간 : 1.81초

8. n = 10,000
- 소요 시간 : 1.90초

9. n = 100,000
- 소요 시간 : 2.32초

### 성능 차이 이유
1. n = 1일 때 시간이 오래 걸리는 이유
	- 일반적으로 db는 `auto-commit` 옵션이 활성화 되어있다. 따라서, 1개의 데이터를 처리할 때 마다 `auto-commit`을 수행하고, 이로 인해 Disk I/O 오버헤드가 발생한다.
		- auto-commit모드에서는 BEGIN -> parsing/compile -> EXECUTION -> Commit -> DISK I/O의 흐름이 실행된다.
	- 이 때, 계속해서 parsing / compile을 하는 작업조차 큰 오버헤드가 될 수 있다.
2. n = 100,000일 때 가장 빠르지 않은 이유 (추론)
	- CPU의 L1, L2, L3 캐시의 일반적인 크기 및 지연시간은 다음과 같다.
		- L1 : 8 ~ 32 KB, 0.5ns ~ 2.5ns 
		- L2: 256KB ~ 8MB, 3.5ns ~ 7ns
		- L3: 10MB ~ 64MB, 20ns ~ 26ns
	- django는 Insert 시 batch_size = 100,000이라면 전달받은 전체 데이터에 대한 검증을 수행한다고 한다.
		그렇다면, 100,000개의 데이터(약 17MB)에 대해 검증을 수행하게 되는데, 검증을 수행하게 되면 적어도 처음일은 데이터들은 L3캐시까지 데이터들이 밀려난다.
	- 이후, 검증이 끝난 데이터들에 대해서 _insert를 수행할 때 앞의 데이터들부터 _insert를 수행하게 되는데 계속해서 Cache miss가 발생하고 이를 해결하는 오버헤드가 발생할 수 밖에 없다.
	
### Future Work
1. Default DB를 sqlite3가 아닌 다른 database(mysql, mongodb)로 변경했을 때의 속도 차이 테스트

