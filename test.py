
def go(n, M):
    step = 0 #已经走的步数
    now = 0 # 现在的位置
    if (now == M):
        return step

    step = step + n*n
    now = now + n * n
    if (now < M) :
        return (step + go(n, M - n * n))
    else:
        #return (step + go(n, M + n - 1))
        return (step + go(n, M - (M - (now - M - 1) - (n - 1))))



go(3,10)



