import streamlit as st


def simple_generator():
    yield 1
    yield 2
    yield 3


def countdown(n):
    while n > 0:
        yield n
        n -= 1


def square_numbers(numbers):
    for n in numbers:
        st.write(f'square_number : {n}')
        yield n * n


def filter_even(numbers):
    for n in numbers:
        st.write(f'filter_even : {n}')
        if n % 2 == 0:
            yield n


if __name__ == '__main__':
    sample_01 = st.button('sample yield 01')

    if sample_01:
        # 제너레이터 객체 생성
        gen = simple_generator()

        # 제너레이터로부터 값 가져오기
        st.write(next(gen))  # 출력: 1
        st.write(next(gen))  # 출력: 2
        st.write(next(gen))  # 출력: 3

        try:
            st.write(next(gen))  # StopIteration 예외 발생
        except StopIteration:
            st.write("제너레이터가 종료되었습니다.")

    sample_02 = st.button('sample yield 02')

    if sample_02:

        # 카운트다운 제너레이터 사용
        for number in countdown(5):
            st.write(number)

    sample_03 = st.button('sample yield 03')
    if sample_03:
        # 제너레이터 체이닝을 통한 사용
        numbers = range(10)
        st.write(numbers)
        squared = square_numbers(numbers)
        even_squares = filter_even(squared)

        st.write(list(even_squares))  # [0, 4, 16, 36, 64]

    sample_04 = st.button('sample yield 04')
    if sample_04:
        import asyncio

        async def async_generator():
            for i in range(5):
                await asyncio.sleep(1)  # 비동기적으로 대기
                yield i

        async def main():
            async for number in async_generator():
                st.write(number)

        # 비동기 실행
        asyncio.run(main())

    sample_05 = st.button('sample yield 05')
    if sample_05:
        def stateful_generator():
            state = 'INIT'
            while True:
                if state == 'INIT':
                    st.write("초기 상태")
                    state = (yield "START")
                elif state == 'RUNNING':
                    st.write("실행 중 상태")
                    state = (yield "RUNNING")
                elif state == 'STOP':
                    st.write("종료 상태")
                    yield "STOP"
                    break

        gen = stateful_generator()
        st.write(next(gen))  # "START" 출력
        st.write(gen.send('RUNNING'))  # "RUNNING" 출력
        st.write(gen.send('STOP'))  # "STOP" 출력
