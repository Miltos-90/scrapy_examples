from src.ua_generator.useragent import UserAgent



if __name__ == '__main__':

    failed = 0
    for _ in range(1000):

        try:
            ua = UserAgent().generate()

            device = ('desktop', 'mobile')
            platform = ('windows', 'macos', 'ios', 'linux', 'android')
            browser = ('chrome', 'edge', 'firefox', 'safari')

            ua = UserAgent().generate(device = device, platform = platform, browser = browser)

            #ua = generate(device = ('desktop'))

        except:
            failed += 1

    print(failed)