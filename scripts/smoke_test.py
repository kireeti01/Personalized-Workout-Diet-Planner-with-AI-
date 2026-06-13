import json
import urllib.request
import urllib.error
from datetime import datetime

def post(url, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.getcode(), json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
            return e.code, json.loads(body)
        except Exception:
            return e.code, {'error': e.reason}
    except Exception as e:
        return None, {'error': str(e)}

def main():
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    email = f"smoke+{ts}@example.com"
    print('Using email:', email)

    code, reg = post('http://127.0.0.1:5000/api/register', {'email': email, 'name': 'Smoke Tester', 'password': 'Pass1234'})
    print('\nREGISTER status:', code)
    print(json.dumps(reg, indent=2))

    code, login = post('http://127.0.0.1:5000/api/login', {'email': email, 'password': 'Pass1234'})
    print('\nLOGIN status:', code)
    print(json.dumps(login, indent=2))

    user_id = None
    if isinstance(login, dict):
        user = login.get('user') or login.get('data') or login
        if isinstance(user, dict) and 'id' in user:
            user_id = user['id']
        elif 'id' in login:
            user_id = login['id']

    print('\nResolved user_id:', user_id)

    profile_payload = {
        'user_id': user_id,
        'profile': {
            'age': 28,
            'gender': 'Female',
            'height': 165,
            'weight': 60,
            'fitness_goal': 'Weight Loss',
            'activity_level': 'Light',
            'budget': 'Medium',
            'dietary_preference': 'Vegetarian',
            'available_equipment': 'Bodyweight',
            'health_conditions': 'None'
        }
    }

    code, prof = post('http://127.0.0.1:5000/api/profile', profile_payload)
    print('\nPROFILE status:', code)
    print(json.dumps(prof, indent=2))

if __name__ == '__main__':
    main()
