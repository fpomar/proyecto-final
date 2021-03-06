from flask import request, send_file
from flask.json import JSONEncoder
from datetime import datetime
import dateutil.parser
from werkzeug.routing import BaseConverter
import numpy as np
import io
from PIL import Image
import imageio

class DateTimeConverter(BaseConverter):
    def to_python(self, value):
        return dateutil.parser.parse(value)

    def to_url(self, value):
        # TODO: REMOVE HORRIBLE HACK
        if value == '_PARAM_TIMESTR': return value

        return value.isoformat()

class DateTimeJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeJSONEncoder, self).default(obj)

def render_image_array(array):
    image = Image.fromarray((array*255.0).astype(np.uint8))
    return render_image(image)

def render_image(image):
    output = io.BytesIO()
    image.save(output, format='PNG')
    return send_file(io.BytesIO(output.getvalue()), mimetype='image/png')

def render_animation(images, interval=None):
    image_bytes = imageio.mimsave(imageio.RETURN_BYTES, images, format='gif', fps=1.0/interval)
    return send_file(io.BytesIO(image_bytes), mimetype='image/gif')

def request_wants_json():
    best = request.accept_mimetypes \
        .best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']
