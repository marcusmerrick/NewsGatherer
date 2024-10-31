import requests
import json

# MediaStack API details
mediastack_api_key = "eeff43e384e414ea4b0a29143d9eb2ce"
mediastack_url = "http://api.mediastack.com/v1/news"

# Guardian API details
guardian_api_key = "7daa4b83-1cc2-4965-b426-91b66d20e256"
guardian_url = "https://content.guardianapis.com/search"

# Parameters for both APIs
mediastack_params = {
    'access_key': mediastack_api_key,
    'categories': '-general,-sports',
    'sort': 'published_desc',
    'limit': 10,
}

guardian_params = {
    'api-key': guardian_api_key,
    'q': 'election',
    'section': 'politics',
    'order-by': 'newest',
    'page-size': 10,
}

try:
    # Fetching MediaStack data
    response_mediastack = requests.get(mediastack_url, params=mediastack_params)
    response_mediastack.raise_for_status()
    mediastack_data = response_mediastack.json()

    processed_mediastack_data = []
    for article in mediastack_data['data']:
        processed_article = {
            'title': article.get('title', ''),
            'description': article.get('description', ''),
            'url': article.get('url', ''),
            'author': article.get('author', ''),
            'published_at': article.get('published_at', ''),
        }
        content = f"<p><strong>{processed_article['title']}</strong></p>"
        content += f"<p>Author: {processed_article['author']}</p>"
        content += f"<p>Published at: {processed_article['published_at']}</p>"
        content += f"<p>Description: {processed_article['description']}</p>"
        content += f"<p>Read full article at <a href='{processed_article['url']}'>{processed_article['url']}</a></p>"
        processed_article['content'] = content
        processed_mediastack_data.append(processed_article)

    with open('mediastack_news.json', 'w', encoding='utf-8') as f:
        json.dump({'data': processed_mediastack_data}, f, ensure_ascii=False, indent=4)
    
    print("\nMediaStack data saved to mediastack_news.json")

    # Fetching Guardian data
    response_guardian = requests.get(guardian_url, params=guardian_params)
    response_guardian.raise_for_status()
    guardian_data = response_guardian.json()

    processed_guardian_data = []
    for result in guardian_data['response']['results']:
        processed_article = {
            'title': result.get('webTitle', ''),
            'url': result.get('webUrl', ''),
            'published_at': result.get('webPublicationDate', ''),
        }
        content = f"<p><strong>{processed_article['title']}</strong></p>"
        content += f"<p>Published at: {processed_article['published_at']}</p>"
        content += f"<p>Read full article at <a href='{processed_article['url']}'>{processed_article['url']}</a></p>"
        processed_article['content'] = content
        processed_guardian_data.append(processed_article)

    with open('guardian_articles.json', 'w', encoding='utf-8') as f:
        json.dump({'data': processed_guardian_data}, f, ensure_ascii=False, indent=4)
    
    print("\nGuardian data saved to guardian_articles.json")

    # Combine MediaStack data with existing Guardian data
    combined_data = processed_guardian_data + processed_mediastack_data
    combined_data.sort(key=lambda x: x['published_at'], reverse=True)
    combined_data = combined_data[:100]

    with open('combined_articles.json', 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=4)

    print("\nCombined data saved to combined_articles.json")
    print(f"Total articles in combined_articles.json: {len(combined_data)}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {str(e)}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {str(e)}")
