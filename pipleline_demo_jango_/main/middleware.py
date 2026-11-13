from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
import re
import time

#       ---------------------- 2 -----------------------     #
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time() #
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Невідома')

        response = self.get_response(request)
        
        end_time = time.time() # Час завершення
        process_time = end_time - start_time # час виконання запиту  #

        
        # вивід інформації в консоль #
        print("\n" + "="*50)
        print(f"[LOGGING MIDDLEWARE]")
        print(f"  Метод:   {request.method}")
        print(f"  URL:     {request.path}")
        print(f"  IP:      {ip}")
        print(f"  Статус:  {response.status_code}")
        print(f"  Час:     {process_time:.4f} сек")
        print("="*50 + "\n")
        
        return response




#       ---------------------- 1 -----------------------     #
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
        ua = user_agent.lower()
        if 'edg' in ua:
            return 'Microsoft Edge'
        elif 'opera' in ua or 'opr' in ua:
            return 'Opera'
        elif 'chrome' in ua and 'safari' in ua:
            return 'Google Chrome'
        elif 'firefox' in ua:
            return 'Mozilla Firefox'
        elif 'safari' in ua:
            return 'Safari'
        else:
            return 'Невідомий браузер'



#       ---------------------- 3 -----------------------     #
class IPBlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        #   ---БАН---
        # self.blocked_ips = ['127.0.0.1']  <-- розкоментувати для бану
        self.blocked_ips = []             # <-- закоментувати що б не очищувати перший список


    def __call__(self, request):
        # Отримуємо IP так само, як і в першому middleware
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Невідома')

        # перевірка на наявність IP в чорному списку
        if ip in self.blocked_ips:
            print(f"\n🚫 [BLOCKED] Спроба доступу з заблокованого IP: {ip} на {request.path}")
            return HttpResponseForbidden("<h1>403 Forbidden</h1><p>Ваш IP заблоковано!</p>")

        # якщо IP ok -> пропускаємо запит далі
        return self.get_response(request)

            
#       ---------------------- 4 -----------------------     #
class TrackNumberValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # перевірка чи запит йде до конкретної посилки  #
        #  /parcels/1234567890/ (але не /parcels/) ---- #
        if request.path.startswith('/parcels/') and len(request.path) > 10:
            

            parts = request.path.strip('/').split('/')
            
            if len(parts) >= 2:
                tracking_number = parts[1]
                
                if len(tracking_number) < 10 or len(tracking_number) > 16:
                    print(f"\n❌ [VALIDATION ERROR] Неправильна довжина трек-номеру: {tracking_number}")
                    return HttpResponseBadRequest("<h1>400 Bad Request</h1><p>Трек-номер має містити від 10 до 16 символів!</p>")
                
                # перевірка на заборонені символи  (дозволено тільки A-Z, a-z, 0-9)
                if not re.match(r'^[A-Za-z0-9]+$', tracking_number):
                    print(f"\n❌ [VALIDATION ERROR] Неприпустимі символи в трек-номері: {tracking_number}")
                    return HttpResponseBadRequest("<h1>400 Bad Request</h1><p>Трек-номер може містити лише літери та цифри!</p>")

        # якщо ok  — пропускаємо далі
        return self.get_response(request)



#       ---------------------- 5 -----------------------     #
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        #  словник зберігає історії запитів { 'IP': [time1, time2, ... ]}
        self.request_history = {}

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Невідома')
        current_time = time.time()

        # якщо немає записів для цього IP -> створюємо список
        if ip not in self.request_history:
            self.request_history[ip] = []

        # очищення старіших (за 60) записів та залишання <60 записів
        self.request_history[ip] = [
            t for t in self.request_history[ip] 
            if current_time - t < 60
        ]

        # перевірка кількості запитів
        if len(self.request_history[ip]) >= 10:
            print(f"\n⏳ [RATE LIMIT] Перевищено ліміт для IP: {ip}")
            return HttpResponse(
                "<h1>429 Too Many Requests</h1><p>Забагато запитів! Зачекайте 1 хвилину.</p>", 
                status=429
            )

        # перевірка на ліміт
        self.request_history[ip].append(current_time)

        return self.get_response(request)


