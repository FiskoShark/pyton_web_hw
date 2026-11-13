class UserAgentMiddleware:
    def __init__(self, get_response):
        
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', 'Невідомий')

        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Невідома')


        browser = self._detect_browser(user_agent)


        method = request.method



        print("=" * 50)
        print(f"[UserAgentMiddleware]")
        print(f"  User-Agent: {user_agent}")
        print(f"  IP:         {ip}")
        print(f"  Браузер:    {browser}")
        print(f"  Метод:      {method}")
        print(f"  Шлях:       {request.path}")
        print("=" * 50)


        response = self.get_response(request)
        return response

    def _detect_browser(self, user_agent):
        """Просте визначення браузера за рядком User-Agent."""
        ua = user_agent.lower()
        if 'edg' in ua:
            return 'Microsoft Edge'
        elif 'chrome' in ua and 'safari' in ua:
            return 'Google Chrome'
        elif 'firefox' in ua:
            return 'Mozilla Firefox'
        elif 'safari' in ua:
            return 'Safari'
        elif 'opera' in ua or 'opr' in ua:
            return 'Opera'
        else:
            return 'Невідомий браузер'




        