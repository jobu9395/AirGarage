import json

from flask import Flask, redirect, url_for, render_template, request
from yelpapi import YelpAPI
import pandas as pd
from IPython.display import Image, HTML


app = Flask(__name__)


@app.route('/')
def entry():
    title = "Yelp API for locating low-rated parking lots"
    return render_template("entry.html", title=title)


@app.route('/form', methods=["POST"])
def form():
    try:
        yelp_api = YelpAPI(
            'mi5qSSqdhmrNXBjLq5MBMwuqcS0q8aE4u52fwqrG8CkrBjjksgdV8ZblHdh4ThtDqQVFapfOwrCqadcTH4sJIMhQgEcWpc0bK_9ms_rJ1H-xMT1Amp4tmH_PhAg3X3Yx')

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
        link_adjustment(data)
        address_adjustment(data)

        data = data.sort_values(by='parking_lot_score', ascending=True)

        HTML_data = data.to_html(escape=False)

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
        new_image_url = '<img src="%s", alt="business image", style="height:150px">' % image_url
        if image_url != '':
            data['image_url'] = data['image_url'].replace(image_url, new_image_url)

    return data['image_url']


def link_adjustment(data):
    for link_url in data['url']:
        new_link_url = ' <a href="%s">Yelp page link</a> ' % link_url
        data['url'] = data['url'].replace(link_url, new_link_url)

    return data['url']


def address_adjustment(data):
    for address_dict in data['location']:
        del address_dict['address1'], address_dict['address2'], address_dict['address3'], address_dict['city'], address_dict['state'], address_dict['zip_code'], address_dict['country']
    
    return data['location']


def dictionary_to_string(dict):
    string = json.dumps(dict)
    return string




if __name__ == '__main__':
    app.run()
