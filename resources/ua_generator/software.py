from generators import UserAgentGenerator

if __name__ == '__main__':

    pg = UserAgentGenerator()
    for _ in range(250):
        
        p = pg()
        print(p)