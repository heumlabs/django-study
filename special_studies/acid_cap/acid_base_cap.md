# ACID

## 1. ACID 란 무엇인가?

- **ACID**는 데이터베이스 트랜젝션이 안전하게 수행된다는 것을 보장하기 위한 성질을 가리키는 약어이다.

- ![](https://blog.sqlauthority.com/i/c/acid.png)

    - **Atomicity**(원자성)은 트랜잭션과 관련된 작업들이 부분적으로 실행되다가 중단되지 않는 것을 의미한다.
    - **Consistency**(일관성)은 트랜잭션이 데이터베이스를 반쯤 완료된 상태로 두지 않는다는 것을 의미한다.
    - **Isolation**(고립성)은 트랜잭션을 수행 시 다른 트랜잭션의 연산 작업이 끼어들지 못하도록 한다.
    - **Durability**(지속성)은 성공적으로 수행된 트랜잭션은 영원히 반영되어야 함을 의미한다. 즉 서버는 비정상 종료로부터 복구 되어야 한다.

- ACID는 DB의 모든 연산이 한번에 실행되는 것을 권장

- 트랜잭션 관리를 위한 두 가지 방법

    - 로깅방식 : DB에 데이터를 업데이트 하기 전에 로그에 모든 변경사항을 기록
    - 새도우 페이징 : 변경된 내용이 DB의 복사본에 저장되고, 트랜잭션이 commit 되면 활성화

- 데이터베이스는 ACID를 보장하기 위해 락(lock)을 사용하지만 네트워크 환경에서는 ACID 특성을 보장하는 것은 어렵다.


## 2. BASE

- 클라우드와 같은 분산 시스템은 ACID를 실현하는 것은 곤란하다. 일관성을 유지하려면 2단계 commit과 같은 heavy한 구조가 되어야 하기 때문에

- 그러면 분산 시스템에서 관리되는 데이터의 특성은 BASE로 표현할 수 있다. 

- BASE 란?
    - **B**asically **A**vailable
        - 분산시스템은 항상 가용성을 중시한다.
    - **S**oft-state
        - 떨어진 노드 간의 데이터 업데이트는 데이터가 노드에 도달한 시점에서 갱신
        - 저장소는 쓰기 일관성을 유지할 필요가 없으며, 항상 다른 복사본과 상호 일관성을 유지해야한다.
    - **E**ventually consistency
        - 데이터가 해당 노드에 도달할 때까지는 데이터에 일관성이 없는 상태이지만 도착한 후에는 무결성을 보장 할 수 있으므로 그 상황은 일시적이다.
        - 시스템상에서 일시적으로 Consistent하지 않은 상태가 되어도 일정 시간 후에는 Consistent 상태가 되는 것을 의미한다.

- ![ACID 와 BASE 비교](https://embian.files.wordpress.com/2013/06/acid-vs-base-2.png?w=525&h=138)

- ACID(산) vs BASE(염기)


## 3. CAP

- ![](https://embian.files.wordpress.com/2013/06/cap-circle.png?w=525&h=513)

- CAP 란?
    - `분산 시스템에서는 위 그림의 3개 속성을 모두 가지는 것이 불가능하다!` 이다.

- Consistency (일관성)
    - CAP이론에서 말하는 Consistency는 ACID의 ‘C’가 아니다!
    - ACID의 ‘C’는 “데이터는 항상 일관성 있는 상태를 유지해야 하고 데이터의 조작 후에도 무결성을 해치지 말아야 한다”는 속성이다.
    - CAP의 ‘C’는 “Single request/response operation sequence”의 속성을 나타낸다. 그 말은 쓰기 동작이 완료된 후 발생하는 읽기 동작은 마지막으로 쓰여진 데이터를 리턴해야 한다는 것을 의미한다.
    - 모든 노드가 같은 시간에 같은 데이터를 보여줘야 한다. (저장된 데이터까지 모두 같을 필요는 없음)
    - 정리해보면 Consistency라는 단어보다는 Atomic이라는 단어가 더 정확하게 특징을 나타낸다고 할 수 있다. (Atomic Data Object, Atomic Consistency)

- Availability (가용성)
    - 특정 노드가 장애가 나도 서비스가 가능해야 한다
    - 데이터 저장소에 대한 모든 동작(read, write 등)은 항상 성공적으로 **리턴**되어야 한다.
    - `서비스가 가능하다`와 `성공적으로 리턴`이라는 표현이 애매함.
        - 20시간정도 기다려서 리턴이 왔다면 Availability가 있는 시스템이라고 할 수 있을까?
        - 시스템이 `Fail`이라는 리턴을 성공적으로 보내준다면 그것을 Availability가 있다고 할 수 있을까?

- Tolerance to network Partitions (파티션 허용)
    - Partition-tolerance라고도 한다.
    - 노드간에 통신 문제가 생겨서 메시지를 주고받지 못하는 상황이라도 동작해야 한다.
    - Availablity와의 차이점은 Availability는 특정 노드가 “장애”가 발생한 상황에 대한 것이고 Tolerance to network Partitions는 노드의 상태는 정상이지만 네트워크 등의 문제로 서로간의 연결이 끊어진 상황에 대한 것이다.

## 4. CAP 이론을 이해해보자

- ![](https://embian.files.wordpress.com/2013/06/understanding_cap1.png)
    - 네트워크가 N1, N2로 구분된 분산환경이다.
    - 각 DB 노드는 V=V0이라는 값을 가지고 있다.
    - 각 네트워크에는 A, B라는 클라이언트가 존재한다.
    - A는 V=V1이라고 쓰고 B가 그것을 읽는다.

- ![](https://embian.files.wordpress.com/2013/06/understanding_cap2.png)

- `C (일관성)`이 꼭 필요한 상황인 경우
    - A가 V1이라고 썼기 때문에 B는 V1이라고 읽을 수 있어야만 한다.
    - A의 쓰기 동작은 M이 복구되기 전까지는 성공할 수 없다.
    
    1. `CP : M이 복구되기 전까지는 A의 Write는 block되거나 실패해야 한다. = Availability가 없음`
    2. `CA : M이 문제가 생길 수 없도록 구성 = Partition-Tolerance가 필요 없음`
    
- `A (가용성)`이 꼭 필요한 상황인 경우
    - 어떤 경우에도 서비스가 Unavailable하면 안된다.
    
    1. `AP : A와 B가 꼭 동일한 데이터를 읽을 필요는 없음`
    2. `CA : M이 문제가 생길 수 없도록 구성 = Partition-Tolerance가 필요 없음`

- `P (파티션 허용)`이 꼭 필요한 상황인 경우

    - 메시지 전달 과정(M)에서 문제가 생기더라도 시스템에 영향이 가서는 안된다.
    1. `AP : A와 B가 꼭 동일한 데이터를 읽을 필요는 없음`
    2. `CP : A의 쓰기 동작은 M이 복구되기를 기다린다. = 그동안 쓰기 서비스 불가능 = Availability가 없음`
    

