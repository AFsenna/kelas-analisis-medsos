import requests
import json

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAPtXiQEAAAAAl%2BeVvjtZIx2mljCEeLWhsYN3HkA%3DKWAJyNAFKPAQLCxnveAKSe8y5Jrd2Tnujr2ytg4vBIUdCTsVqv'


def search_twitter(query, tweet_fields, bearer_token=BEARER_TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results=100".format(
        query, tweet_fields
    )

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


if __name__ == '__main__':
    query = "kekerasan fisik -is:retweet -has:links OR keaadaan korban kekerasan fisik -is:retweet -has:links OR pelaku kekerasan fisik  -is:retweet -has:links OR mental pelaku kekerasan fisik  -is:retweet -has:links OR keadaan mental korban kekerasan fisik -is:retweet -has:links OR fisik anak disakiti -is:retweet -has:links"

    tweet_fields = "tweet.fields=text,author_id,created_at"

    json_response = search_twitter(query=query, tweet_fields=tweet_fields, bearer_token=BEARER_TOKEN)

    filename = 'datasetKekerasanFisik.json'
    with open(filename, 'w', encoding="utf-8") as filehandler:
        filehandler.write('%s\n' % json.dumps(json_response, indent=4, sort_keys=True))