from flask import jsonify, send_file
from api import app, db
from api.util import render_image_array
from meteo.meteo_sql import MeteoStaticData


@app.route('/<zone_name>/<datetime:time>/static/<satellite>/<channel>/')
def static_data(zone_name, time, satellite, channel):
    data = db.session.query(MeteoStaticData).filter_by(zone_name=zone_name,
                                                       time=time,
                                                       satellite=satellite,
                                                       channel=channel).first()
    if data is None:
        abort(404)

    data_dict = dict(time=data.state.time,
                     zone_name=data.state.zone.name,
                     satellite=data.satellite,
                     channel=data.channel,
                     size=data.image.shape)
    return jsonify(data_dict)

@app.route('/<zone_name>/<datetime:time>/static/<satellite>/<channel>/image.png')
def static_data_image(zone_name, time, satellite, channel):
    data = db.session.query(MeteoStaticData).filter_by(zone_name=zone_name,
                                                       time=time,
                                                       satellite=satellite,
                                                       channel=channel).first()
    if data is None:
        abort(404)

    return render_image_array(data.image)