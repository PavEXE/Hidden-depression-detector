from flask import Flask, render_template, request, jsonify
from src.analyzer import analyze_text
from src.feature_extractor import extract_features

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    platform = data.get('platform', 'twitter')

    if not text.strip():
        return jsonify({'error': 'No text provided'}), 400

    features = extract_features(text)
    result = analyze_text(text, features, platform)
    return jsonify(result)

@app.route('/batch', methods=['POST'])
def batch_analyze():
    data = request.get_json()
    posts = data.get('posts', [])
    platform = data.get('platform', 'twitter')

    if not posts:
        return jsonify({'error': 'No posts provided'}), 400

    results = []
    for post in posts:
        features = extract_features(post)
        result = analyze_text(post, features, platform)
        results.append({'text': post[:80] + '...' if len(post) > 80 else post, **result})

    # Aggregate risk
    avg_score = sum(r['risk_score'] for r in results) / len(results)
    high_risk_count = sum(1 for r in results if r['risk_level'] == 'High')

    return jsonify({
        'individual_results': results,
        'aggregate': {
            'avg_risk_score': round(avg_score, 2),
            'high_risk_posts': high_risk_count,
            'total_posts': len(posts),
            'overall_risk': 'High' if avg_score > 0.6 else 'Moderate' if avg_score > 0.35 else 'Low'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
