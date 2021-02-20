from flask import Flask, redirect, url_for, render_template, request
from yelpapi import YelpAPI
import pandas as pd


app = Flask(__name__)


@app.route('/')
def entry():
    title = "Yelp API for locating low-rated parking lots"
    return render_template("entry.html", title=title)


@app.route('/form', methods=["POST"])
def form():
    try:
        yelp_api = YelpAPI('mi5qSSqdhmrNXBjLq5MBMwuqcS0q8aE4u52fwqrG8CkrBjjksgdV8ZblHdh4ThtDqQVFapfOwrCqadcTH4sJIMhQgEcWpc0bK_9ms_rJ1H-xMT1Amp4tmH_PhAg3X3Yx')

        location = request.form.get("cityState")
        term = 'parking lot'
        search_limit = 50

        response = yelp_api.search_query(term=term, location=location, limit=search_limit)

        cols = list(response['businesses'][0].keys())
        data = pd.DataFrame(columns=cols)

        for biz in response['businesses']:
            data = data.append(biz, ignore_index=True)

        data_adjustment(data)
        image_adjustment(data)
        data = data.sort_values(by='parking_lot_score', ascending=True)

        HTML_data = data.to_html()
        cityState = location
        cityState = cityState.title()

        title = "List of up to 50 businesses near your entered city and state"

        return render_template("form.html", title=title, cityState=cityState, location_data=HTML_data)

    except:
        return redirect(url_for('error_page'))

@app.route('/error_page')
def error_page():
    title = "Please enter a valid U.S. city and state in the following format: 'City, State'"
    return render_template("error_page.html", title=title)


def data_adjustment(data):
    # add parking_lot_score
    rating = data.rating
    review_count = data.review_count
    parking_lot_score = ( review_count * rating ) / (review_count + 1)
    data['parking_lot_score'] = parking_lot_score

    # remove columns
    del data['id'], data['alias'], data['is_closed'], data['categories'], data['coordinates'], data['transactions'], \
    data['phone'], data['display_phone'], data['distance']

    return data


def image_adjustment(data):
    for image_url in data['image_url']:
        new_image_url = '<img src="%s", alt="business image", style="width:40px;heigh:40px">' % image_url
        if image_url != '':
            data['image_url'] = data['image_url'].replace(image_url, new_image_url)
    return data['image_url']


if __name__ == '__main__':
    app.run()
