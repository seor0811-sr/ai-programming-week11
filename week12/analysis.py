import pandas as pd

def 정제(df):
    # 1. 점수가 비어 있는 행 삭제
    df = df.dropna(subset=['점수'])
    print("1단계(결측치 삭제) 남은 행 수:", len(df))

    # 2. 모든 열이 완전히 같은 중복 행 삭제
    df = df.drop_duplicates()
    print("2단계(중복 행 삭제) 남은 행 수:", len(df))

    # 3. 반과 과목의 앞뒤 공백 제거
    df['반'] = df['반'].astype(str).str.strip()
    df['과목'] = df['과목'].astype(str).str.strip()
    print("3단계(공백 제거) 남은 행 수:", len(df))

    # 4. 점수가 0~100 범위 밖인 행 삭제
    df['점수'] = pd.to_numeric(df['점수'], errors='coerce')
    df = df[df['점수'].between(0, 100)]
    df = df[df['점수'] % 1 == 0]
    print("4단계(점수 범위 검사) 남은 행 수:", len(df))

    return df


# ① 필터링 
def 수학만(df):
    df = df[df['과목'] == '수학']
    print(len(df))
    return df

# ② 그룹화
def 반별평균(df):
    return df.groupby('반')['점수'].mean()


def 과목반별평균(df):
    return df.groupby(['과목', '반'])['점수'].mean()

# ③ 통계

def 반별통계(df):
    return df.groupby('반')['점수'].agg(
        개수='count',
        평균='mean',
        중앙값='median',
        최댓값='max'
    ).round(2)

if __name__ == "__main__":
    df = pd.read_csv('scores_2026.csv')
    df = 정제(df)
    수학만(df)
    print(반별평균(df))
    print(과목반별평균(df))
    print(반별통계(df))