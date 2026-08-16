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

3. n = 240
- 소요 시간 : 1.70초

4. n = 1,000
- 소요 시간 : 1.91초

5. n = 10,000
- 소요 시간 : 2.05초

6. n = 100,000
- 소요 시간 : 2.37초

### 성능 차이 이유
1. n = 1일 때 시간이 오래 걸리는 이유
	- 일반적으로 db는 `auto-commit` 옵션이 활성화 되어있다. 따라서, 1개의 데이터를 처리할 때 마다 `auto-commit`을 수행하고, 이로 인해 Disk I/O 오버헤드가 발생한다.
		- auto-commit이란 하나의 작업을 BEGIN -> parsing/compile -> EXECUTION -> Commit -> DISK I/O의 실행 흐름을 의미한다.
	- 이 때, 계속해서 parsing / compile을 하는 작업조차 큰 오버헤드가 될 수 있다.
2. n = 100,000일 때 가장 빠르지 않은 이유
	1. python이 사용하는 메모리 용량의 급증
		- 일반적으로 Python의 모든 객체는 Heap메모리에 할당된다. 우리가 ORM으로 생성할 100,000개의 데이터에 대한 INSERT 쿼리 또한 Heap 메모리에 할당된다. 그러나,
			100,000개 데이터에 대한 INSERT 쿼리문은 적어도 10MB단위의 텍스트 데이터이다. 이런 큰 Heap메모리 공간을 할당받기 위해서는 OS에게 System call을 통해
			메모리 공간을 요청해야하기 때문에 Context switching오버헤드가 발생하고, 이에 더해 할당된 Heap 메모리 공간을 모두 0으로 채워버리는 동작까지 수행하며 오버헤드가 커지게 된다.
	2. binding parameter(`?`)수의 제한
		- 테스트에서 사용한 sqlite3의 경우 하나의 쿼리문에 들어갈 수 있는 `?`의 개수가 999개로 한정되어있다.
			- binding parameter란 예를 들어, `INSERT INTO Robot(robot_id, pos_x, pos_y, battery) VALUES (?, ?, ?, ?)`와 같은 쿼리에 `?`로 표시된 부분의 개수를 의미한다.
		- 따라서, 100,000개의 데이터를 하나의 쿼리로 만들지 못해서 100,000개의 데이터에 대한 `bulk_create()`를 요청해도 우리 데이터의 경우 대략 250개의 데이터를 집어넣는 쿼리가 최대한 많은 데이터를 한번에 다루는 쿼리이기 때문에, 250개씩의 데이터를 INSERT하는 쿼리를 400개를 생성해야 한다. 이 오버헤드가 꽤 큰 것 같다.
3. n = 250이 가장 빠른 이유
	- n = 100,000일 때 가장 빠르지 않은 이유에서 2번째 binding parameter의 수 제한을 확인한 뒤에, 이론적으로는 n=250에 가장 가까울 때 최고 속도를 낼 것 같아서 이 근처값으로 실험을 해봤는데 실제로 n=250근처일 때 가장 빨랐다.

### Feature Work
1. Default DB를 sqlite3가 아닌 다른 database(mysql, mongodb)로 변경했을 때의 속도 차이 테스트

