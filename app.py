
from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ID Bulucu</title>
</head>
<body style="font-family: monospace; padding: 20px;">
    <h2>Instagram ve Facebook ID Bulucu</h2>
    <form method="post">
        <label>Profil Linki:</label><br>
        <input type="text" name="link" size="80" required><br><br>
        <button name="platform" value="instagram">Instagram ID Bul</button>
        <button name="platform" value="facebook">Facebook ID Bul</button>
    </form>
    {% if result %}
    <h3>Sonuç:</h3>
    <p><strong>ID:</strong> {{ result }}</p>
    {% endif %}
</body>
</html>
'''

def get_facebook_id(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        match = re.search(r'entity_id":"(\d+)"', res.text)
        if not match:
            match = re.search(r'fb://profile/(\d+)', res.text)
        return match.group(1) if match else "ID bulunamadı"
    except:
        return "Facebook ID alınamadı"

def get_instagram_id(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        username = url.rstrip('/').split('/')[-1]
        api_url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        res = requests.get(api_url, headers=headers, timeout=10)
        match = re.search(r'"id":"(\d+)"', res.text)
        return match.group(1) if match else "ID bulunamadı"
    except:
        return "Instagram ID alınamadı"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        link = request.form['link']
        platform = request.form['platform']
        if platform == 'facebook':
            result = get_facebook_id(link)
        elif platform == 'instagram':
            result = get_instagram_id(link)
    return render_template_string(HTML_PAGE, result=result)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
