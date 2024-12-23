def intercept_requests():
    HTTP_PROXY = 'http://192.168.250.188:8080'
    HTTPS_PROXY = 'http://192.168.250.188:8080'

    import requests
    requests.packages.urllib3.disable_warnings()

    old_merge_environment_settings = requests.Session.merge_environment_settings

    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
        settings['proxies'] = {
            'http': HTTP_PROXY,
            'https': HTTPS_PROXY
        }
        settings['verify'] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings
